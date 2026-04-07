import os
import json
from google import genai
from google.genai import types


def execute_tool(name: str, args: dict) -> str:
    """
    Stub executor — replace with real drone API calls.
    Returns a JSON string result that gets fed back to the model.
    """
    if name == "observe":
        # Simulate telemetry data for each requested sensor
        data_keys = args.get("data", [])
        result = {}
        for key in data_keys:
            if key == "battery":
                result["battery"] = {"percent": 82, "voltage": 14.8}
            elif key == "gps":
                result["gps"] = {"fix": "3D", "satellites": 12, "lat": 47.3977, "lon": 8.5456, "alt": 120.0}
            elif key == "heading":
                result["heading"] = {"degrees": 270}
            elif key == "airspeed":
                result["airspeed"] = {"ms": 0.0}
            elif key == "local_vio":
                result["local_vio"] = {"x": 0.0, "y": 0.0, "z": -1.5, "vx": 0.0, "vy": 0.0, "vz": 0.0}
            elif key == "depth":
                result["depth"] = {"meters": 1.5}
        return json.dumps(result)

    elif name == "control":
        action = args.get("action")
        mode = args.get("mode", "")
        if action == "arm":
            return json.dumps({"status": "armed", "message": "Vehicle armed successfully"})
        elif action == "disarm":
            return json.dumps({"status": "disarmed", "message": "Vehicle disarmed"})
        elif action == "set_mode":
            return json.dumps({"status": "ok", "mode": mode, "message": f"Mode set to {mode}"})
        return json.dumps({"status": "error", "message": f"Unknown action: {action}"})

    elif name == "navigate":
        frame = args.get("frame")
        return json.dumps({
            "status": "executing",
            "frame": frame,
            "waypoint": {k: v for k, v in args.items() if k != "frame"},
            "message": f"Navigation command accepted (frame={frame})",
        })

    return json.dumps({"status": "error", "message": f"Unknown tool: {name}"})


def build_tools() -> list[types.Tool]:
    return [
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="control",
                    description="Vehicle state control such as arming, disarming, or mode switching.",
                    parameters=genai.types.Schema(
                        type=genai.types.Type.OBJECT,
                        required=["action"],
                        properties={
                            "action": genai.types.Schema(
                                type=genai.types.Type.STRING,
                                enum=["arm", "disarm", "set_mode"],
                            ),
                            "mode": genai.types.Schema(
                                type=genai.types.Type.STRING,
                                enum=["MANUAL", "OFFBOARD", "LAND", "RTL"],
                            ),
                        },
                    ),
                ),
                types.FunctionDeclaration(
                    name="navigate",
                    description=(
                        "Move drone to a position using one coordinate frame. "
                        "global: lat/lon/alt. local: x,y,z (NED). body: dx,dy,dz relative offsets. "
                        "Optionally specify yaw in degrees."
                    ),
                    parameters=genai.types.Schema(
                        type=genai.types.Type.OBJECT,
                        required=["frame"],
                        properties={
                            "frame": genai.types.Schema(
                                type=genai.types.Type.STRING,
                                enum=["global", "local", "body"],
                            ),
                            "lat": genai.types.Schema(type=genai.types.Type.NUMBER),
                            "lon": genai.types.Schema(type=genai.types.Type.NUMBER),
                            "alt": genai.types.Schema(type=genai.types.Type.NUMBER),
                            "x":   genai.types.Schema(type=genai.types.Type.NUMBER),
                            "y":   genai.types.Schema(type=genai.types.Type.NUMBER),
                            "z":   genai.types.Schema(type=genai.types.Type.NUMBER),
                            "dx":  genai.types.Schema(type=genai.types.Type.NUMBER),
                            "dy":  genai.types.Schema(type=genai.types.Type.NUMBER),
                            "dz":  genai.types.Schema(type=genai.types.Type.NUMBER),
                            "yaw": genai.types.Schema(type=genai.types.Type.NUMBER),
                        },
                    ),
                ),
                types.FunctionDeclaration(
                    name="observe",
                    description=(
                        "Return drone state or sensor data for reasoning. "
                        "Always observe battery and GPS before arming or navigating."
                    ),
                    parameters=genai.types.Schema(
                        type=genai.types.Type.OBJECT,
                        required=["data"],
                        properties={
                            "data": genai.types.Schema(
                                type=genai.types.Type.ARRAY,
                                items=genai.types.Schema(
                                    type=genai.types.Type.STRING,
                                    enum=["battery", "gps", "heading", "airspeed", "local_vio", "depth"],
                                ),
                            ),
                        },
                    ),
                ),
            ]
        )
    ]


