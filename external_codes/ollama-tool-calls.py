import os
import json
import math
from ollama import chat
from pymavlink import mavutil

MAVLINK_CONNECTION = os.environ.get("MAVLINK_CONNECTION", "tcp:127.0.0.1:5760")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:latest")

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

_COPTER_MODES = {
    "STABILIZE": 0,
    "GUIDED":    4,
    "LOITER":    5,
    "RTL":       6,
    "LAND":      9,
    "POSHOLD":  16,
}

def _set_mode(mav: mavutil.mavfile, mode_name: str) -> dict:
    custom_mode = _COPTER_MODES.get(mode_name.upper())
    if custom_mode is None:
        return {"status": "error", "message": f"Unknown mode: {mode_name}. Valid: {list(_COPTER_MODES)}"}
    mav.mav.command_long_send(
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        custom_mode,
        0, 0, 0, 0, 0,
    )
    ack = mav.recv_match(type="COMMAND_ACK", blocking=True, timeout=5)
    if ack and ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
        return {"status": "ok", "mode": mode_name}
    return {"status": "error", "message": f"Mode change rejected (ack={ack})"}


def _arm(mav: mavutil.mavfile) -> dict:
    mav.mav.command_long_send(
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        1,   # param1: 1=arm
        0, 0, 0, 0, 0, 0,
    )
    ack = mav.recv_match(type="COMMAND_ACK", blocking=True, timeout=5)
    if ack and ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
        return {"status": "armed"}
    return {"status": "error", "message": f"Arm rejected (ack={ack})"}


def _disarm(mav: mavutil.mavfile) -> dict:
    mav.mav.command_long_send(
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        0,   # param1: 0=disarm
        0, 0, 0, 0, 0, 0,
    )
    ack = mav.recv_match(type="COMMAND_ACK", blocking=True, timeout=5)
    if ack and ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
        return {"status": "disarmed"}
    return {"status": "error", "message": f"Disarm rejected (ack={ack})"}


def _goto_gps(mav: mavutil.mavfile, lat: float, lon: float, alt: float, yaw: float | None) -> dict:
    """
    SET_POSITION_TARGET_GLOBAL_INT in MAV_FRAME_GLOBAL_RELATIVE_ALT_INT.
    type_mask bits: 1=ignore. Use position (bits 0-2 clear) + optional yaw.
    0x9F8 = ignore vel+accel+yaw_rate, use pos+yaw
    0xDF8 = ignore vel+accel+yaw+yaw_rate, use pos only
    """
    type_mask = 0x9F8 if yaw is not None else 0xDF8
    yaw_rad = math.radians(yaw) if yaw is not None else 0.0
    mav.mav.set_position_target_global_int_send(
        0,
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        type_mask,
        int(lat * 1e7),
        int(lon * 1e7),
        alt,
        0, 0, 0,   # vx, vy, vz (ignored)
        0, 0, 0,   # afx, afy, afz (ignored)
        yaw_rad, 0,
    )
    return {"status": "moving", "frame": "global", "lat": lat, "lon": lon, "alt": alt}


def _goto_local(mav: mavutil.mavfile, x: float, y: float, z: float, yaw: float | None) -> dict:
    """
    SET_POSITION_TARGET_LOCAL_NED in MAV_FRAME_LOCAL_NED.
    x=North(m), y=East(m), z=Down(m, use negative to climb).
    0x9F8 = ignore vel+accel+yaw_rate, use pos+yaw
    0xDF8 = ignore vel+accel+yaw+yaw_rate, use pos only
    """
    type_mask = 0x9F8 if yaw is not None else 0xDF8
    yaw_rad = math.radians(yaw) if yaw is not None else 0.0
    mav.mav.set_position_target_local_ned_send(
        0,
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        type_mask,
        x, y, z,
        0, 0, 0,   # velocity (ignored)
        0, 0, 0,   # accel (ignored)
        yaw_rad, 0,
    )
    return {"status": "moving", "frame": "local_ned", "x": x, "y": y, "z": z}


def _move_body(mav: mavutil.mavfile, dx: float, dy: float, dz: float) -> dict:
    """
    SET_POSITION_TARGET_LOCAL_NED in MAV_FRAME_BODY_OFFSET_NED.
    dx=forward(m), dy=right(m), dz=down(m, negative=up).
    0xDF8 = ignore vel+accel+yaw+yaw_rate, use pos only
    """
    mav.mav.set_position_target_local_ned_send(
        0,
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
        0xDF8,
        dx, dy, dz,
        0, 0, 0,
        0, 0, 0,
        0, 0,
    )
    return {"status": "moving", "frame": "body_offset", "dx": dx, "dy": dy, "dz": dz}


def _observe(mav: mavutil.mavfile, data_keys: list[str]) -> dict:
    result = {}

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
                    "alt_amsl": msg.alt / 1000.0,
                    "alt_rel": msg.relative_alt / 1000.0,
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
            msg = mav.recv_match(type="DISTANCE_SENSOR", blocking=True, timeout=3)
            if msg:
                result["depth"] = {"meters": msg.current_distance / 100.0}
            else:
                result["depth"] = {"error": "timeout"}

    return result


# ---------------------------------------------------------------------------
# Tool executor
# ---------------------------------------------------------------------------

