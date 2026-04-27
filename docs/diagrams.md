# RayeedAI System Architecture Diagrams

## 1. Five-Layer Pipeline Architecture

```mermaid
graph LR
    A["🎤 Voice Input<br/>Audio Interface"] --> B["🧠 Gemini Live API<br/>LLM Orchestration"]
    B --> C["📋 Planner<br/>Mission Planning"]
    C --> D["⚙️ Tool Dispatcher<br/>Safe Execution"]
    D --> E["🚁 Drone Adapter<br/>Backend"]
    E -->|Telemetry| B
    
    style A fill:#e1f5ff
    style B fill:#f3e5f5
    style C fill:#fff3e0
    style D fill:#f1f8e9
    style E fill:#fce4ec
```

## 2. Tool Execution Pipeline (7-Step Flow)

```mermaid
graph TD
    A["Tool Request"] --> B["1️⃣ Registry Check<br/>Tool exists?"]
    B -->|Yes| C["2️⃣ Safety Pre-Check<br/>Battery ≥15%<br/>Telemetry fresh <5s<br/>Altitude <120m<br/>Speed <15 m/s<br/>Retries <3"]
    C -->|Pass| D["3️⃣ Execute<br/>via Adapter<br/>10s timeout"]
    C -->|Fail| X1["❌ Return Error"]
    B -->|No| X2["❌ Tool Not Found"]
    D --> E["4️⃣ State Transition<br/>via State Machine"]
    E --> F["5️⃣ Update Monitors<br/>Telemetry, Battery,<br/>Altitude"]
    F --> G["6️⃣ Reset Retry<br/>Counter on Success"]
    G --> H["7️⃣ Return ToolResponse<br/>ok, tool, state, data,<br/>error, next_action"]
    
    style A fill:#e3f2fd
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#c8e6c9
    style E fill:#bbdefb
    style F fill:#bbdefb
    style G fill:#bbdefb
    style H fill:#c8e6c9
    style X1 fill:#ffcdd2
    style X2 fill:#ffcdd2
```

## 3. State Machine - All States & Transitions

```mermaid
graph TD
    IDLE["🔴 IDLE<br/>Initial State"]
    CONNECTED["🟡 CONNECTED<br/>Link Active"]
    ARMED["🟠 ARMED<br/>Motors Ready"]
    TAKEOFF["🟢 TAKEOFF<br/>Ascending"]
    ENROUTE["🔵 ENROUTE<br/>Flying to Target"]
    HOVER["🟣 HOVER<br/>Holding Position"]
    LANDING["🟤 LANDING<br/>Descending"]
    RTL["🟦 RTL<br/>Return to Launch"]
    FAILSAFE["🔴 FAILSAFE<br/>Emergency Mode"]
    
    IDLE -->|initialize| CONNECTED
    CONNECTED -->|arm| ARMED
    ARMED -->|takeoff| TAKEOFF
    TAKEOFF -->|reach_alt| ENROUTE
    ENROUTE -->|hover| HOVER
    ENROUTE -->|resume| ENROUTE
    HOVER -->|resume| ENROUTE
    HOVER -->|land| LANDING
    ENROUTE -->|land| LANDING
    LANDING -->|landed| IDLE
    ARMED -->|return_home| RTL
    ENROUTE -->|return_home| RTL
    HOVER -->|return_home| RTL
    RTL -->|landed| IDLE
    
    IDLE -.->|force_failsafe| FAILSAFE
    CONNECTED -.->|force_failsafe| FAILSAFE
    ARMED -.->|force_failsafe| FAILSAFE
    TAKEOFF -.->|force_failsafe| FAILSAFE
    ENROUTE -.->|force_failsafe| FAILSAFE
    HOVER -.->|force_failsafe| FAILSAFE
    LANDING -.->|force_failsafe| FAILSAFE
    RTL -.->|force_failsafe| FAILSAFE
    
    FAILSAFE -->|recovered| IDLE
    
    style IDLE fill:#ffcdd2
    style CONNECTED fill:#ffe082
    style ARMED fill:#ffb74d
    style TAKEOFF fill:#a5d6a7
    style ENROUTE fill:#64b5f6
    style HOVER fill:#ba68c8
    style LANDING fill:#bdb76b
    style RTL fill:#81c3d7
    style FAILSAFE fill:#ef5350
```

