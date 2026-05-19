"""
DroneAI — Autonomous Drone Voice Assistant
Five-layer architecture:
  1. Audio interface    → audio/
  2. LLM orchestration → Gemini Live + tools/declarations.py
  3. Mission planning  → planner.py + workflows/
  4. Safe execution    → tool_dispatcher.py + safety_policy.py + state_machine.py
  5. Drone backend     → adapters/ (sim | mavlink, switchable via DRONE_BACKEND env)

Setup:
    pip install -r requirements.txt

Run (simulator):
    python app.py

Run (real drone):
    DRONE_BACKEND=mavlink MAVLINK_URI=udp:192.168.1.10:14550 python app.py
"""

import asyncio
import logging
import os
import traceback
from pathlib import Path

from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEY, MODEL, VOICE_NAME,
    CONTEXT_TRIGGER_TOKENS, CONTEXT_TARGET_TOKENS,
    BACKEND, MAVLINK_URI,
    VISION_ENABLED, VISION_FPS, VISION_DEPTH_MIN_MM, VISION_DEPTH_MAX_MM,
    VISION_BLOB_NAME, VISION_BLOB_SHAVES,
    VISION_CAMERA_PITCH_DEG, VISION_CAMERA_YAW_DEG, VISION_CAMERA_HFOV_DEG,
    YOLO_BLOB_DIR, YOLO_AUTO_DOWNLOAD,
    AUDIO_DEVICE_ID,
    DRONET_MODEL_PATH,
    VIOSLAM_ENABLED, VIOSLAM_DB_PATH, VIOSLAM_LOAD_DB,
    VIOSLAM_FPS, VIOSLAM_SLAM_HZ, VIOSLAM_OCC_CELL_SIZE,
)
from schemas import ToolResponse
from state_machine import StateMachine
from safety_policy import SafetyPolicy
from tool_dispatcher import ToolDispatcher
from planner import Planner, PlanDecision
from audio.mic_capture import MicCapture
from audio.playback import Playback
from audio.turn_manager import TurnManager
from telemetry.telemetry_reader import TelemetryReader
from telemetry.battery_monitor import BatteryMonitor
from telemetry.position_monitor import PositionMonitor
from memory.mission_memory import MissionMemory
from memory.environment_memory import EnvironmentMemory
from tools.declarations import FUNCTION_DECLARATIONS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("DroneAI")


# ── Backend factory ────────────────────────────────────────────────────────────

def build_adapter():
    if BACKEND == "mavlink":
        from adapters.mavlink_adapter import MAVLinkAdapter
        logger.info(f"[BACKEND] MAVLink — {MAVLINK_URI}")
        return MAVLinkAdapter(connection_string=MAVLINK_URI)
    from adapters.sim_adapter import SimAdapter
    logger.info("[BACKEND] Simulator")
    return SimAdapter()


# ── Vision + Localization factory ─────────────────────────────────────────────

def build_vision(localizer=None):
    """
    Attempt to build an OakPipeline + VisionTool for the OAK-D Lite.

    Failures are non-fatal: if the camera is absent or depthai is not
    installed, vision tools will return errors at call-time rather than
    crashing the whole app.

    Args:
        localizer: Optional Localizer instance to inject into VisionTool.

    Returns (OakPipeline | None, VisionTool | None).
    """
    if not VISION_ENABLED:
        logger.info("[VISION] Disabled (VISION_ENABLED=0)")
        return None, None

    try:
        from vision.oak_pipeline import OakPipeline
        from vision.vision_tool import VisionTool
    except ImportError as exc:
        logger.warning(f"[VISION] depthai not installed — vision tools disabled ({exc})")
        return None, None

    # Try to download the YOLO blob to local codebase (non-fatal if offline or unavailable)
    blob_path = None
    try:
        # Create local models directory if it doesn't exist
        blob_dir = Path(YOLO_BLOB_DIR)
        blob_dir.mkdir(parents=True, exist_ok=True)
        
        # Construct local blob path
        blob_filename = f"{VISION_BLOB_NAME}.blob"
        local_blob_path = blob_dir / blob_filename
        
        if local_blob_path.exists():
            # Use existing local blob
            blob_path = str(local_blob_path)
            logger.info(f"[VISION] YOLO blob found locally: {blob_path}")
        elif YOLO_AUTO_DOWNLOAD:
            # Download from Luxonis model zoo to local directory
            import blobconverter
            downloaded_blob = blobconverter.from_zoo(
                name=VISION_BLOB_NAME,
                shaves=VISION_BLOB_SHAVES,
                zoo_type="depthai",
                use_cache=True,
            )
            # Copy to local models directory
            import shutil
            shutil.copy(downloaded_blob, local_blob_path)
            blob_path = str(local_blob_path)
            logger.info(f"[VISION] YOLO blob downloaded and cached: {blob_path}")
        else:
            logger.warning(f"[VISION] YOLO_AUTO_DOWNLOAD disabled and blob not found at {local_blob_path}")
    except Exception as exc:
        logger.warning(f"[VISION] Blob download failed ({exc}) — detection tool disabled")

    # Start the OAK-D pipeline (non-fatal if camera not connected)
    try:
        pipeline = OakPipeline(
            fps=VISION_FPS,
            blob_path=blob_path,
            depth_min_mm=VISION_DEPTH_MIN_MM,
            depth_max_mm=VISION_DEPTH_MAX_MM,
        )
        pipeline.start()
        vision_tool = VisionTool(pipeline, localizer=localizer)
        return pipeline, vision_tool
    except Exception as exc:
        logger.warning(f"[VISION] OAK-D init failed ({exc}) — vision tools disabled")
        return None, None


