from google.genai import types

# ─────────────────────────────────────────────────────────────────────────────
# Gemini Function Declarations
# These are the tool schemas exposed to the LLM.
# Low-level tools kept (Decision 3A) + high-level workflow triggers added.
# ─────────────────────────────────────────────────────────────────────────────

FUNCTION_DECLARATIONS = [
    # ── Read-only telemetry ───────────────────────────────────────────────────
    types.FunctionDeclaration(
        name="get_current_state",
        description="Retrieve the drone's current flight mode, armed status, and system status.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}, required=[]),
    ),
    types.FunctionDeclaration(
        name="get_telemetry",
        description="Fetch real-time telemetry: altitude, airspeed, groundspeed, heading.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}, required=[]),
    ),
    types.FunctionDeclaration(
        name="get_position_str",
        description="Get the drone's current GPS position as a human-readable string.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}, required=[]),
    ),
    types.FunctionDeclaration(
        name="get_battery",
        description="Check battery voltage, current draw, and remaining percentage.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}, required=[]),
    ),
    types.FunctionDeclaration(
        name="get_distance_to_str",
        description="Get distance and bearing to a GPS target coordinate.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "target_lat": types.Schema(type=types.Type.NUMBER, description="Target latitude"),
                "target_lon": types.Schema(type=types.Type.NUMBER, description="Target longitude"),
            },
            required=["target_lat", "target_lon"],
        ),
    ),
    # ── Connection ───────────────────────────────────────────────────────────
    types.FunctionDeclaration(
        name="connect_drone",
        description="Establish a MAVLink connection to the drone.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "connection_string": types.Schema(
                    type=types.Type.STRING,
                    description="MAVLink URI e.g. 'udp:127.0.0.1:14550'",
                )
            },
            required=[],
        ),
    ),
    # ── Mode + arming ─────────────────────────────────────────────────────────
    types.FunctionDeclaration(
        name="set_mode",
        description="Change the drone's flight mode (e.g. GUIDED, LOITER, AUTO, RTL).",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "mode": types.Schema(type=types.Type.STRING, description="Flight mode name"),
            },
            required=["mode"],
        ),
    ),
    types.FunctionDeclaration(
        name="arm_drone",
        description="Arm the drone's motors to prepare for flight.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}, required=[]),
    ),
    types.FunctionDeclaration(
        name="disarm_drone",
        description="Disarm the drone's motors after landing.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}, required=[]),
    ),
    # ── Flight commands ───────────────────────────────────────────────────────
    types.FunctionDeclaration(
        name="takeoff",
        description="Command the drone to take off to a specified altitude in meters.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "altitude": types.Schema(type=types.Type.NUMBER, description="Target altitude in meters"),
            },
            required=["altitude"],
        ),
    ),
    types.FunctionDeclaration(
        name="land",
        description="Command the drone to land at its current location.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}, required=[]),
    ),
    types.FunctionDeclaration(
        name="return_to_launch",
        description="Command the drone to return to its home/launch point and land.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}, required=[]),
    ),
    types.FunctionDeclaration(
        name="goto_position",
        description="Fly the drone to a specific GPS coordinate and altitude.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "lat": types.Schema(type=types.Type.NUMBER, description="Target latitude"),
                "lon": types.Schema(type=types.Type.NUMBER, description="Target longitude"),
                "alt": types.Schema(type=types.Type.NUMBER, description="Target altitude in meters"),
            },
            required=["lat", "lon", "alt"],
        ),
    ),
    types.FunctionDeclaration(
        name="set_yaw",
        description="Set the drone's yaw heading to a specific angle.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "yaw_deg":  types.Schema(type=types.Type.NUMBER,  description="Yaw in degrees (0–360)"),
                "relative": types.Schema(type=types.Type.BOOLEAN, description="True = relative to current heading"),
            },
            required=["yaw_deg"],
        ),
    ),
    types.FunctionDeclaration(
        name="set_speed",
        description="Set the drone's target flight speed in m/s.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "speed_ms": types.Schema(type=types.Type.NUMBER, description="Speed in meters per second"),
            },
            required=["speed_ms"],
        ),
    ),
    # ── Wait / polling ────────────────────────────────────────────────────────
    types.FunctionDeclaration(
        name="wait_altitude",
        description="Block until the drone reaches the target altitude within tolerance.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "target_alt": types.Schema(type=types.Type.NUMBER, description="Target altitude in meters"),
                "tolerance":  types.Schema(type=types.Type.NUMBER, description="Acceptable tolerance in meters"),
            },
            required=["target_alt"],
        ),
    ),
    types.FunctionDeclaration(
        name="wait_arrival",
        description="Block until the drone arrives at its navigation target.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "tolerance_m": types.Schema(type=types.Type.NUMBER, description="Arrival radius in meters"),
            },
            required=[],
        ),
    ),
    types.FunctionDeclaration(
        name="wait_time",
        description="Pause drone actions for a specified number of seconds.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "seconds": types.Schema(type=types.Type.NUMBER, description="Duration in seconds"),
            },
            required=["seconds"],
        ),
    ),
]
