"""
Real-pipeline tests for OakPipeline USB-drop / reconnect behaviour.

These tests do NOT mock OakPipeline — they exercise the actual class in
vision/oak_pipeline.py.  Since we have no OAK-D Lite in CI, we inject a
fake `depthai` module into sys.modules before importing OakPipeline.  The
fake implements just enough of the DepthAI v3 API surface (Pipeline, node
factories, output queues) for OakPipeline._build_graph() to run, and
gives us a hook to simulate a USB drop (pipeline.isRunning() -> False).

What is verified:
  - is_healthy() reflects the underlying pipeline.isRunning()
  - get_* accessors return None (not raise) when the pipeline is dead
  - reconnect() rebuilds and re-starts the pipeline after a drop
  - reconnect() gives up after _RECONNECT_MAX_ATTEMPTS failures
  - force_reconnect() is a public alias
"""

import sys
import types
import threading
import time
from typing import Any, List, Optional

import numpy as np
import pytest


# ── Fake depthai module ──────────────────────────────────────────────────────

class _FakeOutput:
    """Stand-in for a DepthAI v3 node output (chainable, has link/createOutputQueue)."""
    def __init__(self, name: str):
        self._name = name
        self._out_queue: Optional["_FakeQueue"] = None
        self.next_link = None  # .link(other) target

    def link(self, other) -> None:
        # In real v3, .link(target) wires this output into a target input
        # (attribute on the target node, e.g. stereo.left).  We only need
        # to record the connection so .createOutputQueue() on a downstream
        # output works.
        self.next_link = other

    def createOutputQueue(self, maxSize: int = 4, blocking: bool = False):
        q = _FakeQueue(maxSize=maxSize, blocking=blocking)
        self._out_queue = q
        return q


class _FakeQueue:
    """Stand-in for a depthai OutputQueue — supports tryGet()."""
    def __init__(self, maxSize: int = 4, blocking: bool = False):
        self.maxSize = maxSize
        self.blocking = blocking
        self._messages: List[Any] = []
        self.raise_on_get: Optional[Exception] = None

    def tryGet(self):
        if self.raise_on_get is not None:
            exc, self.raise_on_get = self.raise_on_get, None
            raise exc
        if not self._messages:
            return None
        return self._messages.pop(0)

    def put(self, msg: Any) -> None:
        self._messages.append(msg)

    def has(self) -> bool:
        return bool(self._messages)


class _FakeCameraNode:
    """Stand-in for dai.node.Camera — build() returns a node with requestOutput() etc."""
    def __init__(self):
        self.requested_outputs: List[tuple] = []

    def build(self, socket=None, sensorFps: int = 30):
        self.socket = socket
        self.fps = sensorFps
        return self

    def requestOutput(self, size, type=None):
        out = _FakeOutput(f"preview_{size}")
        self.requested_outputs.append((size, type))
        return out


class _FakeStereoNode:
    def __init__(self):
        self.left = _FakeOutput("stereo.left")
        self.right = _FakeOutput("stereo.right")
        self.depth = _FakeOutput("stereo.depth")
        self._profile = None
        self._lr_check = False
        self._subpixel = False
        self._depth_align = None

    def setDefaultProfilePreset(self, preset): self._profile = preset
    def setLeftRightCheck(self, v): self._lr_check = v
    def setSubpixel(self, v): self._subpixel = v
    def setDepthAlign(self, socket): self._depth_align = socket


class _FakeSLCNode:
    def __init__(self):
        self.inputDepth = _FakeOutput("slc.inputDepth")
        self.out = _FakeOutput("slc.out")
        self.initialConfig = self  # addROI/roi config lives here in real API

    def addROI(self, roi_cfg): pass


class _FakeSpatialDetectionNode:
    def __init__(self):
        self.input = _FakeOutput("yolo.input")
        self.inputDepth = _FakeOutput("yolo.inputDepth")
        self.out = _FakeOutput("yolo.out")


class _FakeImageManipNode:
    def __init__(self):
        self.inputImage = _FakeOutput("manip.inputImage")
        self.out = _FakeOutput("manip.out")
        self.initialConfig = self

    def setOutputSize(self, w, h): pass
    def setFrameType(self, t): pass


# Config-data sentinels
class _FakeRect:
    def __init__(self, a, b): self.a, self.b = a, b

class _FakePoint2f:
    def __init__(self, x, y): self.x, self.y = x, y

class _FakeSLCConfigData:
    def __init__(self):
        self.roi = None
        self.calculationAlgorithm = 0
        self.depthThresholds = self

    class _Thresholds:
        lowerThreshold = 200
        upperThreshold = 8000

    depthThresholds = _Thresholds()

class _FakeImgFrame:
    class Type:
        BGR888p = 0


