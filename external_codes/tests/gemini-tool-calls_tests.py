import os
import json
from google import genai
from google.genai import types


# ==========================================
# Pythonic Tool Definitions
# The SDK automatically builds schemas from docstrings and type hints.
# ==========================================

def observe(data: list[str]) -> dict:
    """Return drone state or sensor data for reasoning.
    Always observe battery and GPS before arming or navigating.
    Valid items: "battery", "gps", "heading", "airspeed", "local_vio", "depth".
    """
    result = {}
    for key in data:
        if key == "battery":
            result["battery"] = {"percent": 82, "voltage": 14.8}
        elif key == "gps":
            result["gps"] = {"fix": "3D", "satellites": 12, "lat": 47.3977, "lon": 8.5456, "alt_rel": 0.0, "alt_amsl": 120.0}
        elif key == "heading":
            result["heading"] = {"degrees": 270}
        elif key == "local_vio":
            result["local_vio"] = {"x": 0.0, "y": 0.0, "z": -1.5}
        else:
            result[key] = {"value": 0.0}
    return result

def arm() -> dict:
    """Arm the motors. Requires GUIDED mode first."""
    return {"status": "armed"}

def disarm() -> dict:
    """Disarm the motors. Only when on the ground after landing."""
    return {"status": "disarmed"}

def set_mode(mode: str) -> dict:
    """Set ArduCopter flight mode.
    Args:
        mode: "GUIDED" | "RTL" | "LAND" | "LOITER" | "POSHOLD" | "STABILIZE"
              GUIDED is required before arm/navigate. RTL returns to launch.
              LAND lands in place. LOITER holds position.
    """
    return {"status": "ok", "mode": mode}

def goto_gps(lat: float, lon: float, alt: float, yaw: float = None) -> dict:
    """Fly to an absolute GPS coordinate. Requires GUIDED mode and armed.
    Args:
        lat: Target latitude in decimal degrees.
        lon: Target longitude in decimal degrees.
        alt: Target altitude in meters above home (takeoff point).
        yaw: Optional target heading 0-359 degrees.
    """
    return {"status": "moving", "frame": "global", "lat": lat, "lon": lon, "alt": alt}

def goto_local(x: float, y: float, z: float, yaw: float = None) -> dict:
    """Fly to NED position relative to origin (arming point).
    x=North, y=East, z=Down. Use negative z to climb (z=-10 means 10m altitude).
    Args:
        x: North offset in meters.
        y: East offset in meters.
        z: Down offset in meters (negative = up/climb).
        yaw: Optional target heading 0-359 degrees.
    """
    return {"status": "moving", "frame": "local_ned", "x": x, "y": y, "z": z}

def move_body(dx: float, dy: float, dz: float) -> dict:
    """Move relative to current position in body frame.
    dx=forward, dy=right, dz=down (negative values = backward/left/up).
    Useful for fine adjustments and obstacle avoidance.
    Args:
        dx: Forward offset in meters (negative = backward).
        dy: Right offset in meters (negative = left).
        dz: Down offset in meters (negative = up).
    """
    return {"status": "moving", "frame": "body_offset", "dx": dx, "dy": dy, "dz": dz}


# Unified Dispatcher Registry
TOOL_REGISTRY = {
    "observe": observe,
    "arm": arm,
    "disarm": disarm,
    "set_mode": set_mode,
    "goto_gps": goto_gps,
    "goto_local": goto_local,
    "move_body": move_body,
}


SYSTEM_PROMPT = """\
You are AerialAgent, an autonomous drone planner (ArduCopter / ArduPilot).

SAFETY RULES (never skip):
1. observe(['battery','gps']) before every arm or navigate — abort if battery < 20% or GPS fix != 3D.
2. set_mode('GUIDED') before arm.
3. observe(['local_vio']) after every goto_* to verify position.
4. Finish by set_mode('LAND') or set_mode('RTL'), then disarm after touchdown.

FLIGHT SEQUENCE:
  observe → set_mode(GUIDED) → arm → goto_gps/goto_local/move_body → observe → ... → set_mode(LAND) → disarm

TOOLS:
  arm()                    — arm motors
  disarm()                 — disarm motors
  set_mode(mode)           — GUIDED | RTL | LAND | LOITER | POSHOLD | STABILIZE
  goto_gps(lat, lon, alt)  — absolute GPS target
  goto_local(x, y, z)     — NED offset from origin (z negative = climb)
  move_body(dx, dy, dz)   — body-relative offset
  observe(data[])          — battery | gps | heading | airspeed | local_vio | depth
"""

def run_agent(mission: str, max_turns: int = 10) -> None:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")

    client = genai.Client(api_key=api_key)

    config = types.GenerateContentConfig(
        temperature=0.2,
        thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=2048),
        tools=list(TOOL_REGISTRY.values()),
        system_instruction=[types.Part.from_text(text=SYSTEM_PROMPT)],
    )

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=mission)])]

    for turn in range(max_turns):
        print(f"\n{'-' * 40}\nTurn {turn + 1}\n{'-' * 40}")

        final_chunk, in_thought = None, False
        for chunk in client.models.generate_content_stream(
            model="gemini-2.5-flash-lite",
            contents=contents,
            config=config,
        ):
            parts = chunk.candidates[0].content.parts if chunk.candidates and chunk.candidates[0].content else []
            for part in parts:
                if getattr(part, "thought", False):
                    if not in_thought:
                        print("\n[thinking]", flush=True)
                        in_thought = True
                    if part.text:
                        print(part.text, end="", flush=True)
                else:
                    if in_thought:
                        print("\n[/thinking]\n", flush=True)
                        in_thought = False
                    if part.text:
                        print(part.text, end="", flush=True)
            final_chunk = chunk

        if in_thought:
            print("\n[/thinking]\n", flush=True)

        candidate = final_chunk.candidates[0]
        parts = candidate.content.parts if candidate.content else []
        function_calls = [p.function_call for p in parts if p.function_call]

        contents.append(types.Content(role="model", parts=parts))

        if not function_calls:
            print(f"\n[done] Agent finished task.")
            break

        tool_responses = []
        for fc in function_calls:
            args = dict(fc.args) if fc.args else {}
            print(f"\n[tool call] {fc.name}({json.dumps(args)})")

            result_dict = TOOL_REGISTRY[fc.name](**args)
            print(f"[tool result] {result_dict}")

            tool_responses.append(
                types.Part.from_function_response(name=fc.name, response=result_dict)
            )

        contents.append(types.Content(role="user", parts=tool_responses))

if __name__ == "__main__":
    MISSION = (
        "Fly to waypoint at latitude 47.3980, longitude 8.5460, altitude 50 metres. "
        "Confirm position after arrival, then return to launch."
    )
    run_agent(MISSION)