SYSTEM_PROMPT = """\
You are AerialAgent, an autonomous planner controlling a drone through a small set of tools.

Your goal is to safely achieve the mission objective by issuing a minimal, ordered sequence of tool calls.

━━━ Core Principles ━━━

Safety first
  • Never arm or navigate without first observing battery and GPS.
  • If battery < 20 % or GPS fix is not 3D, abort and land or RTL.
  • In any ambiguous or unsafe situation, prefer LAND or RTL.

Observe before acting
  • Always call observe(["battery","gps"]) before the first arm or navigate.
  • After navigation, verify position with observe(["local_vio"]) or observe(["gps"]).

Minimal control
  • Issue the smallest number of tool calls needed.
  • Do not repeat identical navigation commands.

━━━ Tools ━━━

control(action, [mode])
  arm | disarm | set_mode(MANUAL | OFFBOARD | LAND | RTL)

navigate(frame, ...)
  global  → lat, lon, alt
  local   → x, y, z  (NED metres)
  body    → dx, dy, dz  (relative offset metres)
  optional: yaw (degrees)

observe(data[])
  battery | gps | heading | airspeed | local_vio | depth

━━━ Execution order ━━━
  1. observe battery + GPS
  2. set_mode OFFBOARD
  3. arm
  4. navigate
  5. observe to verify
  6. disarm / LAND when done

━━━ Response policy ━━━
Think step by step internally, but your final output must be ONLY valid JSON:
{
  "tasks": [
    {
      "id": "<unique_id>",
      "tool": "<tool_name>",
      "args": { ... },
      "depends_on": ["<id>"]   // omit if no dependency
    }
  ]
}
No prose, no markdown fences, no extra keys.
If the mission is unclear or unsafe, output: {"tasks": [], "reason": "<explanation>"}
"""


def run_agent(mission: str, max_turns: int = 10) -> None:
    api_key = os.environ.get("GEMINI_API_KEY","AIzaSyCCIKOChwt4ywQPOdTf1iRbrh_547Ir1Mo")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")

    client = genai.Client(api_key=api_key)
    tools = build_tools()

    config = types.GenerateContentConfig(
        temperature=1,          # lower = more deterministic, better for planning
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=5120,  # enough headroom for multi-step reasoning
        ),
        tools=tools,
        system_instruction=[types.Part.from_text(text=SYSTEM_PROMPT)],
    )

    # Conversation history
    contents: list[types.Content] = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=mission)],
        )
    ]

    for turn in range(max_turns):
        print(f"\n{'-' * 60}")
        print(f"Turn {turn + 1}")
        print(f"{'-' * 60}")

        # Stream the response, printing thoughts and text as they arrive
        final_chunk = None
        in_thought = False
        for chunk in client.models.generate_content_stream(
            model="gemini-2.5-flash-lite",
            contents=contents,
            config=config,
        ):
            for part in (chunk.candidates[0].content.parts if chunk.candidates and chunk.candidates[0].content else []):
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
        print()  # newline after streamed text

        # The last chunk contains the fully-assembled candidate with all parts
        candidate = final_chunk.candidates[0]
        finish_reason = candidate.finish_reason
        parts = candidate.content.parts if candidate.content else []
        function_calls = [p.function_call for p in parts if p.function_call is not None]

        # Append model turn to history
        contents.append(types.Content(role="model", parts=parts))

        # No tool calls → model is done
        if not function_calls:
            print(f"\n[done] finish_reason={finish_reason}")
            break

        # Execute each tool call and collect results
        tool_response_parts: list[types.Part] = []
        for fc in function_calls:
            args = dict(fc.args) if fc.args else {}
            print(f"[tool call] {fc.name}({json.dumps(args, indent=2)})")

            result_str = execute_tool(fc.name, args)
            result_data = json.loads(result_str)
            print(f"[tool result] {json.dumps(result_data, indent=2)}")

            tool_response_parts.append(
                types.Part.from_function_response(
                    name=fc.name,
                    response=result_data,
                )
            )

        # Feed tool results back into the conversation
        contents.append(types.Content(role="user", parts=tool_response_parts))

    else:
        print(f"\n[warning] Reached max_turns={max_turns} without model finishing.")


if __name__ == "__main__":
    MISSION = (
        "Fly to waypoint at latitude 47.3980, longitude 8.5460, altitude 50 metres. "
        "Confirm position after arrival, then return to launch."
    )
    run_agent(MISSION)