class _FakePipeline:
    """Stand-in for dai.Pipeline — tracks isRunning, isBuilt, has start/stop/wait."""
    instances: List["_FakePipeline"] = []

    def __init__(self):
        self._running = False
        self._stopped = False
        self.nodes: List[Any] = []
        self.raise_on_start: Optional[Exception] = None
        self.start_count = 0
        _FakePipeline.instances.append(self)

    def create(self, factory):
        node = factory()
        self.nodes.append(node)
        return node

    def isBuilt(self): return True
    def isRunning(self): return self._running
    def start(self):
        if self.raise_on_start is not None:
            exc, self.raise_on_start = self.raise_on_start, None
            raise exc
        self._running = True
        self._stopped = False
        self.start_count += 1

    def stop(self):
        self._running = False
        self._stopped = True

    def wait(self): pass

    def setMaxReconnectionAttempts(self, *a, **kw): pass


def _install_fake_dai(monkeypatch, start_should_fail: bool = False) -> None:
    """Replace `depthai` in sys.modules with a fake that matches the v3 API
    surface used by OakPipeline._build_graph()."""
    dai = types.ModuleType("depthai")
    node_mod = types.ModuleType("depthai.node")

    node_mod.Camera = _FakeCameraNode
    node_mod.StereoDepth = _FakeStereoNode
    node_mod.SpatialLocationCalculator = _FakeSLCNode
    node_mod.SpatialDetectionNetwork = _FakeSpatialDetectionNode
    node_mod.ImageManip = _FakeImageManipNode

    # Static enum-like values used in the real pipeline
    class _CBS:
        CAM_A = "CAM_A"
        CAM_B = "CAM_B"
        CAM_C = "CAM_C"
    dai.CameraBoardSocket = _CBS

    class _StereoPreset:
        class PresetMode:
            DEFAULT = "DEFAULT"
            HIGH_DENSITY = "HIGH_DENSITY"
    node_mod.StereoDepth.PresetMode = _StereoPreset.PresetMode

    class _SLCAlgo:
        MEDIAN = 1
    dai.SpatialLocationCalculatorAlgorithm = _SLCAlgo

    dai.Rect = _FakeRect
    dai.Point2f = _FakePoint2f
    dai.SpatialLocationCalculatorConfigData = _FakeSLCConfigData
    dai.ImgFrame = _FakeImgFrame
    dai.Pipeline = _FakePipeline

    sys.modules["depthai"] = dai
    sys.modules["depthai.node"] = node_mod
    # Real depthai sets `dai.node` as an attribute pointing at the submodule
    dai.node = node_mod

    # Speed up reconnect backoff for tests (0.5/1/2/4/8s → 5/10/20/40/80ms)
    import vision.oak_pipeline as oak_mod
    monkeypatch.setattr(oak_mod, "_RECONNECT_BACKOFF_BASE_S", 0.005)
    monkeypatch.setattr(oak_mod, "_RECONNECT_BACKOFF_CAP_S", 0.08)
    monkeypatch.setattr(oak_mod, "_RECONNECT_MAX_ATTEMPTS", 3)


@pytest.fixture
def fake_dai(monkeypatch):
    _install_fake_dai(monkeypatch)
    yield


# ── Tests ────────────────────────────────────────────────────────────────────

def test_is_healthy_true_after_start(fake_dai):
    from vision.oak_pipeline import OakPipeline
    p = OakPipeline()
    p.start()
    try:
        assert p.is_healthy() is True
        assert p.available is True
    finally:
        p.stop()


def test_is_healthy_false_after_usb_drop(fake_dai):
    """Simulate an RPi brownout: pipeline.isRunning() flips to False."""
    from vision.oak_pipeline import OakPipeline
    p = OakPipeline()
    p.start()
    # Simulate USB drop
    p._pipeline._running = False
    assert p.is_healthy() is False
    p.stop()


def test_get_depth_frame_returns_none_when_unhealthy(fake_dai):
    from vision.oak_pipeline import OakPipeline
    p = OakPipeline()
    p.start()
    p._pipeline._running = False
    # Should NOT raise — returns None so VisionTool can surface a clean error
    assert p.get_depth_frame() is None
    p.stop()


def test_get_sector_distances_returns_none_when_unhealthy(fake_dai):
    from vision.oak_pipeline import OakPipeline
    p = OakPipeline()
    p.start()
    p._pipeline._running = False
    assert p.get_sector_distances() is None
    p.stop()


def test_get_detections_returns_none_when_unhealthy(fake_dai):
    from vision.oak_pipeline import OakPipeline
    p = OakPipeline(fps=10, blob_path="/fake/yolo.blob")
    p.start()
    p._pipeline._running = False
    assert p.get_detections() is None
    p.stop()


