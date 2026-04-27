"""
Pure coordinate frame transformation functions.

Frame conventions
-----------------
Camera frame (DepthAI OAK-D):
    x = right    y = down    z = forward (optical axis)    units: mm

Drone body FRD frame (what the AI sees):
    F = forward  R = right   D = down                      units: m

World NED frame (backend only, never sent to AI):
    N = north    E = east    D = down                      units: m (offset from origin)

Global frame (backend only):
    lat (decimal °)   lon (decimal °)   alt_m (AGL)

All functions are pure (no I/O, no state) — fully unit-testable.
"""

import math

# Sector centre positions in normalised image x-coordinates [0, 1].
# Derived from _SECTORS ROI dict in vision/oak_pipeline.py.
_SECTOR_CENTRE_X = {
    "left":         0.10,  # ROI centre of [0.00, 0.20]
    "center_left":  0.30,  # ROI centre of [0.20, 0.40]
    "center":       0.50,  # ROI centre of [0.40, 0.60]
    "center_right": 0.70,  # ROI centre of [0.60, 0.80]
    "right":        0.90,  # ROI centre of [0.80, 1.00]
}

# Radius of the Earth used for flat-earth NED→global approximation (metres)
_EARTH_R = 6_371_000.0


# ── Camera → FRD ─────────────────────────────────────────────────────────────

def camera_to_frd(
    x_mm: float,
    y_mm: float,
    z_mm: float,
    pitch_deg: float = 0.0,
    yaw_deg: float = 0.0,
) -> tuple[float, float, float]:
    """
    Convert a point from DepthAI camera frame to drone body FRD frame (metres).

    When the camera is mounted level and facing forward (pitch=0, yaw=0) the
    mapping is a pure axis remap:
        F = z_mm / 1000   (camera forward  → drone forward)
        R = x_mm / 1000   (camera right    → drone right)
        D = y_mm / 1000   (camera down     → drone down)

    pitch_deg > 0  camera tilted nose-down (common for downward-looking setups).
    yaw_deg   > 0  camera rotated clockwise from drone forward axis.

    Rotation order: yaw first (around camera Y/down axis), then pitch
    (around the resulting right axis).  This handles typical fixed-mount
    offsets on a multirotor.

    Args:
        x_mm:      camera-frame right displacement in mm
        y_mm:      camera-frame down displacement in mm
        z_mm:      camera-frame forward depth in mm
        pitch_deg: camera pitch offset from drone body (degrees, nose-down +)
        yaw_deg:   camera yaw offset from drone forward (degrees, CW +)

    Returns:
        (forward_m, right_m, down_m) in drone FRD frame, metres
    """
    # Convert to metres (camera frame)
    xc = x_mm / 1000.0
    yc = y_mm / 1000.0
    zc = z_mm / 1000.0

    # Apply yaw rotation around camera Y (down) axis
    if yaw_deg != 0.0:
        psi = math.radians(yaw_deg)
        cos_p, sin_p = math.cos(psi), math.sin(psi)
        xc, zc = xc * cos_p + zc * sin_p, -xc * sin_p + zc * cos_p

    # Apply pitch rotation around camera X (right) axis.
    # Positive pitch_deg = nose-down: optical axis (+z) rotates toward +y (down).
    # This is a negative rotation about the right-hand +x axis, so we use -theta.
    if pitch_deg != 0.0:
        theta = math.radians(pitch_deg)
        cos_t, sin_t = math.cos(theta), math.sin(theta)
        yc, zc = yc * cos_t + zc * sin_t, -yc * sin_t + zc * cos_t

    # Axis remap: camera (x=R, y=D, z=F) → FRD (F, R, D)
    return zc, xc, yc


# ── FRD → NED ────────────────────────────────────────────────────────────────

