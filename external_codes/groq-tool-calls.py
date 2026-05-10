from groq import Groq
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

DRONE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "arm",
            "description": "Arm the motors. Requires GUIDED mode first.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "disarm",
            "description": "Disarm the motors. Only when on the ground after landing.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_mode",
            "description": (
                "Set ArduCopter flight mode. "
                "GUIDED: autonomous control (required before arm/navigate). "
                "RTL: return to launch. LAND: land in place. "
                "LOITER: hold position. POSHOLD: manual hold. STABILIZE: manual."
            ),
            "parameters": {
                "type": "object",
                "required": ["mode"],
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["GUIDED", "RTL", "LAND", "LOITER", "POSHOLD", "STABILIZE"],
                        "description": "Target flight mode.",
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
                "Requires GUIDED mode and armed. alt is meters above home."
            ),
            "parameters": {
                "type": "object",
                "required": ["lat", "lon", "alt"],
                "properties": {
                    "lat":  {"type": "number", "description": "Latitude in decimal degrees."},
                    "lon":  {"type": "number", "description": "Longitude in decimal degrees."},
                    "alt":  {"type": "number", "description": "Altitude in meters above home."},
                    "yaw":  {"type": "number", "description": "Heading 0-359 degrees (optional)."},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "goto_local",
            "description": (
                "Fly to NED position relative to origin (arming point). "
                "x=North, y=East, z=Down. Use negative z to climb (z=-10 = 10m altitude)."
            ),
            "parameters": {
                "type": "object",
                "required": ["x", "y", "z"],
                "properties": {
                    "x": {"type": "number", "description": "North offset in meters."},
                    "y": {"type": "number", "description": "East offset in meters."},
                    "z": {"type": "number", "description": "Down offset in meters (negative = up)."},
                    "yaw": {"type": "number", "description": "Heading 0-359 degrees (optional)."},
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
                "dx=forward, dy=right, dz=down (negative = backward/left/up). "
                "Useful for fine adjustments and obstacle avoidance."
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
                "Call observe(['local_vio']) after navigation to confirm position."
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

load_dotenv()

DRONE_SYSTEM_PROMPT = """You are a drone mission planner. Your job is to translate a natural-language mission description into a precise, sequential Python mission script using ONLY the drone functions listed below.

## Output Rules

1. Output ONLY Python code blocks — no prose, no explanation outside the blocks.
2. Each logical phase of the mission is a SEPARATE ```python block with a markdown heading above it that names the phase.
   Heading format: `### <Step N>: <Phase Name>`
3. Every block must be self-contained and runnable in order. Assume each previous block already executed successfully.
4. Do NOT define helper functions, classes, or imports. The executor provides all functions directly.
5. Use only the function names listed below — no other Python APIs (no time.sleep, no print, no math, etc.).
6. For each function call, pass arguments as keyword arguments matching the parameter names exactly.
7. After every state-changing call (set_mode, arm_drone, takeoff, goto_position, etc.) always call get_telemetry() on the next line to confirm the new state.
8. If a mission requires waiting for altitude, always call wait_altitude() after takeoff() before any goto_position().
9. Always end the mission with either land() or return_to_launch(), then disarm_drone().

## Available Functions

connect_drone()
    Connect to the drone. Must be the very first call.

get_telemetry()
    Returns full state: position, attitude, battery, GPS, mode, armed status.

get_position()
    Returns lat, lon, alt, heading.

get_battery()
    Returns voltage, current, remaining_percent.

set_mode(mode: str)
    mode: "STABILIZE" | "GUIDED" | "LOITER" | "RTL" | "LAND" | "AUTO" | "ALT_HOLD" | "POSHOLD"
    Must set GUIDED before arming/takeoff/goto.

arm_drone()
    Arm motors. Requires GUIDED or STABILIZE mode.

disarm_drone()
    Disarm motors. Only when on the ground.

takeoff(altitude: float)
    altitude: meters above home. Requires armed + GUIDED mode.

wait_altitude(target_altitude: float, tolerance: float = 1.0, timeout: float = 30)
    Block until drone reaches target_altitude within tolerance.

goto_position(latitude: float, longitude: float, altitude: float)
    Fly to GPS coordinate. Requires GUIDED mode and airborne.

set_yaw(heading: float, relative: bool = False)
    heading: 0-360 degrees (0=North). relative=True means offset from current yaw.

set_speed(speed: float, speed_type: str = "groundspeed")
    speed_type: "groundspeed" | "airspeed"

get_distance_to(target_lat: float, target_lon: float)
    Returns distance in meters to target coordinate.

land()
    Land at current position.

return_to_launch()
    RTL — fly back to home and land.

## Example Output Format

### Step 1: Connect and Preflight Check
```python
connect_drone()
get_telemetry()
get_battery()
```

### Step 2: Arm and Takeoff
```python
set_mode(mode="GUIDED")
get_telemetry()
arm_drone()
get_telemetry()
takeoff(altitude=15)
wait_altitude(target_altitude=15, tolerance=1.0, timeout=30)
get_telemetry()
```

### Step 3: Navigate to Waypoint
```python
set_speed(speed=5)
goto_position(latitude=-35.3632621, longitude=149.1652374, altitude=15)
get_telemetry()
```

### Step 4: Land and Disarm
```python
land()
get_telemetry()
disarm_drone()
```

Now generate the mission plan for the following request:"""

def parse_args():
    parser = argparse.ArgumentParser(description="Generate text using Qwen3 via Groq API")
    parser.add_argument("prompt", nargs="?", help="The prompt to send to the model")
    parser.add_argument("-m", "--model", default="qwen/qwen3-32b", help="Model to use (default: qwen/qwen3-32b)")
    parser.add_argument("-t", "--temperature", type=float, default=1.0, help="Temperature (default: 1.0)")
    parser.add_argument("--max-tokens", type=int, default=5012, help="Max completion tokens (default: 5012)")
    parser.add_argument("-r", "--reasoning", default="default", choices=["default", "none", "low", "high"], help="Reasoning effort (default: default)")
    parser.add_argument("--no-log", action="store_true", help="Disable saving to log file")
    parser.add_argument("--drone", action="store_true", help="Use drone mission planner system prompt")
    return parser.parse_args()

def extract_python_blocks(text):
    """Return list of (name, code) tuples. Name is derived from the nearest preceding heading."""
    blocks = []
    # Find all headings and code fences with their positions
    heading_pattern = re.compile(r'^#{1,6}\s+\*{0,2}(.+?)\*{0,2}\s*$', re.MULTILINE)
    fence_pattern = re.compile(r'```python\n(.*?)```', re.DOTALL)

    headings = [(m.start(), m.group(1).strip()) for m in heading_pattern.finditer(text)]

    for i, fence in enumerate(fence_pattern.finditer(text)):
        code = fence.group(1).strip()
        fence_start = fence.start()
        # Find the closest heading that appears before this fence
        name = None
        for hpos, htitle in reversed(headings):
            if hpos < fence_start:
                name = htitle
                break
        if not name:
            name = f"block_{i + 1}"
        # Sanitize for filename
        safe_name = re.sub(r'[^\w\s-]', '', name).strip().lower()
        safe_name = re.sub(r'[\s]+', '_', safe_name)
        blocks.append((safe_name, code))
    return blocks

def main():
    args = parse_args()

    if not args.prompt:
        print("Error: prompt is required. Usage: python qwen3-generation.py \"your prompt here\"")
        return

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    script_dir = Path(__file__).parent
    log_dir = script_dir / "logs"
    if not args.no_log:
        log_dir.mkdir(exist_ok=True)

    messages = []
    if args.drone:
        messages.append({"role": "system", "content": DRONE_SYSTEM_PROMPT})
    messages.append({"role": "user", "content": args.prompt})

    completion = client.chat.completions.create(
        model=args.model,
        messages=messages,
        temperature=args.temperature,
        max_completion_tokens=args.max_tokens,
        reasoning_effort=args.reasoning,
        top_p=1,
        stream=True,
        stop=None,
        tools=DRONE_TOOLS if args.drone else None,
        tool_choice="auto" if args.drone else None,
    )

    think_content = ""
    main_content = ""
    in_think = False
    thinking_started = False

    THINK_COLOR = "\033[2;33m"   # dim yellow
    RESET_COLOR = "\033[0m"
    HEADER_COLOR = "\033[1;36m"  # bold cyan

    print(f"{HEADER_COLOR}=== THINKING ==={RESET_COLOR}")

    for chunk in completion:
        content = chunk.choices[0].delta.content or ""

        while content:
            if "<think>" in content and not in_think:
                before_think, _, after_think = content.partition("<think>")
                main_content += before_think
                content = after_think
                in_think = True
                thinking_started = True
            elif "</think>" in content and in_think:
                think_part, _, after_think = content.partition("</think>")
                think_content += think_part
                print(f"{THINK_COLOR}{think_part}{RESET_COLOR}", end="", flush=True)
                content = after_think
                in_think = False
                print(f"\n\n{HEADER_COLOR}=== RESPONSE ==={RESET_COLOR}")
            else:
                if in_think:
                    think_content += content
                    print(f"{THINK_COLOR}{content}{RESET_COLOR}", end="", flush=True)
                else:
                    main_content += content
                    print(content, end="", flush=True)
                break

    if not thinking_started:
        print("(no thinking)")
        print(f"\n{HEADER_COLOR}=== RESPONSE ==={RESET_COLOR}")
        print(main_content)

    code_blocks = extract_python_blocks(main_content)
    if code_blocks:
        CODE_COLOR = "\033[1;32m"   # bold green
        CODE_BG    = "\033[2;32m"   # dim green for code body
        print(f"\n{HEADER_COLOR}=== PYTHON CODE BLOCKS ({len(code_blocks)}) ==={RESET_COLOR}")
        for name, code in code_blocks:
            print(f"{CODE_COLOR}--- {name}.py ---{RESET_COLOR}")
            print(f"{CODE_BG}{code}{RESET_COLOR}")

    if not args.no_log:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        gen_dir = log_dir / f"generation_{timestamp}"
        gen_dir.mkdir(parents=True, exist_ok=True)

        # Save individual code block files
        saved_files = []
        seen_names = {}
        for name, code in code_blocks:
            count = seen_names.get(name, 0) + 1
            seen_names[name] = count
            filename = f"{name}.py" if count == 1 else f"{name}_{count}.py"
            py_file = gen_dir / filename
            py_file.write_text(code, encoding="utf-8")
            saved_files.append(filename)

        log_data = {
            "timestamp": datetime.now().isoformat(),
            "model": args.model,
            "input": args.prompt,
            "output": main_content,
            "thinking": think_content,
            "code_blocks": [{"file": f, "code": c} for (n, c), f in zip(code_blocks, saved_files)],
        }
        log_file = gen_dir / "generation.json"
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Saved to {gen_dir}/")
        for fname in saved_files:
            print(f"  {fname}")
        print(f"  generation.json")

if __name__ == "__main__":
    main()