def test_reconnect_succeeds_after_drop(fake_dai):
    from vision.oak_pipeline import OakPipeline
    p = OakPipeline()
    p.start()
    old_pipeline = p._pipeline
    # USB drop
    old_pipeline._running = False
    # Disconnect callbacks fired
    disconnect_called = []
    reconnected_called = []
    p._on_disconnect = lambda: disconnect_called.append(True)
    p._on_reconnected = lambda: reconnected_called.append(True)

    assert p.reconnect() is True
    assert p.is_healthy() is True
    assert p._pipeline is not old_pipeline  # new pipeline object
    assert disconnect_called == [True]
    assert reconnected_called == [True]
    p.stop()


def test_reconnect_is_noop_when_already_healthy(fake_dai):
    from vision.oak_pipeline import OakPipeline
    p = OakPipeline()
    p.start()
    original = p._pipeline
    assert p.reconnect() is True
    assert p._pipeline is original  # unchanged
    p.stop()


def test_reconnect_gives_up_after_max_attempts(fake_dai):
    """All reconnect attempts fail (start() raises).  Should return False
    and mark the pipeline as not started — callers can then surface a hard
    failure to the user."""
    from vision.oak_pipeline import OakPipeline
    import vision.oak_pipeline as oak_mod

    p = OakPipeline()
    p.start()
    p._pipeline._running = False

    # Force every start() call to raise (simulating: cable unplugged, no device)
    def always_fail(self):
        raise RuntimeError("no device found (simulated USB unplug)")

    original_start = _FakePipeline.start
    _FakePipeline.start = always_fail
    try:
        start = time.monotonic()
        result = p.reconnect()
        elapsed = time.monotonic() - start
    finally:
        _FakePipeline.start = original_start

    assert result is False
    assert p.is_healthy() is False
    # Backoff was respected (we lowered it to 5/10/20 ms with 80 ms cap, 3 attempts)
    assert elapsed >= 0.005 + 0.010 + 0.020


def test_force_reconnect_is_public_alias(fake_dai):
    from vision.oak_pipeline import OakPipeline
    p = OakPipeline()
    p.start()
    p._pipeline._running = False
    assert p.force_reconnect() is True
    p.stop()


def test_queue_read_xlink_error_does_not_propagate(fake_dai):
    """An X_LINK_ERROR during tryGet() must NOT crash the caller; the
    pipeline should mark itself unhealthy and return None."""
    from vision.oak_pipeline import OakPipeline
    p = OakPipeline()
    p.start()
    # Inject a fake XLink error into the depth queue's tryGet
    p._q_depth.raise_on_get = RuntimeError(
        "Couldn't read data from stream: 'depth' (X_LINK_ERROR)"
    )
    assert p.get_depth_frame() is None
    assert p.is_healthy() is False
    p.stop()


def test_vision_tool_routes_through_real_pipeline(fake_dai):
    """End-to-end: real OakPipeline + real VisionTool, fake dai, no mocks."""
    from vision.oak_pipeline import OakPipeline
    from vision.vision_tool import VisionTool

    p = OakPipeline()
    p.start()
    try:
        # Inject a fake SLC message into the queue
        class _FakeSLCMsg:
            def getSpatialLocations(self):
                class _Loc:
                    def __init__(self, z): self.spatialCoordinates = type("C", (), {"z": z})()
                return [_Loc(2500.0), _Loc(1800.0), _Loc(900.0), _Loc(2200.0), _Loc(3000.0)]
        p._q_slc.put(_FakeSLCMsg())

        vt = VisionTool(p)
        result = vt.execute("vision_obstacle_check", {})
        assert "sectors" in result
        assert result["nearest_sector"] == "center"
        assert abs(result["nearest_distance_m"] - 0.9) < 0.01
        assert result["clear"] is False
    finally:
        p.stop()


def test_vision_tool_reconnects_on_unhealthy_pipeline(fake_dai):
    """If pipeline goes unhealthy between tool calls, VisionTool.execute()
    should attempt a reconnect before reporting failure."""
    from vision.oak_pipeline import OakPipeline
    from vision.vision_tool import VisionTool

    p = OakPipeline()
    p.start()
    vt = VisionTool(p)

    # Simulate a drop right before the tool is called
    p._pipeline._running = False

    result = vt.execute("vision_obstacle_check", {})
    # After reconnect the pipeline is healthy and the queue is empty, so
    # _wait_for times out and returns {"error": ...} — but NOT the
    # "reconnect failed" error.  We just want to confirm the reconnect
    # branch was taken (pipeline is healthy again).
    assert p.is_healthy() is True
    assert "error" in result  # empty queue after fresh start
    p.stop()
