from state_machine import MissionState

# Each entry defines:
#   description:     human-readable purpose
#   args_schema:     expected arguments (type + optional)
#   permission_level: "read" | "write" | "critical"
#   allowed_states:  set of MissionState or None (= any state allowed)

TOOL_REGISTRY: dict = {
    "connect_drone": {
        "description": "Establish MAVLink connection to the drone.",
        "args_schema": {"connection_string": {"type": "string", "required": False}},
        "permission_level": "write",
        "allowed_states": {MissionState.IDLE},
    },
    "get_current_state": {
        "description": "Get flight mode, armed status, system status.",
        "args_schema": {},
        "permission_level": "read",
        "allowed_states": None,
    },
    "get_telemetry": {
        "description": "Fetch altitude, airspeed, groundspeed, heading.",
        "args_schema": {},
        "permission_level": "read",
        "allowed_states": None,
    },
    "get_position_str": {
        "description": "Get GPS position as human-readable string.",
        "args_schema": {},
        "permission_level": "read",
        "allowed_states": None,
    },
    "get_battery": {
        "description": "Check battery voltage, current, and percentage.",
        "args_schema": {},
        "permission_level": "read",
        "allowed_states": None,
    },
    "get_distance_to_str": {
        "description": "Get distance and bearing to a GPS target.",
        "args_schema": {
            "target_lat": {"type": "number", "required": True},
            "target_lon": {"type": "number", "required": True},
        },
        "permission_level": "read",
        "allowed_states": None,
    },
    "set_mode": {
        "description": "Change the drone flight mode.",
        "args_schema": {"mode": {"type": "string", "required": True}},
        "permission_level": "write",
        "allowed_states": {
            MissionState.CONNECTED, MissionState.ARMED,
            MissionState.HOVER, MissionState.FAILSAFE,
        },
    },
    "arm_drone": {
        "description": "Arm motors to prepare for flight.",
        "args_schema": {},
        "permission_level": "critical",
        "allowed_states": {MissionState.CONNECTED},
    },
    "disarm_drone": {
        "description": "Disarm motors after landing.",
        "args_schema": {},
        "permission_level": "critical",
        "allowed_states": {
            MissionState.IDLE, MissionState.CONNECTED,
            MissionState.LANDING, MissionState.FAILSAFE,
        },
    },
    "takeoff": {
        "description": "Take off to a specified altitude in meters.",
        "args_schema": {"altitude": {"type": "number", "required": True}},
        "permission_level": "critical",
        "allowed_states": {MissionState.ARMED},
    },
    "land": {
        "description": "Land at current location.",
        "args_schema": {},
        "permission_level": "critical",
        "allowed_states": {
            MissionState.HOVER, MissionState.ENROUTE,
            MissionState.RTL, MissionState.FAILSAFE,
        },
    },
    "return_to_launch": {
        "description": "Return to home/launch point and land.",
        "args_schema": {},
        "permission_level": "critical",
        "allowed_states": {MissionState.HOVER, MissionState.ENROUTE},
    },
    "goto_position": {
        "description": "Fly to a GPS coordinate and altitude.",
        "args_schema": {
            "lat": {"type": "number", "required": True},
            "lon": {"type": "number", "required": True},
            "alt": {"type": "number", "required": True},
        },
        "permission_level": "write",
        "allowed_states": {MissionState.HOVER, MissionState.ENROUTE},
    },
    "set_yaw": {
        "description": "Set yaw heading in degrees.",
        "args_schema": {
            "yaw_deg":  {"type": "number",  "required": True},
            "relative": {"type": "boolean", "required": False},
        },
        "permission_level": "write",
        "allowed_states": {MissionState.HOVER, MissionState.ENROUTE},
    },
    "set_speed": {
        "description": "Set target flight speed in m/s.",
        "args_schema": {"speed_ms": {"type": "number", "required": True}},
        "permission_level": "write",
        "allowed_states": {MissionState.HOVER, MissionState.ENROUTE},
    },
    "wait_altitude": {
        "description": "Wait until drone reaches target altitude.",
        "args_schema": {
            "target_alt": {"type": "number", "required": True},
            "tolerance":  {"type": "number", "required": False},
        },
        "permission_level": "read",
        "allowed_states": {MissionState.TAKEOFF, MissionState.HOVER},
    },
    "wait_arrival": {
        "description": "Wait until drone arrives at navigation target.",
        "args_schema": {"tolerance_m": {"type": "number", "required": False}},
        "permission_level": "read",
        "allowed_states": {MissionState.ENROUTE, MissionState.RTL},
    },
    "wait_time": {
        "description": "Pause for a specified number of seconds.",
        "args_schema": {"seconds": {"type": "number", "required": True}},
        "permission_level": "read",
        "allowed_states": None,
    },

    # ── Vision (OAK-D Lite) ───────────────────────────────────────────────────
    "vision_obstacle_check": {
        "description": (
            "Scan 5 horizontal sectors with OAK-D Lite stereo depth. "
            "Returns distance per sector and nearest obstacle. No NN required."
        ),
        "args_schema": {},
        "permission_level": "read",
        "allowed_states": None,
    },
    "vision_depth_snapshot": {
        "description": (
            "Capture a stereo depth frame and return a 3×3 grid of per-cell "
            "statistics plus a landing zone flatness assessment."
        ),
        "args_schema": {},
        "permission_level": "read",
        "allowed_states": None,
    },
    "vision_detect_objects": {
        "description": (
            "Run on-device YOLO on the OAK-D Lite VPU and return detected "
            "objects with 3D spatial coordinates (x, y, z in mm)."
        ),
        "args_schema": {
            "min_confidence": {"type": "number", "required": False},
        },
        "permission_level": "read",
        "allowed_states": None,
    },
}
