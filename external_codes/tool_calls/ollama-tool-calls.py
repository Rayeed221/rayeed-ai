import os
import json
import math
from ollama import chat
from pymavlink import mavutil

# ---------------------------------------------------------------------------
# MAVLink connection — set MAVLINK_CONNECTION to your vehicle endpoint,
# e.g. "udpin:0.0.0.0:14550", "tcp:127.0.0.1:5760", or "/dev/ttyUSB0,57600"
# ---------------------------------------------------------------------------

MAVLINK_CONNECTION = os.environ.get("MAVLINK_CONNECTION", "tcp:127.0.0.1:5760")
# OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:latest")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3.5:2b")

_mav: mavutil.mavfile | None = None

def get_mav() -> mavutil.mavfile:
    global _mav
    if _mav is None:
        _mav = mavutil.mavlink_connection(MAVLINK_CONNECTION)
        _mav.wait_heartbeat()
    return _mav


# ---------------------------------------------------------------------------
# MAVLink helpers
# ---------------------------------------------------------------------------

# Map mode name → ArduPilot custom_mode number (ArduCopter)
_COPTER_MODES = {
    "MANUAL":  0,   # STABILIZE used as manual-ish baseline
    "GUIDED":  4,
    "LAND":    9,
    "RTL":     6,
}

def _set_mode(mav: mavutil.mavfile, mode_name: str) -> dict:
    custom_mode = _COPTER_MODES.get(mode_name.upper())
    if custom_mode is None:
        return {"status": "error", "message": f"Unknown mode: {mode_name}"}
    mav.mav.command_long_send(
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0,                                         # confirmation
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        custom_mode,
        0, 0, 0, 0, 0,
    )
    ack = mav.recv_match(type="COMMAND_ACK", blocking=True, timeout=5)
    if ack and ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
        return {"status": "ok", "mode": mode_name, "message": f"Mode set to {mode_name}"}
    return {"status": "error", "message": f"Mode change rejected (ack={ack})"}


def _arm(mav: mavutil.mavfile) -> dict:
    mav.mav.command_long_send(
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,   # confirmation
        1,   # arm
        0, 0, 0, 0, 0, 0,
    )
    ack = mav.recv_match(type="COMMAND_ACK", blocking=True, timeout=5)
    if ack and ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
        return {"status": "armed", "message": "Vehicle armed successfully"}
    return {"status": "error", "message": f"Arm rejected (ack={ack})"}


def _disarm(mav: mavutil.mavfile) -> dict:
    mav.mav.command_long_send(
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,   # confirmation
        0,   # disarm
        0, 0, 0, 0, 0, 0,
    )
    ack = mav.recv_match(type="COMMAND_ACK", blocking=True, timeout=5)
    if ack and ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
        return {"status": "disarmed", "message": "Vehicle disarmed"}
    return {"status": "error", "message": f"Disarm rejected (ack={ack})"}


def _navigate_global(mav: mavutil.mavfile, lat: float, lon: float, alt: float, yaw: float | None) -> dict:
    """
    SET_POSITION_TARGET_GLOBAL_INT — moves to absolute GPS position in GUIDED mode.
    lat/lon supplied as degrees; multiplied to int×1e7 internally.
    yaw in degrees; NaN (ignored) when None.
    """
    type_mask = (
        0b0000_111111_000_111   # use pos + yaw, ignore vel/accel/yaw-rate
        if yaw is not None
        else 0b0000_111111_100_111  # also ignore yaw
    )
    yaw_val = math.radians(yaw) if yaw is not None else 0.0
    mav.mav.set_position_target_global_int_send(
        0,                                          # time_boot_ms
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        type_mask,
        int(lat * 1e7),                             # lat_int (deg × 1e7)
        int(lon * 1e7),                             # lon_int (deg × 1e7)
        alt,                                        # alt (m, relative to home)
        0, 0, 0,                                    # vx, vy, vz (ignored)
        0, 0, 0,                                    # afx, afy, afz (ignored)
        yaw_val, 0,                                 # yaw (rad), yaw_rate
    )
    return {
        "status": "executing",
        "frame": "global",
        "lat": lat, "lon": lon, "alt": alt,
        "message": "Global navigate command sent",
    }


