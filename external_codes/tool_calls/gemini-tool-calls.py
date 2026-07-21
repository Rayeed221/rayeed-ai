import os
import json
from google import genai
from google.genai import types


def execute_tool(name: str, args: dict) -> str:
    """Stub executor — replace with real MAVLink calls."""

    if name == "observe":
        data_keys = args.get("data", [])
        result = {}
        for key in data_keys:
            if key == "battery":
                result["battery"] = {"percent": 82, "voltage": 14.8}
            elif key == "gps":
                result["gps"] = {"fix": "3D", "satellites": 12, "lat": 47.3977, "lon": 8.5456, "alt_rel": 0.0, "alt_amsl": 120.0}
            elif key == "heading":
                result["heading"] = {"degrees": 270}
            elif key == "airspeed":
                result["airspeed"] = {"ms": 0.0}
            elif key == "local_vio":
                result["local_vio"] = {"x": 0.0, "y": 0.0, "z": -1.5, "vx": 0.0, "vy": 0.0, "vz": 0.0}
            elif key == "depth":
                result["depth"] = {"meters": 1.5}
        return json.dumps(result)

    elif name == "arm":
        return json.dumps({"status": "armed"})

    elif name == "disarm":
        return json.dumps({"status": "disarmed"})

    elif name == "set_mode":
        mode = args.get("mode", "")
        return json.dumps({"status": "ok", "mode": mode})

    elif name == "goto_gps":
        return json.dumps({
            "status": "moving",
            "frame": "global",
            "lat": args.get("lat"), "lon": args.get("lon"), "alt": args.get("alt"),
        })

    elif name == "goto_local":
        return json.dumps({
            "status": "moving",
            "frame": "local_ned",
            "x": args.get("x"), "y": args.get("y"), "z": args.get("z"),
        })

    elif name == "move_body":
        return json.dumps({
            "status": "moving",
            "frame": "body_offset",
            "dx": args.get("dx"), "dy": args.get("dy"), "dz": args.get("dz"),
        })

    return json.dumps({"status": "error", "message": f"Unknown tool: {name}"})


