import os
import json
from google import genai
from google.genai import types

# ==========================================
# Target 1: Pythonic Tool Definitions
# The SDK automatically builds schemas from docstrings and type hints.
# ==========================================

def observe(data: list[str]) -> dict:
    """Return drone state or sensor data for reasoning.
    Always observe battery and GPS before arming or navigating.
    Valid items: "battery", "gps", "heading", "airspeed", "local_vio", "depth".
    """
    result = {}
    for key in data:
        if key == "battery": result["battery"] = {"percent": 82, "voltage": 14.8}
        elif key == "gps": result["gps"] = {"fix": "3D", "satellites": 12, "lat": 47.3977, "lon": 8.5456, "alt": 120.0}
        elif key == "heading": result["heading"] = {"degrees": 270}
        elif key == "local_vio": result["local_vio"] = {"x": 0.0, "y": 0.0, "z": -1.5}
        else: result[key] = {"value": 0.0}
    return result

def control(action: str, mode: str = "") -> dict:
    """Vehicle state control such as arming, disarming, or mode switching.
    Args:
        action: "arm", "disarm", or "set_mode"
        mode: "MANUAL", "OFFBOARD", "LAND", or "RTL" (required if action is set_mode)
    """
    if action == "arm": return {"status": "armed", "message": "Vehicle armed"}
    elif action == "disarm": return {"status": "disarmed", "message": "Vehicle disarmed"}
    elif action == "set_mode": return {"status": "ok", "mode": mode}
    return {"status": "error", "message": "Unknown action"}

def navigate(frame: str, lat: float = 0.0, lon: float = 0.0, alt: float = 0.0, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> dict:
    """Move drone to a position using one coordinate frame.
    Args:
        frame: "global" (lat/lon/alt) or "local" (x/y/z in NED meters).
    """
    return {"status": "executing", "frame": frame, "message": f"Navigation started in {frame} frame"}

# Target 2: Unified Dispatcher Registry
TOOL_REGISTRY = {"observe": observe, "control": control, "navigate": navigate}

# ==========================================
# Target 3: Prompt Harmonization
# ==========================================

SYSTEM_PROMPT = """\
You are AerialAgent, an autonomous drone planner.
Goal: Safely achieve the mission via tools.

━━━ Safety Rules ━━━
1. MUST observe(["battery", "gps"]) before doing anything else.
2. MUST set_mode to "OFFBOARD" before arming.
3. Verify position with observe(["local_vio"]) after navigating.
4. Finish by disarming or setting mode to "LAND".
Abort if battery < 20% or GPS fix is not 3D.

━━━ Final Output Phase ━━━
Once physical tasks are complete, output your final response as ONLY a JSON summary:
{
  "tasks": [
    {"id": "1", "tool": "observe", "args": {"data": ["battery"]}}
  ]
}
"""

def run_agent(mission: str, max_turns: int = 10) -> None:
    api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyCCIKOChwt4ywQPOdTf1iRbrh_547Ir1Mo")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")

    client = genai.Client(api_key=api_key)
    
    config = types.GenerateContentConfig(
        temperature=0.2, # Lowered for better planning stability
        thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=2048),
        tools=list(TOOL_REGISTRY.values()), # Directly pass Python functions!
        system_instruction=[types.Part.from_text(text=SYSTEM_PROMPT)],
    )

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=mission)])]

    # ==========================================
    # Target 4: Streamlined Loop
    # ==========================================
    for turn in range(max_turns):
        print(f"\n{'-' * 40}\nTurn {turn + 1}\n{'-' * 40}")
        
        final_chunk, in_thought = None, False
        for chunk in client.models.generate_content_stream(
            model="gemini-2.5-flash-lite", # Upgraded to standard flash model for reasoning
            contents=contents,
            config=config,
        ):
            parts = chunk.candidates[0].content.parts if chunk.candidates and chunk.candidates[0].content else []
            for part in parts:
                if getattr(part, "thought", False):
                    if not in_thought: print("\n[thinking]", flush=True); in_thought = True
                    if part.text: print(part.text, end="", flush=True)
                else:
                    if in_thought: print("\n[/thinking]\n", flush=True); in_thought = False
                    if part.text: print(part.text, end="", flush=True)
            final_chunk = chunk

        if in_thought: print("\n[/thinking]\n", flush=True)

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
            
            # Execute natively via the registry
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