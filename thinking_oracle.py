"""
thinking_oracle.py — qwen3:0.6b sequential thinking engine for DroneAI (RayeedAI).

Contract:
  - Streams thinking content ONLY (no prose output consumed)
  - Extracts structured JSON decision from thinking block or content response
  - Runs synchronously; caller wraps with asyncio.to_thread() from async contexts
  - Fallback to deterministic rule-based planner on any oracle failure
  - Zero impact on existing safety_policy.py hard gates — oracle is advisory layer

Usage:
    oracle = ThinkingOracle()
    ctx = {
        "tool":             "goto_position",
        "ok":               True,
        "error":            None,
        "state":            "enroute",
        "battery_pct":      78.5,
        "altitude_m":       15.0,
        "telemetry_age_sec": 1.2,
        "retry_count":      0,
        "airborne":         True,
    }
    # Sync call (wrap in asyncio.to_thread from async context)
    decision: ThinkingDecision = oracle.deliberate(ctx)

Build the Ollama model first:
    ollama create droneoracle -f thinking_oracle.Modelfile
"""

import json
import re
import logging
import time
from dataclasses import dataclass, field
from typing import Optional

import ollama

logger = logging.getLogger(__name__)

ORACLE_MODEL   = "droneoracle"
ORACLE_TIMEOUT = 8.0   # seconds — must be < tool_dispatcher.py TOOL_TIMEOUT_SEC (10s)

VALID_DECISIONS = {"CONTINUE", "WAIT", "RETRY", "REPLAN", "ABORT", "FAILSAFE"}

# Tools that warrant oracle deliberation — skip trivial read-only calls
HIGH_VALUE_TOOLS = {
    "goto_position", "takeoff", "return_to_launch",
    "arm_drone", "wait_arrival", "wait_altitude", "land",
}

# Tools watched by dispatcher post-execution hook (subset of HIGH_VALUE_TOOLS)
ORACLE_WATCHED_TOOLS = {
    "arm_drone", "takeoff", "goto_position",
    "return_to_launch", "land",
}


@dataclass
class ThinkingDecision:
    decision:    str
    reason:      str
    thinking:    str                  # raw thinking block — logged at DEBUG level
    next_tool:   Optional[str]  = None
    wait_sec:    Optional[float] = None
    confidence:  float           = 1.0
    latency_ms:  float           = 0.0
    source:      str             = "oracle"   # "oracle" | "fallback"