## 4. Background Subsystems - Async Task Architecture

```mermaid
graph TB
    subgraph SessionTasks["Session Tasks (Main Audio Loop)"]
        MIC["🎤 Mic Capture"]
        SEND["📤 Send to Gemini"]
        RCV["📥 Receive from Gemini"]
        PLAY["🔊 Playback"]
        TM["🔇 Turn Manager<br/>Mute/Unmute"]
    end
    
    subgraph BgTasks["Background Monitoring Tasks"]
        TR["📊 TelemetryReader"]
        BM["🔋 BatteryMonitor"]
        PM["📍 PositionMonitor"]
    end
    
    subgraph Persistence["Persistent Memory"]
        MM["📝 MissionMemory<br/>mission_state.json"]
        EM["🗺️ EnvironmentMemory<br/>environment.json"]
    end
    
    MIC --> SEND
    SEND --> RCV
    RCV --> PLAY
    TM -.->|control| MIC
    TM -.->|control| PLAY
    
    TR --> MM
    BM --> MM
    PM --> MM
    MM -.->|notify| SessionTasks
    EM -.->|waypoints/zones| SessionTasks
    
    style SessionTasks fill:#e8f5e9
    style BgTasks fill:#e3f2fd
    style Persistence fill:#f3e5f5
```

## 5. Planner Decision Engine - Outcomes

```mermaid
graph TD
    Input["Tool Execute<br/>Request"]
    
    Input --> Decision{"Planner<br/>Decision"}
    
    Decision -->|Success| CONTINUE["✅ CONTINUE<br/>Proceed to next step"]
    Decision -->|Wait for condition| WAIT["⏸️ WAIT<br/>Non-blocking wait<br/>Audio/Telemetry continues"]
    Decision -->|Transient failure| RETRY["🔄 RETRY<br/>Same step, inc counter<br/>Max 3 times"]
    Decision -->|New approach| REPLAN["📋 REPLAN<br/>Abort current, start new<br/>workflow toward RTH"]
    Decision -->|Unrecoverable| ABORT["🛑 ABORT<br/>Clean shutdown<br/>via RTH"]
    Decision -->|Critical danger| FAILSAFE["🚨 FAILSAFE<br/>Override LLM,<br/>force_failsafe"]
    
    style Input fill:#e3f2fd
    style Decision fill:#fff9c4
    style CONTINUE fill:#c8e6c9
    style WAIT fill:#bbdefb
    style RETRY fill:#ffe082
    style REPLAN fill:#ffb74d
    style ABORT fill:#ffccbc
    style FAILSAFE fill:#ef5350
```

## 6. Safety Policy Gates - Pre-Execution Checks

```mermaid
graph TD
    Tool["Tool Request"] --> BatCheck{"Battery<br/>≥ 15%?"}
    
    BatCheck -->|No| Failsafe1["🚨 FAILSAFE"]
    BatCheck -->|Yes| TelCheck{"Telemetry<br/>Fresh?<br/><5s"}
    
    TelCheck -->|No <10s| Wait1["⏸️ WAIT"]
    TelCheck -->|Yes| AltCheck{"Altitude<br/>< 120m?"}
    TelCheck -->|No ≥10s| Failsafe2["🚨 FAILSAFE"]
    
    AltCheck -->|No| Block1["❌ BLOCK"]
    AltCheck -->|Yes| SpdCheck{"Speed<br/>< 15 m/s?"}
    
    SpdCheck -->|No| Block2["❌ BLOCK"]
    SpdCheck -->|Yes| RetryCheck{"Retries<br/>< 3?"}
    
    RetryCheck -->|No| Block3["❌ BLOCK"]
    RetryCheck -->|Yes| Execute["✅ EXECUTE"]
    
    style Tool fill:#e3f2fd
    style BatCheck fill:#fff9c4
    style TelCheck fill:#fff9c4
    style AltCheck fill:#fff9c4
    style SpdCheck fill:#fff9c4
    style RetryCheck fill:#fff9c4
    style Execute fill:#c8e6c9
    style Failsafe1 fill:#ef5350
    style Failsafe2 fill:#ef5350
    style Block1 fill:#ffcdd2
    style Block2 fill:#ffcdd2
    style Block3 fill:#ffcdd2
    style Wait1 fill:#bbdefb
```

## 7. Workflow Execution Pattern

