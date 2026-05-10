from groq import Groq
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

### To Do updates:

DRONE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "arm",
            "description": "Arm motors. GUIDED mode required first.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "disarm",
            "description": "Disarm motors. Ground only.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_mode",
            "description": "Set flight mode. Use GUIDED before arm/navigate, RTL to return home, LAND to land.",
            "parameters": {
                "type": "object",
                "required": ["mode"],
                "properties": {
                    "mode": {"type": "string", "enum": ["GUIDED", "RTL", "LAND", "LOITER", "POSHOLD", "STABILIZE"]},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "goto_gps",
            "description": "Fly to GPS coordinate. alt = meters above home.",
            "parameters": {
                "type": "object",
                "required": ["lat", "lon", "alt"],
                "properties": {
                    "lat": {"type": "number"},
                    "lon": {"type": "number"},
                    "alt": {"type": "number"},
                    "yaw": {"type": "number", "description": "Heading degrees (optional)."},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "goto_local",
            "description": "Fly to NED offset from origin. x=North, y=East, z=Down (negative z = climb).",
            "parameters": {
                "type": "object",
                "required": ["x", "y", "z"],
                "properties": {
                    "x": {"type": "number"},
                    "y": {"type": "number"},
                    "z": {"type": "number"},
                    "yaw": {"type": "number", "description": "Heading degrees (optional)."},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "move_body",
            "description": "Move relative to current position. dx=fwd, dy=right, dz=down (neg=up).",
            "parameters": {
                "type": "object",
                "required": ["dx", "dy", "dz"],
                "properties": {
                    "dx": {"type": "number"},
                    "dy": {"type": "number"},
                    "dz": {"type": "number"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "observe",
            "description": "Read telemetry. Call with ['battery','gps'] before arm/navigate; ['local_vio'] after navigate.",
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

load_dotenv()

DRONE_SYSTEM_PROMPT = """You are a drone mission planner. Translate the mission into sequential Python code blocks.

Rules:
- Output ONLY ```python blocks with a `### Step N: Name` heading before each.
- No imports, no helpers, no prose. Use keyword args. No time.sleep/print/math.
- After every state-changing call add get_telemetry() on the next line.
- Call wait_altitude() after takeoff() before goto_position().
- End with land() or return_to_launch(), then disarm_drone().

Functions:
  connect_drone()
  get_telemetry()
  get_battery()
  get_position()
  set_mode(mode)           # GUIDED | LOITER | RTL | LAND | STABILIZE | POSHOLD
  arm_drone()
  disarm_drone()
  takeoff(altitude)
  wait_altitude(target_altitude, tolerance=1.0, timeout=30)
  goto_position(latitude, longitude, altitude)
  set_yaw(heading, relative=False)
  set_speed(speed, speed_type="groundspeed")
  get_distance_to(target_lat, target_lon)
  land()
  return_to_launch()

Generate the mission plan:"""

def parse_args():
    parser = argparse.ArgumentParser(description="Generate text using Qwen3 via Groq API")
    parser.add_argument("prompt", nargs="?", help="The prompt to send to the model")
    parser.add_argument("-m", "--model", default="qwen/qwen3-32b", help="Model to use (default: qwen/qwen3-32b)")
    parser.add_argument("-t", "--temperature", type=float, default=1.0, help="Temperature (default: 1.0)")
    parser.add_argument("--max-tokens", type=int, default=1024, help="Max completion tokens (default: 1024)")
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

    tool_kwargs = {"tools": DRONE_TOOLS, "tool_choice": "auto"} if args.drone else {}

    completion = client.chat.completions.create(
        model=args.model,
        messages=messages,
        temperature=args.temperature,
        max_completion_tokens=args.max_tokens,
        reasoning_effort=args.reasoning,
        top_p=1,
        stream=True,
        stop=None,
        **tool_kwargs,
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