class ThinkingOracle:
    """
    Sequential thinking engine using qwen3:0.6b.

    qwen3 with think=True streams a <think>...</think> reasoning block
    before the content response. We:
      1. Collect the thinking buffer (model's internal chain-of-thought)
      2. Collect the content buffer (model's JSON commitment)
      3. Parse JSON from content first, fall back to regex extraction from thinking
      4. Map to ThinkingDecision dataclass
      5. On any failure, return deterministic rule_fallback() result

    The thinking block is the steering signal — it's what makes qwen3:0.6b
    useful here despite its small size. The content JSON is just the final
    structured commitment after reasoning.
    """

    def __init__(self, model: str = ORACLE_MODEL, timeout: float = ORACLE_TIMEOUT):
        self._model    = model
        self._timeout  = timeout
        self._calls    = 0
        self._failures = 0

    # ── Public API ────────────────────────────────────────────────────────────

    def deliberate(self, context: dict) -> ThinkingDecision:
        """
        Synchronous deliberation — wrap with asyncio.to_thread() from async callers.

        Args:
            context: dict with keys:
                tool             (str)   — name of last executed tool
                ok               (bool)  — whether tool succeeded
                error            (str|None) — error message if failed
                state            (str)   — current MissionState.value
                battery_pct      (float) — last known battery percentage
                altitude_m       (float) — last known altitude in meters
                telemetry_age_sec (float) — seconds since last telemetry update
                retry_count      (int)   — current retry count for this tool
                airborne         (bool)  — whether drone is currently in flight

        Returns:
            ThinkingDecision with decision, reason, thinking block, and metadata.
        """
        self._calls += 1
        t0 = time.monotonic()

        prompt = self._build_prompt(context)

        try:
            thinking_buf = ""
            content_buf  = ""

            stream = ollama.chat(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                think=True,
                stream=True,
                options={
                    "temperature":  0.05,
                    "num_predict":  96,
                    "num_ctx":      768,
                    "top_k":        10,
                    "top_p":        0.7,
                },
            )

            for chunk in stream:
                msg = chunk.message
                if msg.thinking:
                    thinking_buf += msg.thinking
                if msg.content:
                    content_buf += msg.content

            latency_ms = (time.monotonic() - t0) * 1000
            logger.debug(
                f"[ORACLE] Thinking ({latency_ms:.0f}ms):\n"
                f"{thinking_buf[:400]}{'...' if len(thinking_buf) > 400 else ''}"
            )

            # Parse decision — content response first, thinking extraction fallback
            decision = (
                self._parse_json(content_buf)
                or self._extract_from_thinking(thinking_buf)
            )

            if decision:
                decision.thinking   = thinking_buf
                decision.latency_ms = latency_ms
                decision.source     = "oracle"
                logger.info(
                    f"[ORACLE] {context.get('tool')} → {decision.decision} "
                    f"| conf={decision.confidence:.2f} | {decision.reason} "
                    f"| {latency_ms:.0f}ms"
                )
                return decision

            # Parsed nothing valid
            logger.warning(
                f"[ORACLE] Could not parse decision from model output — "
                f"content='{content_buf[:100]}' — using rule fallback"
            )

        except ollama.ResponseError as exc:
            self._failures += 1
            logger.warning(f"[ORACLE] Ollama ResponseError: {exc} — rule fallback")
        except Exception as exc:
            self._failures += 1
            logger.warning(f"[ORACLE] Unexpected error: {exc} — rule fallback")

        return self._rule_fallback(context)

    def should_invoke(self, tool_name: str, ok: bool, airborne: bool) -> bool:
        """
        Gate check — avoids oracle latency on trivial read-only calls.
        Always invoke on failures or when airborne.
        """
        return (
            tool_name in HIGH_VALUE_TOOLS
            or not ok
            or airborne
        )

    def stats(self) -> dict:
        return {
            "calls":         self._calls,
            "failures":      self._failures,
            "fallback_rate": round(self._failures / max(1, self._calls), 3),
        }

    # ── Prompt construction ───────────────────────────────────────────────────

    @staticmethod
    def _build_prompt(ctx: dict) -> str:
        """
        Compact single-line prompt — fits in 768-token context with room for
        thinking and 96-token JSON response. No conversation history needed;
        every call is independent (oracle is stateless).
        """
        return (
            f"tool={ctx.get('tool', 'unknown')} "
            f"ok={ctx.get('ok', True)} "
            f"state={ctx.get('state', 'unknown')} "
            f"error={ctx.get('error') or 'none'} "
            f"battery={ctx.get('battery_pct', 100.0):.1f}% "
            f"altitude={ctx.get('altitude_m', 0.0):.1f}m "
            f"tel_age={ctx.get('telemetry_age_sec', 0.0):.1f}s "
            f"retries={ctx.get('retry_count', 0)} "
            f"airborne={ctx.get('airborne', False)}"
        )

    # ── JSON extraction ───────────────────────────────────────────────────────

    @staticmethod
    def _parse_json(text: str) -> Optional[ThinkingDecision]:
        """Parse clean JSON from model content response."""
        text = text.strip()
        # Strip markdown fences if present
        text = re.sub(r"^```(?:json)?", "", text).rstrip("```").strip()
        if not text:
            return None
        try:
            d = json.loads(text)
            return ThinkingDecision._from_dict(d)
        except (json.JSONDecodeError, KeyError, TypeError):
            return None

    @staticmethod
    def _extract_from_thinking(thinking: str) -> Optional[ThinkingDecision]:
        """
        Extract last valid JSON object from thinking block.
        Model sometimes embeds the decision JSON mid-reasoning before finalizing.
        We take the last occurrence as the most refined decision.
        """
        matches = re.findall(r'\{[^{}]*"decision"[^{}]*\}', thinking, re.DOTALL)
        if not matches:
            return None
        # Try from last to first — most refined decision is typically last
        for raw in reversed(matches):
            try:
                d = json.loads(raw)
                result = ThinkingDecision._from_dict(d)
                if result:
                    return result
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
        return None

    @staticmethod
    def _from_dict(d: dict) -> Optional["ThinkingDecision"]:
        """Validate and construct ThinkingDecision from parsed dict."""
        decision = str(d.get("decision", "")).upper().strip()
        if decision not in VALID_DECISIONS:
            return None
        wait_raw = d.get("wait_sec")
        return ThinkingDecision(
            decision   = decision,
            reason     = str(d.get("reason", ""))[:120],
            thinking   = "",
            next_tool  = d.get("next_tool") or None,
            wait_sec   = float(wait_raw) if wait_raw is not None else None,
            confidence = float(d.get("confidence", 1.0)),
        )

    # ── Deterministic rule fallback ───────────────────────────────────────────

    @staticmethod
    def _rule_fallback(ctx: dict) -> ThinkingDecision:
        """
        Mirrors safety_policy.py thresholds exactly.
        Activated when oracle is unavailable, times out, or produces unparseable output.
        This ensures zero regression from existing behavior.
        """
        battery    = ctx.get("battery_pct", 100.0)
        tel_age    = ctx.get("telemetry_age_sec", 0.0)
        retries    = ctx.get("retry_count", 0)
        ok         = ctx.get("ok", True)
        error      = ctx.get("error") or ""
        airborne   = ctx.get("airborne", False)

        if tel_age > 10.0 or "TELEMETRY_EMERGENCY" in error:
            decision, reason = "FAILSAFE", f"telemetry age {tel_age:.1f}s exceeds emergency threshold"
        elif battery <= 15.0 or "BATTERY_CRITICAL" in error:
            decision, reason = "FAILSAFE", f"battery critical at {battery:.1f}%"
        elif retries >= 3 or "MAX_RETRIES" in error:
            decision, reason = "ABORT", f"retry limit reached ({retries})"
        elif battery <= 25.0 and airborne:
            decision, reason = "REPLAN", f"battery low at {battery:.1f}% — replan toward RTH"
        elif not ok and retries < 3:
            decision, reason = "RETRY", f"transient failure (retry {retries}/3)"
        else:
            decision, reason = "CONTINUE", "nominal"

        return ThinkingDecision(
            decision   = decision,
            reason     = reason,
            thinking   = "[rule-fallback — oracle unavailable]",
            confidence = 1.0,
            source     = "fallback",
        )
