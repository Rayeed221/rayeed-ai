"""
RTAB-Map Parameter Configuration Comparison Tool
=================================================
Compare different parameter configurations side-by-side
"""

from typing import Dict

# Import configurations from the enhanced script
configs = {
    "Basic": {
        "RGBD/CreateOccupancyGrid": "true",
        "Grid/3D": "true",
        "Rtabmap/SaveWMState": "true"
    },

    "High Performance": {
        "Rtabmap/DetectionRate": "3.0",
        "Rtabmap/TimeThr": "0",
        "Rtabmap/MemoryThr": "200",
        "Rtabmap/LoopThr": "0.11",
        "RGBD/Enabled": "true",
        "RGBD/LinearUpdate": "0.1",
        "RGBD/AngularUpdate": "0.1",
        "RGBD/CreateOccupancyGrid": "true",
        "RGBD/LocalRadius": "10.0",
        "Vis/MaxFeatures": "800",
        "Grid/3D": "true",
        "Grid/CellSize": "0.05",
    },

    "Max Accuracy": {
        "Rtabmap/DetectionRate": "1.0",
        "Rtabmap/MemoryThr": "0",
        "RGBD/Enabled": "true",
        "RGBD/LinearUpdate": "0.05",
        "RGBD/AngularUpdate": "0.05",
        "RGBD/CreateOccupancyGrid": "true",
        "Vis/MaxFeatures": "1000",
        "Vis/MinInliers": "20",
        "Grid/3D": "true",
        "Grid/CellSize": "0.02",
    },

    "Minimal/Fast": {
        "RGBD/Enabled": "true",
        "RGBD/LinearUpdate": "0.3",
        "RGBD/CreateOccupancyGrid": "true",
        "Vis/MaxFeatures": "200",
        "Grid/3D": "false",
        "Rtabmap/DetectionRate": "1.0",
    },
}


def compare_configs():
    """Print side-by-side comparison of configurations"""

    # Collect all unique parameter names
    all_params = set()
    for config in configs.values():
        all_params.update(config.keys())
    all_params = sorted(all_params)

    # Print header
    print("\n" + "=" * 120)
    print("RTAB-Map Parameter Configuration Comparison")
    print("=" * 120)

    # Print column headers
    col_width = 25
    header = f"{'Parameter':<40}"
    for name in configs.keys():
        header += f"{name:<{col_width}}"
    print(header)
    print("-" * 120)

    # Print each parameter
    for param in all_params:
        row = f"{param:<40}"
        for config_name, config in configs.items():
            value = config.get(param, "-")
            row += f"{value:<{col_width}}"
        print(row)

    print("=" * 120)

    # Print summary statistics
    print("\nConfiguration Statistics:")
    print("-" * 60)
    for name, config in configs.items():
        print(f"{name:<20} {len(config):>3} parameters")

    print("\n")


def print_config_details():
    """Print detailed explanation of each configuration"""

    print("\n" + "=" * 80)
    print("Configuration Details")
    print("=" * 80)

    details = {
        "Basic": {
            "description": "Minimal configuration with basic SLAM functionality",
            "use_case": "Quick testing, minimal resource usage",
            "pros": ["Fastest", "Low memory", "Simple"],
            "cons": ["Limited accuracy", "No loop closure tuning"]
        },
        "High Performance": {
            "description": "Optimized for drones and fast-moving platforms",
            "use_case": "Outdoor navigation, drone mapping, dynamic environments",
            "pros": ["Good balance speed/accuracy", "Robust to fast motion", "Loop closure enabled"],
            "cons": ["Higher CPU usage", "More memory"]
        },
        "Max Accuracy": {
            "description": "Maximum accuracy with detailed mapping",
            "use_case": "Indoor mapping, slow movement, precise reconstruction",
            "pros": ["Highest accuracy", "Fine grid resolution", "More features"],
            "cons": ["Slowest", "High memory usage", "Not for real-time"]
        },
        "Minimal/Fast": {
            "description": "Ultra-fast with minimal features",
            "use_case": "Quick prototyping, resource-constrained systems",
            "pros": ["Fastest processing", "Lowest resource usage"],
            "cons": ["Poor accuracy", "No 3D grid", "Few features"]
        }
    }

    for name, info in details.items():
        print(f"\n{name}")
        print("-" * 40)
        print(f"Description: {info['description']}")
        print(f"Use Case:    {info['use_case']}")
        print(f"Pros:        {', '.join(info['pros'])}")
        print(f"Cons:        {', '.join(info['cons'])}")

    print("\n" + "=" * 80)