def frd_to_ned(
    f_m: float,
    r_m: float,
    d_m: float,
    heading_deg: float,
) -> tuple[float, float, float]:
    """
    Rotate a drone-body FRD vector to world NED frame using compass heading.

    Only yaw (heading) is applied — roll and pitch are assumed small for a
    hovering multirotor and are ignored.  This is the standard flat-earth
    navigation approximation.

    Args:
        f_m:         forward displacement in metres (FRD)
        r_m:         right displacement in metres (FRD)
        d_m:         down displacement in metres (FRD)
        heading_deg: drone compass heading, degrees 0–360 (0=North, 90=East)

    Returns:
        (north_m, east_m, down_m) in NED frame, metres
    """
    psi = math.radians(heading_deg)
    cos_h = math.cos(psi)
    sin_h = math.sin(psi)

    north_m =  f_m * cos_h - r_m * sin_h
    east_m  =  f_m * sin_h + r_m * cos_h
    down_m  =  d_m  # down is invariant under yaw rotation

    return north_m, east_m, down_m


# ── NED → Global ─────────────────────────────────────────────────────────────

def ned_to_global(
    n_m: float,
    e_m: float,
    d_m: float,
    origin_lat: float,
    origin_lon: float,
    origin_alt_m: float,
) -> tuple[float, float, float]:
    """
    Convert a NED offset (metres from drone) to absolute GPS coordinates.

    Uses the flat-earth / local tangent plane approximation.  Valid for
    offsets < ~10 km.  Longitude scaling accounts for latitude contraction.

    Args:
        n_m:          north offset in metres
        e_m:          east offset in metres
        d_m:          down offset in metres
        origin_lat:   drone latitude in decimal degrees
        origin_lon:   drone longitude in decimal degrees
        origin_alt_m: drone altitude AGL in metres

    Returns:
        (lat, lon, alt_m) of the observed point
    """
    metres_per_deg_lat = 111_111.0
    metres_per_deg_lon = 111_111.0 * math.cos(math.radians(origin_lat))

    lat = origin_lat + n_m / metres_per_deg_lat
    lon = origin_lon + e_m / max(metres_per_deg_lon, 1e-9)  # avoid /0 at poles
    alt = origin_alt_m - d_m  # NED down is negative altitude gain

    return lat, lon, alt


# ── Local frame summary (AI-facing) ──────────────────────────────────────────

def local_frame_summary(
    f_m: float,
    r_m: float,
    d_m: float,
) -> dict:
    """
    Build the ``local_frame`` dict that the AI receives.

    All values rounded to 2 decimal places (centimetre precision).

    Returns:
        {
            "forward_m":  float,  # positive = ahead of drone
            "right_m":    float,  # positive = drone's right, negative = left
            "down_m":     float,  # positive = below drone plane, negative = above
            "distance_m": float,  # Euclidean 3-D distance
        }
    """
    dist = math.sqrt(f_m ** 2 + r_m ** 2 + d_m ** 2)
    return {
        "forward_m":  round(f_m, 2),
        "right_m":    round(r_m, 2),
        "down_m":     round(d_m, 2),
        "distance_m": round(dist, 2),
    }


# ── Sector → FRD (obstacle check) ────────────────────────────────────────────

def sector_to_frd(
    sector_name: str,
    z_m: float,
    hfov_deg: float = 73.0,
) -> tuple[float, float, float]:
    """
    Approximate FRD coordinates for an obstacle-check sector.

    The SpatialLocationCalculator only returns depth (z_mm) per sector,
    not full x/y.  We reconstruct approximate horizontal position using each
    sector's known centre position within the camera FOV.

    Horizontal angle from optical axis:
        angle = (sector_centre_x − 0.5) × hfov_deg

    FRD from angle + depth (camera level assumed):
        F = z_m · cos(angle)
        R = z_m · sin(angle)
        D = 0.0

    Args:
        sector_name: one of "left", "center_left", "center", "center_right", "right"
        z_m:         depth reading from SpatialLocationCalculator in metres
        hfov_deg:    horizontal field of view of the camera (default 73° for OAK-D Lite)

    Returns:
        (forward_m, right_m, down_m) — approximate FRD position, metres
    """
    centre_x = _SECTOR_CENTRE_X.get(sector_name, 0.5)
    angle_deg = (centre_x - 0.5) * hfov_deg
    angle_rad = math.radians(angle_deg)

    f_m = z_m * math.cos(angle_rad)
    r_m = z_m * math.sin(angle_rad)
    d_m = 0.0  # sectors span the middle of the frame — assume horizontal

    return f_m, r_m, d_m