def execute_tool(name: str, args: dict) -> str:
    mav = get_mav()

    if name == "observe":
        return json.dumps(_observe(mav, args.get("data", [])))

    elif name == "arm":
        return json.dumps(_arm(mav))

    elif name == "disarm":
        return json.dumps(_disarm(mav))

    elif name == "set_mode":
        return json.dumps(_set_mode(mav, args.get("mode", "")))

    elif name == "goto_gps":
        return json.dumps(_goto_gps(
            mav,
            lat=args["lat"], lon=args["lon"], alt=args["alt"],
            yaw=args.get("yaw"),
        ))

    elif name == "goto_local":
        return json.dumps(_goto_local(
            mav,
            x=args["x"], y=args["y"], z=args["z"],
            yaw=args.get("yaw"),
        ))

    elif name == "move_body":
        return json.dumps(_move_body(
            mav,
            dx=args["dx"], dy=args["dy"], dz=args["dz"],
        ))

    return json.dumps({"status": "error", "message": f"Unknown tool: {name}"})


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "arm",
            "description": "Arm the motors. Requires GUIDED mode. Call set_mode first.",
            "parameters": {"type": "object", "required": [], "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "disarm",
            "description": "Disarm the motors. Only call when on the ground after landing.",
            "parameters": {"type": "object", "required": [], "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_mode",
            "description": (
                "Set ArduCopter flight mode. "
                "GUIDED: autonomous position control (required before arm/navigate). "
                "RTL: return to launch and land. "
                "LAND: land at current position. "
                "LOITER: hold position. "
                "POSHOLD: manual position hold. "
                "STABILIZE: manual attitude control."
            ),
            "parameters": {
                "type": "object",
                "required": ["mode"],
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["GUIDED", "RTL", "LAND", "LOITER", "POSHOLD", "STABILIZE"],
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "goto_gps",
            "description": (
                "Fly to an absolute GPS coordinate. "
                "Requires GUIDED mode and armed. "
                "alt is meters relative to home (takeoff point)."
            ),
            "parameters": {
                "type": "object",
                "required": ["lat", "lon", "alt"],
                "properties": {
                    "lat": {"type": "number", "description": "Target latitude in decimal degrees."},
                    "lon": {"type": "number", "description": "Target longitude in decimal degrees."},
                    "alt": {"type": "number", "description": "Target altitude in meters above home."},
                    "yaw": {"type": "number", "description": "Target heading 0-359 degrees (optional)."},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "goto_local",
            "description": (
                "Fly to a NED position relative to the origin (arming point). "
                "x=North, y=East, z=Down (use negative z to climb, e.g. z=-10 = 10m altitude)."
            ),
            "parameters": {
                "type": "object",
                "required": ["x", "y", "z"],
                "properties": {
                    "x": {"type": "number", "description": "North offset in meters."},
                    "y": {"type": "number", "description": "East offset in meters."},
                    "z": {"type": "number", "description": "Down offset in meters (negative = up)."},
                    "yaw": {"type": "number", "description": "Target heading 0-359 degrees (optional)."},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "move_body",
            "description": (
                "Move relative to current position in body frame. "
                "dx=forward, dy=right, dz=down (negative dz = up). "
                "Useful for precise obstacle avoidance or fine adjustments."
            ),
            "parameters": {
                "type": "object",
                "required": ["dx", "dy", "dz"],
                "properties": {
                    "dx": {"type": "number", "description": "Forward offset in meters (negative = backward)."},
                    "dy": {"type": "number", "description": "Right offset in meters (negative = left)."},
                    "dz": {"type": "number", "description": "Down offset in meters (negative = up)."},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "observe",
            "description": (
                "Read drone telemetry. "
                "Always call observe(['battery','gps']) before arm or navigate. "
                "Call observe(['local_vio']) after navigation to confirm position. "
                "Call observe(['heading','airspeed']) to monitor flight conditions."
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
                        "description": "List of sensors to read.",
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
You are AerialAgent, an autonomous drone controller. Execute missions safely via tool calls.

SAFETY RULES (never skip):
1. observe(['battery','gps']) before every arm or navigate — abort if battery < 20% or GPS fix != 3D
2. set_mode('GUIDED') before arm
3. observe(['local_vio']) after every goto_* to confirm arrival

FLIGHT SEQUENCE:
  observe → set_mode(GUIDED) → arm → goto_gps/goto_local → observe → ... → set_mode(LAND) → disarm

NAVIGATION:
  goto_gps(lat, lon, alt)      — absolute GPS target
  goto_local(x, y, z)          — NED offset from origin (z negative = climb)
  move_body(dx, dy, dz)        — relative to current body frame

Think step by step, then issue only the next required tool call.
"""


# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

def run_agent(mission: str, max_turns: int = 20) -> None:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": mission},
    ]

    for turn in range(max_turns):
        print(f"\n{'-' * 60}")
        print(f"Turn {turn + 1}")
        print(f"{'-' * 60}")

        stream = chat(
            model=OLLAMA_MODEL,
            messages=messages,
            tools=TOOLS,
            think=False,
            options={"temperature": 1, "n_ctx": 2048, "seed": 36},
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

        messages.append({
            "role": "assistant",
            "thinking": thinking_buf,
            "content": content_buf,
            "tool_calls": tool_calls,
        })

        if not tool_calls:
            print(f"\n[done] no further tool calls")
            break

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
        "Conduct a precision solar farm inspection at lat 32.7157, lon -117.1611. "
        "Take off to 15m altitude and follow a zig-zag path across 12 predefined rows of panels (spacing 10m). "
        "Maintain a ground speed of exactly 1.5 m/s. If heading deviates by more than 5 degrees due to wind, "
        "stop and hover for 5 seconds to stabilize. At the end of row 6, observe battery level; "
        "if battery is above 60%, continue to row 12, otherwise RTL immediately. "
        "Disarm 5 seconds after touchdown."
    )
    run_agent(MISSION)
