"""
VIO + SLAM integration for the OAK-D Lite running RTAB-Map on Myriad X.

Public surface:
  - VIOSLAMRunner   — asyncio background task that owns the DepthAI pipeline
  - VIOPose         — frozen dataclass: pose snapshot in VIO start frame
  - SLAMSnapshot    — frozen dataclass: occupancy grid summary
  - LiveOccupancyGrid — rolling 3D obstacle grid (pure NumPy)

Everything lives behind config.VIOSLAM_ENABLED.  When disabled (default), this
package imports cleanly with zero DepthAI overhead.
"""