def _navigate_local(mav: mavutil.mavfile, x: float, y: float, z: float, yaw: float | None) -> dict:
    """
    SET_POSITION_TARGET_LOCAL_NED with MAV_FRAME_LOCAL_NED.
    x=North, y=East, z=Down (NED convention, z negative = up).
    """
    type_mask = (
        0b0000_111111_000_111  # ignore velocity, accel, force, yaw-rate; use pos + yaw
        if yaw is not None
        else 0b0000_111111_100_111   # also ignore yaw
    )
    yaw_val = math.radians(yaw) if yaw is not None else 0.0
    mav.mav.set_position_target_local_ned_send(
        0,                                              # time_boot_ms (ignored)
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        type_mask,
        x, y, z,                                       # position (m)
        0, 0, 0,                                        # velocity (ignored)
        0, 0, 0,                                        # accel   (ignored)
        yaw_val, 0,                                     # yaw, yaw_rate
    )
    return {
        "status": "executing",
        "frame": "local",
        "x": x, "y": y, "z": z,
        "message": "Local NED navigate command sent",
    }


def _navigate_body(mav: mavutil.mavfile, dx: float, dy: float, dz: float, yaw: float | None) -> dict:
    """
    SET_POSITION_TARGET_LOCAL_NED with MAV_FRAME_BODY_OFFSET_NED.
    dx/dy/dz are offsets in the body (forward/right/down) frame.
    """
    type_mask = (
        0b0000_111111_000_111
        if yaw is not None
        else 0b0000_111111_100_111
    )
    yaw_val = math.radians(yaw) if yaw is not None else 0.0
    mav.mav.set_position_target_local_ned_send(
        0,
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
        type_mask,
        dx, dy, dz,
        0, 0, 0,
        0, 0, 0,
        yaw_val, 0,
    )
    return {
        "status": "executing",
        "frame": "body",
        "dx": dx, "dy": dy, "dz": dz,
        "message": "Body-offset navigate command sent",
    }


def _observe(mav: mavutil.mavfile, data_keys: list[str]) -> dict:
    result = {}

    # Fetch VFR_HUD once if either heading or airspeed is requested
    vfr_hud = None
    if "heading" in data_keys or "airspeed" in data_keys:
        vfr_hud = mav.recv_match(type="VFR_HUD", blocking=True, timeout=3)

    for key in data_keys:
        if key == "battery":
            msg = mav.recv_match(type="BATTERY_STATUS", blocking=True, timeout=3)
            if msg:
                voltage = msg.voltages[0] / 1000.0 if msg.voltages[0] != 65535 else None
                result["battery"] = {
                    "percent": msg.battery_remaining,
                    "voltage": voltage,
                }
            else:
                result["battery"] = {"error": "timeout"}

        elif key == "gps":
            msg = mav.recv_match(type="GLOBAL_POSITION_INT", blocking=True, timeout=3)
            if msg:
                fix_msg = mav.recv_match(type="GPS_RAW_INT", blocking=True, timeout=3)
                fix_type = fix_msg.fix_type if fix_msg else -1
                fix_str = {0: "NO_GPS", 1: "NO_FIX", 2: "2D", 3: "3D",
                           4: "DGPS", 5: "RTK_FLOAT", 6: "RTK_FIXED"}.get(fix_type, str(fix_type))
                result["gps"] = {
                    "fix": fix_str,
                    "satellites": fix_msg.satellites_visible if fix_msg else -1,
                    "lat": msg.lat / 1e7,
                    "lon": msg.lon / 1e7,
                    "alt": msg.alt / 1000.0,   # mm → m (AMSL)
                }
            else:
                result["gps"] = {"error": "timeout"}

        elif key == "heading":
            if vfr_hud:
                result["heading"] = {"degrees": vfr_hud.heading}
            else:
                result["heading"] = {"error": "timeout"}

        elif key == "airspeed":
            if vfr_hud:
                result["airspeed"] = {"ms": vfr_hud.airspeed}
            else:
                result["airspeed"] = {"error": "timeout"}

        elif key == "local_vio":
            msg = mav.recv_match(type="LOCAL_POSITION_NED", blocking=True, timeout=3)
            if msg:
                result["local_vio"] = {
                    "x": msg.x, "y": msg.y, "z": msg.z,
                    "vx": msg.vx, "vy": msg.vy, "vz": msg.vz,
                }
            else:
                result["local_vio"] = {"error": "timeout"}

        elif key == "depth":
            # DISTANCE_SENSOR downward-facing (MAV_SENSOR_ROTATION_PITCH_270)
            msg = mav.recv_match(type="DISTANCE_SENSOR", blocking=True, timeout=3)
            if msg:
                result["depth"] = {"meters": msg.current_distance / 100.0}  # cm → m
            else:
                result["depth"] = {"error": "timeout"}

    return result