```mermaid
graph TD
    WF["Workflow<br/>e.g., Takeoff"]
    
    WF --> S1["Step 1<br/>execute_step"]
    S1 --> Disp1["Dispatcher.dispatch<br/>+ wait + retry + failsafe"]
    Disp1 -->|Success| S2["Step 2<br/>execute_step"]
    Disp1 -->|Failure| Abort1["Abort workflow<br/>Return False"]
    
    S2 --> Disp2["Dispatcher.dispatch<br/>+ wait + retry + failsafe"]
    Disp2 -->|Success| S3["Step 3<br/>execute_step"]
    Disp2 -->|Failure| Abort2["Abort workflow<br/>Return False"]
    
    S3 --> Disp3["Dispatcher.dispatch<br/>+ wait + retry + failsafe"]
    Disp3 -->|Success| Complete["✅ Complete<br/>Return True"]
    Disp3 -->|Failure| Abort3["Abort workflow<br/>Return False"]
    
    style WF fill:#fff3e0
    style S1 fill:#f1f8e9
    style S2 fill:#f1f8e9
    style S3 fill:#f1f8e9
    style Disp1 fill:#e1f5fe
    style Disp2 fill:#e1f5fe
    style Disp3 fill:#e1f5fe
    style Complete fill:#c8e6c9
    style Abort1 fill:#ffcdd2
    style Abort2 fill:#ffcdd2
    style Abort3 fill:#ffcdd2
```

## 8. Drone Backend Abstraction

```mermaid
graph LR
    Dispatcher["Tool Dispatcher<br/>Central Hub"]
    
    subgraph Interface["Base Adapter Interface<br/>adapters/base_adapter.py"]
        Execute["execute"]
        Handlers["_handle_arm_drone<br/>_handle_takeoff<br/>_handle_navigate<br/>... 18 tools"]
    end
    
    subgraph Sim["SimAdapter<br/>Default Backend"]
        SimExec["execute<br/>asyncio.to_thread"]
        SimHandlers["In-memory state<br/>Instant responses"]
    end
    
    subgraph MAV["MAVLinkAdapter<br/>Real Hardware"]
        MavExec["execute<br/>asyncio.to_thread"]
        MavHandlers["pymavlink calls<br/>Hardware control"]
    end
    
    Dispatcher -->|DRONE_BACKEND=sim| Sim
    Dispatcher -->|DRONE_BACKEND=mavlink| MAV
    
    Sim --> Interface
    MAV --> Interface
    
    style Dispatcher fill:#e3f2fd
    style Interface fill:#f3e5f5
    style Sim fill:#c8e6c9
    style MAV fill:#ffccbc
```

## 9. Complete System Architecture

```mermaid
graph TB
    subgraph Audio["Audio I/O Layer"]
        direction LR
        MIC["🎤 Mic Capture"]
        SPEAKER["🔊 Speaker Output"]
    end
    
    subgraph LLM["LLM Orchestration"]
        direction LR
        GEMINI["🧠 Gemini Live<br/>API Session"]
        SYSPROMPT["📋 System Prompt<br/>Bangla Instructions"]
        FUNCDECL["📝 Function<br/>Declarations"]
    end
    
    subgraph Planning["Mission Planning"]
        direction LR
        PLANNER["Planner<br/>Decision Engine"]
        WF["Workflows<br/>startup, takeoff,<br/>navigation, landing"]
    end
    
    subgraph Execution["Safe Execution Layer"]
        direction TB
        DISPATCH["Tool Dispatcher<br/>7-Step Pipeline"]
        SAFETY["Safety Policy<br/>Pre-Checks"]
        REGISTRY["Tool Registry<br/>18 Tools Metadata"]
        SM["State Machine<br/>9 States"]
    end
    
    subgraph Backend["Drone Backend"]
        direction LR
        ADAPTER["Adapter Interface<br/>base_adapter.py"]
        SIM["SimAdapter<br/>Memory-based"]
        MAV["MAVLinkAdapter<br/>Hardware"]
    end
    
    subgraph Monitoring["Background Monitoring"]
        direction LR
        TELEM["📊 TelemetryReader"]
        BATT["🔋 BatteryMonitor"]
        POS["📍 PositionMonitor"]
    end
    
    subgraph Memory["Persistent Memory"]
        direction LR
        MISSION["mission_state.json<br/>Tool + State"]
        ENV["environment.json<br/>Waypoints/Zones"]
    end
    
    Audio -->|PCM frames| LLM
    LLM -->|Command intent| Planning
    Planning -->|execute_step| Execution
    Execution -->|Tool request| DISPATCH
    DISPATCH -->|Check safety| SAFETY
    DISPATCH -->|Lookup metadata| REGISTRY
    DISPATCH -->|Transition| SM
    DISPATCH -->|Execute| Backend
    Backend --> ADAPTER
    ADAPTER --> SIM
    ADAPTER --> MAV
    Backend -->|Telemetry| Monitoring
    Monitoring -->|Update state| Memory
    Memory -->|Read state| LLM
    DISPATCH -->|Write state| Memory
    LLM -->|Audio response| Audio
    
    style Audio fill:#e1f5ff
    style LLM fill:#f3e5f5
    style Planning fill:#fff3e0
    style Execution fill:#f1f8e9
    style Backend fill:#fce4ec
    style Monitoring fill:#e0f2f1
    style Memory fill:#f1f8e9
```