def explain_key_parameters():
    """Explain the most important parameters"""

    print("\n" + "=" * 80)
    print("Key Parameter Explanations")
    print("=" * 80)

    explanations = {
        "RGBD/LinearUpdate": {
            "desc": "Minimum linear movement (meters) to create a new node",
            "impact": "Lower = more nodes = better accuracy but slower",
            "range": "0.05 (indoor) to 0.3 (outdoor fast)",
            "default": "0.1"
        },
        "RGBD/AngularUpdate": {
            "desc": "Minimum rotation (radians) to create a new node",
            "impact": "Lower = more frequent updates during rotation",
            "range": "0.05 to 0.2 (0.1 rad ~ 6 degrees)",
            "default": "0.1"
        },
        "Vis/MaxFeatures": {
            "desc": "Maximum visual features to extract per image",
            "impact": "Higher = better matching but slower processing",
            "range": "200 (fast) to 1000 (accurate)",
            "default": "1000"
        },
        "Rtabmap/DetectionRate": {
            "desc": "How often (Hz) to process images for SLAM",
            "impact": "Higher = more loop closures but more CPU",
            "range": "1.0 (slow) to 3.0 (fast movement)",
            "default": "1.0"
        },
        "Grid/CellSize": {
            "desc": "Occupancy grid cell size in meters",
            "impact": "Smaller = finer detail but more memory/CPU",
            "range": "0.02 (fine) to 0.1 (coarse)",
            "default": "0.05"
        },
        "Rtabmap/MemoryThr": {
            "desc": "Max nodes in working memory (0 = unlimited)",
            "impact": "Prevents memory overflow in long missions",
            "range": "100-300 for drones, 0 for short missions",
            "default": "0"
        },
        "Kp/DetectorStrategy": {
            "desc": "Feature detector algorithm selection",
            "impact": "Different detectors work better in different environments",
            "options": "6=GFTT (indoor), 8=ORB (outdoor), 9=FAST (speed)",
            "default": "6"
        }
    }

    for param, info in explanations.items():
        print(f"\n{param}")
        print(f"  Description: {info['desc']}")
        print(f"  Impact:      {info['impact']}")
        if 'range' in info:
            print(f"  Range:       {info['range']}")
        if 'options' in info:
            print(f"  Options:     {info['options']}")
        print(f"  Default:     {info['default']}")

    print("\n" + "=" * 80)


def tuning_workflow():
    """Print recommended tuning workflow"""

    print("\n" + "=" * 80)
    print("Recommended Parameter Tuning Workflow")
    print("=" * 80)

    steps = [
        {
            "step": 1,
            "title": "Start with a preset",
            "action": "Choose High Performance or Max Accuracy based on your needs"
        },
        {
            "step": 2,
            "title": "Adjust movement thresholds",
            "action": "Tune RGBD/LinearUpdate and RGBD/AngularUpdate based on your platform speed"
        },
        {
            "step": 3,
            "title": "Optimize feature count",
            "action": "Start with Vis/MaxFeatures=500, increase if tracking fails, decrease if too slow"
        },
        {
            "step": 4,
            "title": "Set detection rate",
            "action": "Rtabmap/DetectionRate: 1 Hz for slow, 2-3 Hz for fast movement"
        },
        {
            "step": 5,
            "title": "Configure memory limits",
            "action": "Set Rtabmap/MemoryThr=200-300 for long missions to prevent RAM overflow"
        },
        {
            "step": 6,
            "title": "Tune grid resolution",
            "action": "Grid/CellSize: 0.05m is good default, 0.02m for detail, 0.1m for speed"
        },
        {
            "step": 7,
            "title": "Enable loop closure",
            "action": "Set RGBD/ProximityBySpace=true for loop closure detection"
        },
        {
            "step": 8,
            "title": "Test and iterate",
            "action": "Run on real data, monitor CPU/RAM usage, adjust as needed"
        }
    ]

    for step_info in steps:
        print(f"\nStep {step_info['step']}: {step_info['title']}")
        print(f"  -> {step_info['action']}")

    print("\n" + "=" * 80)


def main():
    """Main comparison function"""

    print("\nRTAB-Map Configuration Comparison Tool")

    # Show comparison table
    compare_configs()

    # Show detailed information
    print_config_details()

    # Explain key parameters
    explain_key_parameters()

    # Show tuning workflow
    tuning_workflow()

    # Print usage example
    print("\n" + "=" * 80)
    print("Usage Example")
    print("=" * 80)
    print("""
# In your code, choose a configuration:
from rtab_map_params_exploration import params_high_performance

slam = pipeline.create(dai.node.RTABMapSLAM)
slam.setParams(params_high_performance)

# Or create custom configuration by combining parameters:
custom_params = {
    "RGBD/Enabled": "true",
    "RGBD/LinearUpdate": "0.15",    # Custom value
    "Vis/MaxFeatures": "600",        # Custom value
    "Grid/3D": "true",
}
slam.setParams(custom_params)
""")
    print("=" * 80)


if __name__ == "__main__":
    main()