# ── Gemini client + live config ────────────────────────────────────────────────

gemini_client = genai.Client(
    http_options={"api_version": "v1beta"},
    api_key=GEMINI_API_KEY,
)

LIVE_CONFIG = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=VOICE_NAME)
        )
    ),
    context_window_compression=types.ContextWindowCompressionConfig(
        trigger_tokens=CONTEXT_TRIGGER_TOKENS,
        sliding_window=types.SlidingWindow(target_tokens=CONTEXT_TARGET_TOKENS),
    ),
    tools=[types.Tool(function_declarations=FUNCTION_DECLARATIONS)],
    system_instruction=types.Content(
        parts=[types.Part.from_text(text=(
            "Your name is RayeedAI (রাইদ-এআই). "
            "You are an autonomous drone flight assistant. "
            "Only respond in Bangla. "
            "When the user gives a flight command, execute it step by step using the available tools. "
            "If a safety concern arises mid-mission, you may ask one brief clarifying question "
            "in Bangla before proceeding. Otherwise do not ask questions."
        ))],
        role="user",
    ),
)


# ──────────────────────────────────────────────────────────────────────────────
# DroneAI — main application class
# ──────────────────────────────────────────────────────────────────────────────

class DroneAI:
    def __init__(self):
        self.session        = None

        # Queues
        self.audio_in_queue = asyncio.Queue()   # AI audio → speaker
        self.mic_queue      = asyncio.Queue()   # mic PCM  → session

        # ── Layer 5: Backend ────────────────────────────────────────────────
        self.adapter        = build_adapter()

        # ── Localization: PoseCache + Localizer ─────────────────────────────
        # Built before Vision so the Localizer can be injected into VisionTool.
        from localization.pose_cache import PoseCache
        from localization.localizer import Localizer
        self.pose_cache     = PoseCache()
        self.localizer      = Localizer(
            self.pose_cache,
            camera_pitch_deg=VISION_CAMERA_PITCH_DEG,
            camera_yaw_deg=VISION_CAMERA_YAW_DEG,
            hfov_deg=VISION_CAMERA_HFOV_DEG,
        )

        # ── Layer 0: Vision (OAK-D Lite) — non-fatal if camera absent ───────
        self.oak_pipeline, _vision_tool = build_vision(localizer=self.localizer)

        # ── Layer 4: Safe execution ─────────────────────────────────────────
        self.sm             = StateMachine()
        self.safety         = SafetyPolicy(self.sm)
        self.dispatcher     = ToolDispatcher(self.sm, self.safety, self.adapter, _vision_tool)

        # ── VIO/SLAM runner (background task — feature-flagged, non-fatal) ──
        self.vioslam_runner = None
        if VIOSLAM_ENABLED:
            from localization.vio_slam.vio_slam_runner import VIOSLAMRunner
            self.vioslam_runner = VIOSLAMRunner(
                db_path=VIOSLAM_DB_PATH,
                load_db=VIOSLAM_LOAD_DB,
                fps=VIOSLAM_FPS,
                slam_hz=VIOSLAM_SLAM_HZ,
                occ_cell_size=VIOSLAM_OCC_CELL_SIZE,
                pose_cache=self.pose_cache,
            )
            self.safety.set_vioslam_runner(self.vioslam_runner)

        # ── Layer 3: Mission planning ────────────────────────────────────────
        self.planner        = Planner(self.sm, self.safety, self.dispatcher)

        # ── Layer 1: Audio interface ─────────────────────────────────────────
        self.turn_manager   = TurnManager()
        self.mic_capture    = MicCapture(self.mic_queue)
        self.playback       = Playback(self.audio_in_queue)

        # ── Telemetry (background tasks) — pose_cache injected for localization
        self.tel_reader     = TelemetryReader(self.dispatcher, self.safety, self.pose_cache)
        self.bat_monitor    = BatteryMonitor(self.dispatcher, self.safety, self.planner)
        self.pos_monitor    = PositionMonitor(self.dispatcher, self.pose_cache)

        # ── Memory (persistent state) ────────────────────────────────────────
        self.mission_mem    = MissionMemory()
        self.env_mem        = EnvironmentMemory()

    # ── DroNet avoidance loop (Layer 2 — autonomous, not LLM-driven) ──────────

    async def _avoidance_loop(self) -> None:
        """Run DroNet at ~20 Hz as a background task (non-fatal if OAK-D absent)."""
        try:
            from vision.avoidance.dronet_runner import DroNetRunner
        except ImportError as exc:
            logger.warning(f"[AVOIDANCE] DroNetRunner not available: {exc}")
            return

        runner = DroNetRunner(
            mav_connection_string=MAVLINK_URI,
            model_path=DRONET_MODEL_PATH,
        )
        self.safety.set_avoidance_runner(runner)
        await runner.run()

    # ── VIO/SLAM loop (Layer 2 — autonomous pose + occupancy mapping) ─────────

    async def _vioslam_loop(self) -> None:
        """Run RTABMap VIO + SLAM at camera fps as a background task.

        No-op when VIOSLAM_ENABLED=0 (runner is None).  Non-fatal on any
        runtime failure — see VIOSLAMRunner.run().
        """
        if self.vioslam_runner is None:
            return
        await self.vioslam_runner.run()

    # ── Send mic PCM to Gemini ─────────────────────────────────────────────────

    async def send_audio(self):
        while True:
            data = await self.mic_queue.get()
            if self.session:
                await self.session.send_realtime_input(
                    audio=types.Blob(data=data, mime_type="audio/pcm")
                )

    # ── Extract thought + text parts from server_content ──────────────────────

    def _log_model_parts(self, response):
        """
        Parse server_content.model_turn.parts for:
          - thought=True  → [THOUGHT] log (model's internal reasoning chain)
          - text part     → [TEXT]    log (transcript, also voiced if audio modality active)
        Both are logged every turn for full debug visibility.
        """
        sc = getattr(response, "server_content", None)
        if not sc:
            return
        turn = getattr(sc, "model_turn", None)
        if not turn:
            return
        for part in getattr(turn, "parts", []) or []:
            text = getattr(part, "text", None)
            if not text:
                continue
            if getattr(part, "thought", False):
                # Model's internal reasoning — log only, no voice
                logger.info(f"[THOUGHT] {text.strip()}")
            else:
                # Spoken transcript — log alongside voice audio
                logger.info(f"[TEXT] {text.strip()}")
                print(f"\n[AI TEXT] {text.strip()}", flush=True)

    # ── Receive from Gemini (audio + tool calls) ───────────────────────────────

    async def receive_responses(self):
        """
        Resilient receive loop — a single tool response failure no longer
        kills the task. The loop restarts after each recoverable exception,
        keeping mic, playback, and telemetry tasks alive.
        """
        while True:
            if not self.session:
                await asyncio.sleep(0.05)
                continue
            try:
                async for response in self.session.receive():

                    # ── Thought + text parts (log + voice if available) ──────
                    self._log_model_parts(response)

                    # ── Tool call → dispatcher → planner ────────────────────
                    if tool_call := response.tool_call:
                        for fc in tool_call.function_calls:
                            args = dict(fc.args) if fc.args else {}
                            logger.info(f"[LLM] Tool call: {fc.name}({args})")

                            # Dispatcher: validate → safety → adapter → normalize → state
                            tool_resp: ToolResponse = await self.dispatcher.dispatch(fc.name, args)

                            # Planner authority: may override LLM next_action
                            decision = await self.planner.decide(tool_resp)
                            logger.info(f"[PLANNER] {fc.name} → {decision.value}")

                            if decision == PlanDecision.WAIT and tool_resp.wait:
                                # Non-blocking — audio + telemetry keep running
                                self.planner.schedule_wait(tool_resp.wait)

                            elif decision in (PlanDecision.FAILSAFE, PlanDecision.ABORT):
                                await self.planner.trigger_failsafe(
                                    reason=tool_resp.error or f"planner {decision.value}"
                                )

                            elif decision == PlanDecision.REPLAN:
                                logger.warning("[PLANNER] Low battery — replanning toward RTH")
                                from workflows.return_home import run_return_home
                                asyncio.ensure_future(self.planner.run_workflow(run_return_home))

                            # Persist mission state after every tool call
                            self.mission_mem.save_state({
                                "mission_state": self.sm.state.value,
                                "last_tool":     fc.name,
                            })

                            # ── Send tool result back to LLM (guarded) ───────
                            # FunctionResponse is the correct class — NOT types.ToolResponse
                            try:
                                await self.session.send_tool_response(
                                    function_responses=[
                                        types.FunctionResponse(
                                            id=fc.id,
                                            name=fc.name,
                                            response=tool_resp.to_dict(),
                                        )
                                    ]
                                )
                            except Exception as send_exc:
                                logger.error(
                                    f"[TOOL_RESPONSE] Failed to send result for "
                                    f"'{fc.name}': {send_exc} — session may be stale"
                                )
                        continue

                    # ── AI audio chunk ───────────────────────────────────────
                    if data := response.data:
                        self.turn_manager.block()
                        self.audio_in_queue.put_nowait(data)
                        continue

                    # ── Turn complete ────────────────────────────────────────
                    if response.server_content and response.server_content.turn_complete:
                        self.turn_manager.unblock()
                        while not self.audio_in_queue.empty():
                            self.audio_in_queue.get_nowait()
                        logger.info("[TURN] Complete — mic unblocked")

            except asyncio.CancelledError:
                # Propagate shutdown — do not restart
                raise
            except Exception as exc:
                # Any other exception (AttributeError, connection drop, etc.)
                # is logged and the loop restarts — audio tasks keep running
                logger.error(f"[RECEIVE] Recoverable error: {exc} — restarting receive loop")
                await asyncio.sleep(0.5)

    # ── Main run loop ──────────────────────────────────────────────────────────

    async def run(self):
        """
        Two-group task isolation:

          Group A — SESSION tasks (mic, send, receive, playback)
            A crash here means the Gemini session is unrecoverable → full exit.
            receive_responses() has its own internal restart loop for soft errors.

          Group B — BACKGROUND tasks (telemetry, battery, position)
            Each has internal try/except. They run independently and are cancelled
            cleanly on shutdown — a background crash does NOT kill audio.
        """
        loop = asyncio.get_event_loop()

        # ── Background tasks started before session opens ──────────────────
        background_tasks = [
            loop.create_task(self.tel_reader.run(),      name="telemetry_reader"),
            loop.create_task(self.bat_monitor.run(),     name="battery_monitor"),
            loop.create_task(self.pos_monitor.run(),     name="position_monitor"),
            loop.create_task(self._avoidance_loop(),     name="avoidance_loop"),
            loop.create_task(self._vioslam_loop(),       name="vioslam_loop"),
        ]

        try:
            async with gemini_client.aio.live.connect(model=MODEL, config=LIVE_CONFIG) as session:
                self.session = session
                logger.info("=" * 60)
                logger.info("  RayeedAI — DroneAI started")
                logger.info(f"  Backend : {BACKEND.upper()}")
                logger.info(f"  Vision  : {'OAK-D Lite' if self.oak_pipeline and self.oak_pipeline.available else 'disabled'}")
                logger.info(f"  VIO/SLAM: {'enabled' if self.vioslam_runner is not None else 'disabled'}")
                logger.info(f"  State   : {self.sm.state.value}")
                logger.info("  Speak to RayeedAI. Press Ctrl+C to exit.")
                logger.info("=" * 60)

                # ── Session tasks — all must stay alive ────────────────────
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(self.mic_capture.run(self.turn_manager), name="mic_capture")
                    tg.create_task(self.send_audio(),                        name="send_audio")
                    tg.create_task(self.receive_responses(),                  name="receive_responses")
                    tg.create_task(self.playback.run(self.turn_manager),     name="playback")

        except asyncio.CancelledError:
            logger.info("[SESSION] Shutting down...")
        except ExceptionGroup as eg:
            traceback.print_exception(eg)
        except Exception as exc:
            logger.critical(f"[SESSION] Fatal error: {exc}")
            traceback.print_exc()
        finally:
            # Cancel background tasks cleanly
            for task in background_tasks:
                task.cancel()
            await asyncio.gather(*background_tasks, return_exceptions=True)
            if self.oak_pipeline is not None:
                self.oak_pipeline.stop()
            logger.info("[SESSION] Terminated.")


# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    asyncio.run(DroneAI().run())
