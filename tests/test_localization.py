"""
Tests for the localization/ module.

All tests are purely mathematical / in-memory — no hardware, no depthai,
no GPS connection required.  Coverage:

  frame_transforms.py  — camera_to_frd, frd_to_ned, ned_to_global,
                          local_frame_summary, sector_to_frd
  pose_cache.py        — PoseCache update + get + is_valid
  localizer.py         — enrich_detection, enrich_sector, enrich_landing_zone,
                          global_observations
"""

import math
import time

import pytest

from localization.frame_transforms import (
    camera_to_frd,
    frd_to_ned,
    ned_to_global,
    local_frame_summary,
    sector_to_frd,
)
from localization.pose_cache import DronePose, PoseCache
from localization.localizer import GlobalObservation, Localizer


# ── Helpers ───────────────────────────────────────────────────────────────────

def _pose(lat=23.81, lon=90.41, alt_m=5.0, heading_deg=0.0) -> PoseCache:
    """Return a fully populated PoseCache."""
    pc = PoseCache()
    pc.update_telemetry(alt_m=alt_m, heading_deg=heading_deg)
    pc.update_position(lat=lat, lon=lon, alt_m=alt_m)
    return pc


def _approx(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) < tol


# ── camera_to_frd ─────────────────────────────────────────────────────────────

class TestCameraToFrd:
    def test_level_forward_axis_remap(self):
        """Camera z=forward → FRD F; x=right → R; y=down → D."""
        f, r, d = camera_to_frd(0, 0, 3000)
        assert _approx(f, 3.0)
        assert _approx(r, 0.0)
        assert _approx(d, 0.0)

    def test_level_right_displacement(self):
        f, r, d = camera_to_frd(500, 0, 2000)
        assert _approx(f, 2.0)
        assert _approx(r, 0.5)
        assert _approx(d, 0.0)

    def test_level_down_displacement(self):
        f, r, d = camera_to_frd(0, 300, 2000)
        assert _approx(f, 2.0)
        assert _approx(r, 0.0)
        assert _approx(d, 0.3)

    def test_zero_point(self):
        f, r, d = camera_to_frd(0, 0, 0)
        assert _approx(f, 0.0) and _approx(r, 0.0) and _approx(d, 0.0)

    def test_mm_to_metres_conversion(self):
        f, r, d = camera_to_frd(1000, 2000, 3000)
        assert _approx(f, 3.0)
        assert _approx(r, 1.0)
        assert _approx(d, 2.0)

    def test_yaw_90_rotates_forward_to_right(self):
        """Camera rotated 90° CW: what was forward in camera is now right in body."""
        f, r, d = camera_to_frd(0, 0, 1000, yaw_deg=90.0)
        # After 90° yaw: camera z maps to body R
        assert abs(f) < 1e-9
        assert _approx(r, 1.0, tol=1e-9)

    def test_yaw_minus_90_rotates_forward_to_left(self):
        f, r, d = camera_to_frd(0, 0, 1000, yaw_deg=-90.0)
        assert abs(f) < 1e-9
        assert _approx(r, -1.0, tol=1e-9)

    def test_pitch_90_maps_forward_to_down(self):
        """Camera tilted 90° nose-down: optical axis points down."""
        f, r, d = camera_to_frd(0, 0, 1000, pitch_deg=90.0)
        assert abs(f) < 1e-9
        assert _approx(d, 1.0, tol=1e-9)

    def test_negative_x_maps_to_negative_right(self):
        f, r, d = camera_to_frd(-400, 0, 2000)
        assert _approx(r, -0.4)

    def test_returns_float_tuple(self):
        result = camera_to_frd(100, 200, 3000)
        assert len(result) == 3
        assert all(isinstance(v, float) for v in result)


# ── frd_to_ned ────────────────────────────────────────────────────────────────