def build_tools() -> list[types.Tool]:
    S = genai.types.Schema
    T = genai.types.Type
    return [
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="arm",
                    description="Arm the motors. Requires GUIDED mode first.",
                    parameters=S(type=T.OBJECT, properties={}),
                ),
                types.FunctionDeclaration(
                    name="disarm",
                    description="Disarm the motors. Only when on the ground after landing.",
                    parameters=S(type=T.OBJECT, properties={}),
                ),
                types.FunctionDeclaration(
                    name="set_mode",
                    description=(
                        "Set ArduCopter flight mode. "
                        "GUIDED: autonomous control (required before arm/navigate). "
                        "RTL: return to launch. LAND: land in place. "
                        "LOITER: hold position. POSHOLD: manual hold. STABILIZE: manual."
                    ),
                    parameters=S(
                        type=T.OBJECT,
                        required=["mode"],
                        properties={
                            "mode": S(type=T.STRING, enum=["GUIDED", "RTL", "LAND", "LOITER", "POSHOLD", "STABILIZE"]),
                        },
                    ),
                ),
                types.FunctionDeclaration(
                    name="goto_gps",
                    description=(
                        "Fly to an absolute GPS coordinate. "
                        "Requires GUIDED mode and armed. alt is meters above home."
                    ),
                    parameters=S(
                        type=T.OBJECT,
                        required=["lat", "lon", "alt"],
                        properties={
                            "lat": S(type=T.NUMBER, description="Latitude in decimal degrees."),
                            "lon": S(type=T.NUMBER, description="Longitude in decimal degrees."),
                            "alt": S(type=T.NUMBER, description="Altitude in meters above home."),
                            "yaw": S(type=T.NUMBER, description="Heading 0-359 degrees (optional)."),
                        },
                    ),
                ),
                types.FunctionDeclaration(
                    name="goto_local",
                    description=(
                        "Fly to NED position relative to origin (arming point). "
                        "x=North, y=East, z=Down. Use negative z to climb (z=-10 = 10m altitude)."
                    ),
                    parameters=S(
                        type=T.OBJECT,
                        required=["x", "y", "z"],
                        properties={
                            "x": S(type=T.NUMBER, description="North offset in meters."),
                            "y": S(type=T.NUMBER, description="East offset in meters."),
                            "z": S(type=T.NUMBER, description="Down offset in meters (negative = up)."),
                            "yaw": S(type=T.NUMBER, description="Heading 0-359 degrees (optional)."),
                        },
                    ),
                ),
                types.FunctionDeclaration(
                    name="move_body",
                    description=(
                        "Move relative to current position in body frame. "
                        "dx=forward, dy=right, dz=down (negative = up). "
                        "Useful for fine adjustments and obstacle avoidance."
                    ),
                    parameters=S(
                        type=T.OBJECT,
                        required=["dx", "dy", "dz"],
                        properties={
                            "dx": S(type=T.NUMBER, description="Forward offset in meters (negative = backward)."),
                            "dy": S(type=T.NUMBER, description="Right offset in meters (negative = left)."),
                            "dz": S(type=T.NUMBER, description="Down offset in meters (negative = up)."),
                        },
                    ),
                ),
                types.FunctionDeclaration(
                    name="observe",
                    description=(
                        "Read drone telemetry. "
                        "Always call observe(['battery','gps']) before arm or navigate. "
                        "Call observe(['local_vio']) after navigation to confirm position."
                    ),
                    parameters=S(
                        type=T.OBJECT,
                        required=["data"],
                        properties={
                            "data": S(
                                type=T.ARRAY,
                                items=S(
                                    type=T.STRING,
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
You are AerialAgent, an autonomous drone planner (ArduCopter / ArduPilot).

SAFETY RULES (never skip):
  • observe(['battery','gps']) before every arm or navigate.
  • Abort if battery < 20% or GPS fix is not 3D.
  • observe(['local_vio']) after every goto_* to verify position.
  • Prefer set_mode(LAND) or set_mode(RTL) in any ambiguous or unsafe situation.

FLIGHT SEQUENCE:
  1. observe battery + GPS
  2. set_mode(GUIDED)
  3. arm
  4. goto_gps / goto_local / move_body
  5. observe to verify
  6. set_mode(LAND) or set_mode(RTL) when done
  7. disarm after touchdown

TOOLS:
  arm()                          — arm motors (GUIDED required)
  disarm()                       — disarm motors (ground only)
  set_mode(mode)                 — GUIDED | RTL | LAND | LOITER | POSHOLD | STABILIZE
  goto_gps(lat, lon, alt)        — fly to GPS coordinate (alt = m above home)
  goto_local(x, y, z)            — NED offset from origin (z negative = climb)
  move_body(dx, dy, dz)          — relative body-frame offset
  observe(data[])                — battery | gps | heading | airspeed | local_vio | depth

Issue the minimum tool calls needed. Do not repeat identical navigation commands.
"""


def run_agent(mission: str, max_turns: int = 10) -> None:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")

    client = genai.Client(api_key=api_key)
    tools = build_tools()

    config = types.GenerateContentConfig(
        temperature=1,
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=5120,
        ),
        tools=tools,
        system_instruction=[types.Part.from_text(text=SYSTEM_PROMPT)],
    )

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
        print()

        candidate = final_chunk.candidates[0]
        finish_reason = candidate.finish_reason
        parts = candidate.content.parts if candidate.content else []
        function_calls = [p.function_call for p in parts if p.function_call is not None]

        contents.append(types.Content(role="model", parts=parts))

        if not function_calls:
            print(f"\n[done] finish_reason={finish_reason}")
            break

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

        contents.append(types.Content(role="user", parts=tool_response_parts))

    else:
        print(f"\n[warning] Reached max_turns={max_turns} without model finishing.")


if __name__ == "__main__":
    MISSION = (
        "Fly to waypoint at latitude 47.3980, longitude 8.5460, altitude 50 metres. "
        "Confirm position after arrival, then return to launch."
    )
    run_agent(MISSION)