# ---------------------------------------------------------------------------
# Tool executor
# ---------------------------------------------------------------------------

def execute_tool(name: str, args: dict) -> str:
    mav = get_mav()

    if name == "observe":
        data_keys = args.get("data", [])
        result = _observe(mav, data_keys)
        return json.dumps(result)

    elif name == "control":
        action = args.get("action")
        if action == "arm":
            return json.dumps(_arm(mav))
        elif action == "disarm":
            return json.dumps(_disarm(mav))
        elif action == "set_mode":
            return json.dumps(_set_mode(mav, args.get("mode", "")))
        return json.dumps({"status": "error", "message": f"Unknown action: {action}"})

    elif name == "navigate":
        frame = args.get("frame")
        yaw = args.get("yaw")
        if frame == "global":
            return json.dumps(_navigate_global(
                mav,
                lat=args["lat"], lon=args["lon"], alt=args["alt"],
                yaw=yaw,
            ))
        elif frame == "local":
            return json.dumps(_navigate_local(
                mav,
                x=args.get("x", 0.0), y=args.get("y", 0.0), z=args.get("z", 0.0),
                yaw=yaw,
            ))
        elif frame == "body":
            return json.dumps(_navigate_body(
                mav,
                dx=args.get("dx", 0.0), dy=args.get("dy", 0.0), dz=args.get("dz", 0.0),
                yaw=yaw,
            ))
        return json.dumps({"status": "error", "message": f"Unknown frame: {frame}"})

    return json.dumps({"status": "error", "message": f"Unknown tool: {name}"})


# ---------------------------------------------------------------------------
# Tool definitions — each description carries a per-tool usage snippet so
# the model knows exactly when and how to call it without reading the system
# prompt again.
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "control",
            "description": (
                "Vehicle state control. "
                "Call set_mode(GUIDED) before arm. "
                "Call arm and initialte TAKEOFF "
            ),
            "parameters": {
                "type": "object",
                "required": ["action"],
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["arm", "disarm", "set_mode"],
                        "description": "arm | disarm | set_mode",
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["MANUAL", "GUIDED", "LAND", "RTL"],
                        "description": "Required when action=set_mode.",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "navigate",
            "description": (
                "Move drone to a position. "
                "Use frame=global for absolute GPS targets (lat/lon/alt). "
                "Use frame=local for NED-relative field patterns (x/y/z metres). "
                "Use frame=body for small obstacle-avoidance offsets (dx/dy/dz). "
                "Always depends_on arm before first navigate."
            ),
            "parameters": {
                "type": "object",
                "required": ["frame"],
                "properties": {
                    "frame": {"type": "string", "enum": ["global", "local", "body"]},
                    "lat":  {"type": "number"},
                    "lon":  {"type": "number"},
                    "alt":  {"type": "number"},
                    "x":    {"type": "number"},
                    "y":    {"type": "number"},
                    "z":    {"type": "number"},
                    "dx":   {"type": "number"},
                    "dy":   {"type": "number"},
                    "dz":   {"type": "number"},
                    "yaw":  {"type": "number", "description": "Heading in degrees (optional)."},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "observe",
            "description": (
                "Read drone telemetry or sensor data. "
                "Always call with [battery,gps] before every arm or navigate. "
                "Call with [local_vio] or [gps] after every navigate to confirm position. "
                "Call with [airspeed,heading] to monitor dynamic conditions mid-flight."
            ),
            "parameters": {
                "type": "object",
                "required": ["data"],
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["battery", "gps", "heading", "airspeed", "local_vio", "depth"],
                        },
                        "description": "Sensors to read.",
                    },
                },
            },
        },
    },
]


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are AerialAgent, an autonomous context gathering agent for controlling a single drone to execute complex missions. 