class TestFrdToNed:
    def test_north_heading_forward_is_north(self):
        """Heading 0° (North): drone forward → NED north."""
        n, e, d = frd_to_ned(2.0, 0.0, 0.0, heading_deg=0.0)
        assert _approx(n, 2.0)
        assert _approx(e, 0.0)

    def test_east_heading_forward_is_east(self):
        n, e, d = frd_to_ned(2.0, 0.0, 0.0, heading_deg=90.0)
        assert abs(n) < 1e-9
        assert _approx(e, 2.0, tol=1e-9)

    def test_south_heading_forward_is_south(self):
        n, e, d = frd_to_ned(2.0, 0.0, 0.0, heading_deg=180.0)
        assert _approx(n, -2.0, tol=1e-9)
        assert abs(e) < 1e-9

    def test_west_heading_forward_is_west(self):
        n, e, d = frd_to_ned(2.0, 0.0, 0.0, heading_deg=270.0)
        assert abs(n) < 1e-9
        assert _approx(e, -2.0, tol=1e-9)

    def test_down_axis_invariant_under_yaw(self):
        """Down displacement is unchanged by any heading."""
        for heading in [0, 45, 90, 135, 180, 270]:
            _, _, d = frd_to_ned(0.0, 0.0, 1.5, heading_deg=heading)
            assert _approx(d, 1.5)

    def test_northeast_heading_45(self):
        """Heading 45°: 1 m forward should give equal N and E components."""
        n, e, d = frd_to_ned(1.0, 0.0, 0.0, heading_deg=45.0)
        assert _approx(n, e, tol=1e-9)

    def test_right_with_north_heading_is_east(self):
        """Heading 0°: right displacement → east."""
        n, e, d = frd_to_ned(0.0, 1.0, 0.0, heading_deg=0.0)
        assert abs(n) < 1e-9
        assert _approx(e, 1.0)

    def test_returns_three_floats(self):
        result = frd_to_ned(1.0, 2.0, 3.0, 45.0)
        assert len(result) == 3


# ── ned_to_global ─────────────────────────────────────────────────────────────

class TestNedToGlobal:
    def test_zero_offset_returns_origin(self):
        lat, lon, alt = ned_to_global(0, 0, 0, 23.81, 90.41, 5.0)
        assert _approx(lat, 23.81)
        assert _approx(lon, 90.41)
        assert _approx(alt, 5.0)

    def test_north_offset_increases_lat(self):
        lat, lon, alt = ned_to_global(111_111, 0, 0, 0.0, 0.0, 0.0)
        assert _approx(lat, 1.0, tol=1e-4)

    def test_east_offset_increases_lon_at_equator(self):
        lat, lon, alt = ned_to_global(0, 111_111, 0, 0.0, 0.0, 0.0)
        assert _approx(lon, 1.0, tol=1e-4)

    def test_down_offset_decreases_alt(self):
        """NED down is positive downward → decreases altitude."""
        lat, lon, alt = ned_to_global(0, 0, 10.0, 23.81, 90.41, 50.0)
        assert _approx(alt, 40.0)

    def test_negative_down_increases_alt(self):
        lat, lon, alt = ned_to_global(0, 0, -5.0, 23.81, 90.41, 10.0)
        assert _approx(alt, 15.0)

    def test_small_offsets_reasonable(self):
        """1 m north of Dhaka should be ~9e-6 degrees north."""
        lat, lon, alt = ned_to_global(1.0, 0.0, 0.0, 23.81, 90.41, 5.0)
        delta_lat = lat - 23.81
        assert 8e-6 < delta_lat < 1e-5


# ── local_frame_summary ───────────────────────────────────────────────────────

class TestLocalFrameSummary:
    def test_forward_only(self):
        s = local_frame_summary(3.0, 0.0, 0.0)
        assert s["forward_m"] == 3.0
        assert s["right_m"] == 0.0
        assert s["down_m"] == 0.0
        assert s["distance_m"] == 3.0

    def test_3d_distance(self):
        s = local_frame_summary(3.0, 4.0, 0.0)
        assert s["distance_m"] == 5.0

    def test_negative_right_is_left(self):
        s = local_frame_summary(0.0, -1.5, 0.0)
        assert s["right_m"] == -1.5

    def test_rounding_to_2dp(self):
        s = local_frame_summary(1.0 / 3.0, 0.0, 0.0)
        assert s["forward_m"] == round(1.0 / 3.0, 2)

    def test_all_keys_present(self):
        s = local_frame_summary(1.0, 2.0, 3.0)
        assert set(s.keys()) == {"forward_m", "right_m", "down_m", "distance_m"}


