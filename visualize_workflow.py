import os
import subprocess
import base64

def generate_mermaid():
    mermaid_code = """
stateDiagram-v2
    [*] --> IDLE
    
    IDLE --> CONNECTED : connect_drone
    CONNECTED --> ARMED : arm_drone
    CONNECTED --> IDLE : disconnect
    
    ARMED --> TAKEOFF : takeoff
    ARMED --> CONNECTED : disarm
    
    TAKEOFF --> HOVER : wait_altitude
    TAKEOFF --> ENROUTE : goto_position
    
    HOVER --> ENROUTE : goto_position
    HOVER --> RTL : return_to_launch
    HOVER --> LANDING : land
    
    ENROUTE --> HOVER : wait_arrival
    ENROUTE --> RTL : return_to_launch
    ENROUTE --> LANDING : land
    
    RTL --> LANDING : wait_arrival
    LANDING --> IDLE : disarm_drone

    state FAILSAFE_FLOW {
        [*] --> Emergency_RTL
        Emergency_RTL --> Emergency_Land
        Emergency_Land --> Emergency_Disarm
        Emergency_Disarm --> IDLE
    }

    note right of FAILSAFE_FLOW : Triggered by SafetyPolicy:\\n- Battery Critical\\n- Telemetry Lost\\n- Max Retries
    
    %% Global Failsafe Transitions
    CONNECTED --> FAILSAFE_FLOW
    ARMED --> FAILSAFE_FLOW
    TAKEOFF --> FAILSAFE_FLOW
    HOVER --> FAILSAFE_FLOW
    ENROUTE --> FAILSAFE_FLOW
    RTL --> FAILSAFE_FLOW
    LANDING --> FAILSAFE_FLOW
    """
    return mermaid_code

def create_html(mermaid_code):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rayeed-AI Workflow Visualization</title>
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({{ 
                startOnLoad: true,
                theme: 'forest',
                securityLevel: 'loose'
            }});
        </script>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }}
            .card {{ background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 30px; width: 100%; max-width: 1000px; }}
            h1 {{ color: #1a73e8; margin-bottom: 10px; }}
            p {{ color: #5f6368; margin-bottom: 30px; }}
            .mermaid {{ display: flex; justify-content: center; }}
            .fallback {{ margin-top: 20px; font-size: 0.9em; color: #777; }}
            a {{ color: #1a73e8; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Rayeed-AI System Logic</h1>
            <p>Interactive state machine and safety workflow visualization.</p>
            <div class="mermaid">
                {mermaid_code}
            </div>
            <div class="fallback">
                If the diagram does not load, you can <a href="https://mermaid.live/edit#base64:{base64.b64encode(mermaid_code.encode()).decode()}" target="_blank">view it in the Mermaid Live Editor</a>.
            </div>
        </div>
    </body>
    </html>
    """
    file_path = "workflow_viz.html"
    with open(file_path, "w") as f:
        f.write(html_content)
    return os.path.abspath(file_path)

if __name__ == "__main__":
    mermaid = generate_mermaid()
    path = create_html(mermaid)
    print(f"Visualization generated at: {path}")
    
    # Attempt to open in browser (Android/Termux specific)
    try:
        subprocess.run(["termux-open", path], check=True)
        print("Opening in Chrome...")
    except Exception:
        # Fallback for other environments
        print(f"Please open the following file manually in your browser: file://{path}")