Your goal is to achieve the mission objective by ordered sequence of tool calls generationds.
Reason concisely in 3 steps. First, define the user goal. Second, analyze the current drone state got from the user. Third, determine the next step where you need to make further thinking process.
Do not generate any prose or markdown, only JSON. Do not include any extra keys in the JSON, only "tasks" with a list of tool calls.

"""


# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

def run_agent(mission: str, max_turns: int = 10) -> None:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": mission},
    ]

    for turn in range(max_turns):
        print(f"\n{'-' * 60}")
        print(f"Turn {turn + 1}")
        print(f"{'-' * 60}")

        # Stream with thinking enabled
        stream = chat(
            model=OLLAMA_MODEL,
            messages=messages,
            tools=TOOLS,
            think=True,
            # think=True,
            options={"temperature": 0.1, "max_tokens":512, "n_ctx": 1024, "seed": 36},
            stream=True,
            
        )

        thinking_buf = ""
        content_buf  = ""
        tool_calls   = []
        in_thinking  = False

        for chunk in stream:
            msg = chunk.message

            if msg.thinking:
                if not in_thinking:
                    print("\n[thinking]", flush=True)
                    in_thinking = True
                print(msg.thinking, end="", flush=True)
                thinking_buf += msg.thinking

            if msg.content:
                if in_thinking:
                    print("\n[/thinking]\n", flush=True)
                    in_thinking = False
                print(msg.content, end="", flush=True)
                content_buf += msg.content

            if msg.tool_calls:
                tool_calls.extend(msg.tool_calls)

        if in_thinking:
            print("\n[/thinking]\n", flush=True)
        print()

        # Append full assistant turn to history (thinking + content + tool_calls)
        messages.append({
            "role": "assistant",
            "thinking": thinking_buf,
            "content": content_buf,
            "tool_calls": tool_calls,
        })

        # No tool calls → model is done
        if not tool_calls:
            print(f"\n[done] no further tool calls")
            break

        # Execute each tool and append results
        for tc in tool_calls:
            name = tc.function.name
            args = dict(tc.function.arguments) if tc.function.arguments else {}
            print(f"[tool call] {name}({json.dumps(args, indent=4)})")

            result_str = execute_tool(name, args)
            result_data = json.loads(result_str)
            print(f"[tool result] {json.dumps(result_data, indent=4)}")

            messages.append({
                "role": "tool",
                "tool_name": name,
                "content": result_str,
            })

    else:
        print(f"\n[warning] Reached max_turns={max_turns} without model finishing.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    MISSION = (
        "Conduct a precision solar farm inspection at lat 32.7157, lon -117.1611. Take off to 15m altitude and follow a zig-zag path across 12 predefined rows of panels (spacing 10m). Maintain a ground speed of exactly 1.5 m/s. If the heading deviates by more than 5 degrees due to wind, stop and hover for 5 seconds to stabilize. At the end of row 6, observe battery level; if battery is above 60%, continue to row 12, otherwise RTL immediately. Disarm 5 seconds after touchdown."
    )
    run_agent(MISSION)