# ── sector_to_frd ─────────────────────────────────────────────────────────────

class TestSectorToFrd:
    def test_center_sector_is_straight_ahead(self):
        f, r, d = sector_to_frd("center", 3.0)
        assert _approx(f, 3.0, tol=1e-9)
        assert abs(r) < 1e-9
        assert _approx(d, 0.0)

    def test_left_sector_has_negative_right(self):
        f, r, d = sector_to_frd("left", 2.0)
        assert r < 0  # left of centre

    def test_right_sector_has_positive_right(self):
        f, r, d = sector_to_frd("right", 2.0)
        assert r > 0  # right of centre

    def test_symmetry_left_right(self):
        """left and right sectors at same depth should be mirror images."""
        fl, rl, dl = sector_to_frd("left", 2.0)
        fr, rr, dr = sector_to_frd("right", 2.0)
        assert _approx(fl, fr, tol=1e-6)
        assert _approx(rl, -rr, tol=1e-6)

    def test_center_left_right_of_left(self):
        """center_left should have less rightward offset than right sector."""
        _, r_cl, _ = sector_to_frd("center_left", 2.0)
        _, r_r, _  = sector_to_frd("right", 2.0)
        assert r_cl < r_r

    def test_down_is_zero_for_all_sectors(self):
        for name in ["left", "center_left", "center", "center_right", "right"]:
            _, _, d = sector_to_frd(name, 3.0)
            assert _approx(d, 0.0)

    def test_unknown_sector_defaults_to_center(self):
        f, r, d = sector_to_frd("unknown_sector", 3.0)
        assert _approx(f, 3.0, tol=1e-9)
        assert abs(r) < 1e-9

    def test_zero_depth_returns_zeros(self):
        f, r, d = sector_to_frd("center", 0.0)
        assert _approx(f, 0.0) and _approx(r, 0.0)

    def test_custom_hfov(self):
        """Wider FOV → larger lateral displacement at same depth."""
        _, r_narrow, _ = sector_to_frd("right", 2.0, hfov_deg=60.0)
        _, r_wide,   _ = sector_to_frd("right", 2.0, hfov_deg=90.0)
        assert r_wide > r_narrow


# ── PoseCache ─────────────────────────────────────────────────────────────────

class TestPoseCache:
    def test_empty_cache_returns_none(self):
        pc = PoseCache()
        assert pc.get() is None

    def test_partial_update_returns_none(self):
        pc = PoseCache()
        pc.update_telemetry(alt_m=5.0, heading_deg=90.0)
        # No position yet — should still return None
        assert pc.get() is None

    def test_full_update_returns_pose(self):
        pc = _pose()
        pose = pc.get()
        assert pose is not None
        assert isinstance(pose, DronePose)

    def test_pose_fields_correct(self):
        pc = _pose(lat=23.81, lon=90.41, alt_m=10.0, heading_deg=45.0)
        pose = pc.get()
        assert pose.lat == 23.81
        assert pose.lon == 90.41
        assert pose.alt_m == 10.0
        assert pose.heading_deg == 45.0

    def test_telemetry_update_overwrites_heading(self):
        pc = _pose(heading_deg=0.0)
        pc.update_telemetry(alt_m=5.0, heading_deg=180.0)
        assert pc.get().heading_deg == 180.0

    def test_position_update_overwrites_lat_lon(self):
        pc = _pose(lat=0.0, lon=0.0)
        pc.update_position(lat=10.0, lon=20.0, alt_m=5.0)
        pose = pc.get()
        assert pose.lat == 10.0
        assert pose.lon == 20.0

    def test_is_valid_true_after_update(self):
        pc = _pose()
        assert pc.is_valid(max_age_s=10.0) is True

    def test_is_valid_false_when_stale(self):
        pc = PoseCache()
        pc._lat = 23.81
        pc._lon = 90.41
        pc._alt_m = 5.0
        pc._heading_deg = 0.0
        pc._last_update = time.monotonic() - 20.0  # 20 s ago
        assert pc.is_valid(max_age_s=10.0) is False

    def test_is_valid_false_when_empty(self):
        pc = PoseCache()
        assert pc.is_valid() is False

    def test_position_fills_alt_if_telemetry_missing(self):
        """update_position should fill alt_m if telemetry has not set it yet."""
        pc = PoseCache()
        pc.update_position(lat=23.81, lon=90.41, alt_m=7.5)
        pc.update_telemetry(alt_m=7.5, heading_deg=0.0)
        assert pc.get().alt_m == 7.5

    def test_thread_safe_concurrent_update(self):
        """Verify no crash under concurrent writes (basic smoke test)."""
        import threading
        pc = PoseCache()
        errors = []

        def writer():
            try:
                for _ in range(100):
                    pc.update_telemetry(5.0, 90.0)
                    pc.update_position(23.81, 90.41, 5.0)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=writer) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []


# ── Localizer ─────────────────────────────────────────────────────────────────

class TestLocalizer:
    def test_enrich_detection_adds_local_frame(self):
        loc = Localizer(_pose())
        det = {"label": 0, "label_name": "person", "confidence": 0.9,
               "x_mm": 0, "y_mm": 0, "z_mm": 3000}
        result = loc.enrich_detection(det)
        assert "local_frame" in result
        lf = result["local_frame"]
        assert set(lf.keys()) == {"forward_m", "right_m", "down_m", "distance_m"}

    def test_enrich_detection_forward_value(self):
        loc = Localizer(_pose())
        det = {"x_mm": 0, "y_mm": 0, "z_mm": 2500,
               "label": 2, "label_name": "car", "confidence": 0.8}
        result = loc.enrich_detection(det)
        assert result["local_frame"]["forward_m"] == 2.5

    def test_enrich_detection_preserves_original_fields(self):
        loc = Localizer(_pose())
        det = {"label": 0, "label_name": "person", "confidence": 0.9,
               "x_mm": 100, "y_mm": 50, "z_mm": 2000}
        result = loc.enrich_detection(det)
        assert result["label"] == 0
        assert result["confidence"] == 0.9
        assert result["x_mm"] == 100

    def test_enrich_detection_stores_global_observation(self):
        loc = Localizer(_pose(heading_deg=0.0))
        det = {"label": 0, "label_name": "person", "confidence": 0.85,
               "x_mm": 0, "y_mm": 0, "z_mm": 5000}
        loc.enrich_detection(det)
        obs = loc.global_observations()
        assert len(obs) == 1
        assert obs[0].label_name == "person"
        assert obs[0].confidence == 0.85

    def test_enrich_detection_no_global_when_no_pose(self):
        loc = Localizer(PoseCache())  # empty pose
        det = {"x_mm": 0, "y_mm": 0, "z_mm": 2000,
               "label": 0, "label_name": "person", "confidence": 0.9}
        result = loc.enrich_detection(det)
        assert "local_frame" in result  # still get local frame (uses heading=0)
        assert len(loc.global_observations()) == 0  # no global stored

    def test_enrich_sector_returns_expected_keys(self):
        loc = Localizer(_pose())
        result = loc.enrich_sector("center", 3.0)
        assert "distance_m" in result
        assert "local_frame" in result

    def test_enrich_sector_distance_m(self):
        loc = Localizer(_pose())
        result = loc.enrich_sector("center", 2.5)
        assert result["distance_m"] == 2.5

    def test_enrich_sector_center_local_frame(self):
        loc = Localizer(_pose())
        result = loc.enrich_sector("center", 3.0)
        lf = result["local_frame"]
        assert lf["forward_m"] == 3.0
        assert lf["right_m"] == 0.0

    def test_enrich_sector_left_has_negative_right(self):
        loc = Localizer(_pose())
        result = loc.enrich_sector("left", 2.0)
        assert result["local_frame"]["right_m"] < 0

    def test_enrich_sector_right_has_positive_right(self):
        loc = Localizer(_pose())
        result = loc.enrich_sector("right", 2.0)
        assert result["local_frame"]["right_m"] > 0

    def test_enrich_landing_zone_adds_local_frame(self):
        loc = Localizer(_pose())
        lz = {"safe": True, "reason": "flat", "std_m": 0.05,
              "coverage_pct": 95.0, "mean_m": 2.5}
        result = loc.enrich_landing_zone(lz)
        assert "local_frame" in result
        assert result["local_frame"]["forward_m"] == 2.5

    def test_enrich_landing_zone_preserves_safe_flag(self):
        loc = Localizer(_pose())
        lz = {"safe": False, "reason": "uneven", "std_m": 0.5,
              "coverage_pct": 80.0, "mean_m": 1.8}
        result = loc.enrich_landing_zone(lz)
        assert result["safe"] is False

    def test_global_observations_are_backend_only(self):
        """global_observations() returns list; nothing in enrich output."""
        loc = Localizer(_pose())
        det = {"x_mm": 0, "y_mm": 0, "z_mm": 1000,
               "label": 0, "label_name": "person", "confidence": 0.9}
        result = loc.enrich_detection(det)
        # Verify global coords NOT in the returned dict
        assert "lat" not in result
        assert "lon" not in result
        assert "global_frame" not in result

    def test_global_store_max_size(self):
        loc = Localizer(_pose(), global_store_size=5)
        det = {"x_mm": 0, "y_mm": 0, "z_mm": 1000,
               "label": 0, "label_name": "x", "confidence": 0.9}
        for _ in range(10):
            loc.enrich_detection(det)
        assert len(loc.global_observations()) == 5

    def test_global_observation_lat_lon_reasonable(self):
        """Object directly ahead at heading 0 should shift lat north."""
        pc = _pose(lat=23.81, lon=90.41, alt_m=5.0, heading_deg=0.0)
        loc = Localizer(pc)
        det = {"x_mm": 0, "y_mm": 0, "z_mm": 111_111_000,  # 111 km ahead
               "label": 0, "label_name": "far_object", "confidence": 0.9}
        loc.enrich_detection(det)
        obs = loc.global_observations()[0]
        # Should be ~1° north
        assert abs(obs.lat - 24.81) < 0.1
        assert abs(obs.lon - 90.41) < 0.01

    def test_camera_yaw_affects_local_frame(self):
        """90° camera yaw means what's forward in camera is right in body."""
        loc = Localizer(_pose(), camera_yaw_deg=90.0)
        det = {"x_mm": 0, "y_mm": 0, "z_mm": 1000,
               "label": 0, "label_name": "x", "confidence": 0.9}
        result = loc.enrich_detection(det)
        lf = result["local_frame"]
        assert abs(lf["forward_m"]) < 1e-9
        assert _approx(lf["right_m"], 1.0, tol=1e-9)

    def test_heading_affects_global_not_local(self):
        """Changing heading changes global coords but not local_frame."""
        det = {"x_mm": 0, "y_mm": 0, "z_mm": 2000,
               "label": 0, "label_name": "x", "confidence": 0.9}

        loc_north = Localizer(_pose(heading_deg=0.0))
        loc_east  = Localizer(_pose(heading_deg=90.0))

        r_north = loc_north.enrich_detection(det)
        r_east  = loc_east.enrich_detection(det)

        # Local frame should be identical regardless of heading
        assert r_north["local_frame"] == r_east["local_frame"]

        # Global coords should differ
        obs_north = loc_north.global_observations()[0]
        obs_east  = loc_east.global_observations()[0]
        assert obs_north.lat != obs_east.lat or obs_north.lon != obs_east.lon