## 10. Tool Execution with Adapter Handler Contract

```mermaid
graph TD
    A["dispatcher.dispatch<br/>tool_name, args"]
    A --> B["Lookup tool in<br/>tool_registry.py"]
    B --> C["Call adapter.execute<br/>tool_name, args"]
    C --> D["Wrapped in<br/>asyncio.to_thread"]
    D --> E["Handler executes<br/>_handle_tool_name<br/>SYNCHRONOUS"]
    E --> F{"Success?"}
    F -->|Yes| G["Return dict:<br/>level, status,<br/>position, error, ..."]
    F -->|No| H["Return dict:<br/>error: str"]
    G --> I["dispatcher reads<br/>specific fields<br/>from adapter contract"]
    H --> J["dispatcher increments<br/>retry counter"]
    I --> K["Update monitors<br/>& state machine"]
    J --> L["Return ToolResponse<br/>with error"]
    
    style A fill:#e3f2fd
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#c8e6c9
    style E fill:#c8e6c9
    style F fill:#fff9c4
    style G fill:#c8e6c9
    style H fill:#ffcdd2
    style I fill:#bbdefb
    style J fill:#bbdefb
    style K fill:#bbdefb
    style L fill:#ffcdd2
```

## 11. Voice Command Processing Flow

```mermaid
graph LR
    USER["👤 User<br/>Bangla Voice"]
    MIC["🎤 Capture PCM"]
    GEMINI["🧠 Gemini Live<br/>Transcribe + Understand"]
    INTENT["Intent<br/>arm, takeoff,<br/>navigate, land, etc"]
    PLANNER["📋 Planner<br/>Safety Decision"]
    DISPATCH["⚙️ Dispatcher<br/>Execute"]
    ADAPTER["🚁 Drone Backend"]
    TELEM["📊 Telemetry"]
    RESPONSE["🔊 Bangla Response<br/>via Speaker"]
    
    USER -->|Speak| MIC
    MIC -->|PCM bytes| GEMINI
    GEMINI -->|Parse tool call| INTENT
    INTENT -->|Check feasibility| PLANNER
    PLANNER -->|execute_step| DISPATCH
    DISPATCH -->|Send command| ADAPTER
    ADAPTER -->|Execute| TELEM
    TELEM -->|State update| GEMINI
    GEMINI -->|Generate response| RESPONSE
    
    style USER fill:#ffe082
    style MIC fill:#e1f5ff
    style GEMINI fill:#f3e5f5
    style INTENT fill:#fff3e0
    style PLANNER fill:#fff3e0
    style DISPATCH fill:#f1f8e9
    style ADAPTER fill:#fce4ec
    style TELEM fill:#e0f2f1
    style RESPONSE fill:#c8e6c9
```

## Key Attributes

- **Async-First**: All subsystems run as isolated asyncio tasks
- **Fault Isolation**: Session crash doesn't kill telemetry; telemetry crash doesn't kill audio
- **Safety Override**: Planner has authority to override LLM decisions
- **Retryable**: Up to 3 automatic retries on transient failures
- **Swappable Backend**: Switch between sim and real drone via env var only
- **Persistent State**: Tool + mission state saved after every tool call
- **Non-Blocking Waits**: Audio/telemetry continue during motor spin-up, altitude stabilization
