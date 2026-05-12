# `__init__.pyi` — Code Structure Map

> Auto-generated on **2026-03-15 04:05:07**
> Source: `C:\Users\User\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\depthai\node\__init__.pyi`
> Total lines: **25319**

---
## Table of Contents

1. [Imports](#imports)
2. [Global Variables](#global-variables)
3. [Functions](#functions)
4. [Classes](#classes)
   - [class ADatatype](#class-adatatype)
   - [class AprilTag](#class-apriltag)
   - [class AprilTagConfig](#class-apriltagconfig)
   - [class AprilTagProperties](#class-apriltagproperties)
   - [class AprilTags](#class-apriltags)
   - [class Asset](#class-asset)
   - [class AssetManager](#class-assetmanager)
   - [class BenchmarkReport](#class-benchmarkreport)
   - [class BlockPipelineEvent](#class-blockpipelineevent)
   - [class BoardConfig](#class-boardconfig)
   - [class Buffer](#class-buffer)
   - [class CalibrationHandler](#class-calibrationhandler)
   - [class CalibrationQuality](#class-calibrationquality)
   - [class CalibrationQualityData](#class-calibrationqualitydata)
   - [class CameraBoardSocket](#class-cameraboardsocket)
   - [class CameraControl](#class-cameracontrol)
   - [class CameraExposureOffset](#class-cameraexposureoffset)
   - [class CameraFeatures](#class-camerafeatures)
   - [class CameraImageOrientation](#class-cameraimageorientation)
   - [class CameraInfo](#class-camerainfo)
   - [class CameraModel](#class-cameramodel)
   - [class CameraSensorConfig](#class-camerasensorconfig)
   - [class CameraSensorType](#class-camerasensortype)
   - [class Capability](#class-capability)
   - [class CapabilityRangeFloat](#class-capabilityrangefloat)
   - [class CapabilityRangeFloatPair](#class-capabilityrangefloatpair)
   - [class CapabilityRangeUint](#class-capabilityrangeuint)
   - [class CapabilityRangeUintPair](#class-capabilityrangeuintpair)
   - [class ChipTemperature](#class-chiptemperature)
   - [class ChipTemperatureRVC4](#class-chiptemperaturervc4)
   - [class CircleAnnotation](#class-circleannotation)
   - [class Clock](#class-clock)
   - [class Color](#class-color)
   - [class ColorCameraProperties](#class-colorcameraproperties)
   - [class Colormap](#class-colormap)
   - [class CoverageData](#class-coveragedata)
   - [class CpuUsage](#class-cpuusage)
   - [class CrashDump](#class-crashdump)
   - [class DatatypeEnum](#class-datatypeenum)
   - [class DepthUnit](#class-depthunit)
   - [class DetectionNetworkType](#class-detectionnetworktype)
   - [class DetectionParserOptions](#class-detectionparseroptions)
   - [class DetectionParserProperties](#class-detectionparserproperties)
   - [class Device](#class-device)
   - [class DeviceBase](#class-devicebase)
   - [class DeviceBootloader](#class-devicebootloader)
   - [class DeviceDesc](#class-devicedesc)
   - [class DeviceInfo](#class-deviceinfo)
   - [class DeviceModelZoo](#class-devicemodelzoo)
   - [class DeviceNode](#class-devicenode)
   - [class DeviceNodeGroup](#class-devicenodegroup)
   - [class DynamicCalibrationControl](#class-dynamiccalibrationcontrol)
   - [class DynamicCalibrationProperties](#class-dynamiccalibrationproperties)
   - [class DynamicCalibrationResult](#class-dynamiccalibrationresult)
   - [class DynamicCalibrationResultData](#class-dynamiccalibrationresultdata)
   - [class EdgeDetectorConfig](#class-edgedetectorconfig)
   - [class EdgeDetectorConfigData](#class-edgedetectorconfigdata)
   - [class EdgeDetectorProperties](#class-edgedetectorproperties)
   - [class EepromData](#class-eepromdata)
   - [class EepromError](#class-eepromerror)
   - [class EncodedFrame](#class-encodedframe)
   - [class EventsManager](#class-eventsmanager)
   - [class Extrinsics](#class-extrinsics)
   - [class FeatureTrackerConfig](#class-featuretrackerconfig)
   - [class FeatureTrackerProperties](#class-featuretrackerproperties)
   - [class FileGroup](#class-filegroup)
   - [class FrameEvent](#class-frameevent)
   - [class GlobalProperties](#class-globalproperties)
   - [class HousingCoordinateSystem](#class-housingcoordinatesystem)
   - [class IMUData](#class-imudata)
   - [class IMUPacket](#class-imupacket)
   - [class IMUProperties](#class-imuproperties)
   - [class IMUReport](#class-imureport)
   - [class IMUReportAccelerometer](#class-imureportaccelerometer)
   - [class IMUReportGyroscope](#class-imureportgyroscope)
   - [class IMUReportMagneticField](#class-imureportmagneticfield)
   - [class IMUReportRotationVectorWAcc](#class-imureportrotationvectorwacc)
   - [class IMUSensor](#class-imusensor)
   - [class IMUSensorConfig](#class-imusensorconfig)
   - [class ImageAlignConfig](#class-imagealignconfig)
   - [class ImageAlignProperties](#class-imagealignproperties)
   - [class ImageFiltersConfig](#class-imagefiltersconfig)
   - [class ImageFiltersPresetMode](#class-imagefilterspresetmode)
   - [class ImageFiltersProperties](#class-imagefiltersproperties)
   - [class ImageManipConfig](#class-imagemanipconfig)
   - [class ImgAnnotation](#class-imgannotation)
   - [class ImgAnnotations](#class-imgannotations)
   - [class ImgDetection](#class-imgdetection)
   - [class ImgDetections](#class-imgdetections)
   - [class ImgFrame](#class-imgframe)
   - [class ImgFrameCapability](#class-imgframecapability)
   - [class ImgResizeMode](#class-imgresizemode)
   - [class ImgTransformation](#class-imgtransformation)
   - [class InputQueue](#class-inputqueue)
   - [class Interpolation](#class-interpolation)
   - [class Keypoint](#class-keypoint)
   - [class KeypointsList](#class-keypointslist)
   - [class LogLevel](#class-loglevel)
   - [class LogMessage](#class-logmessage)
   - [class MemoryInfo](#class-memoryinfo)
   - [class MessageDemuxProperties](#class-messagedemuxproperties)
   - [class MessageGroup](#class-messagegroup)
   - [class MessageQueue](#class-messagequeue)
   - [class ModelType](#class-modeltype)
   - [class MonoCameraProperties](#class-monocameraproperties)
   - [class NNArchive](#class-nnarchive)
   - [class NNArchiveConfigVersion](#class-nnarchiveconfigversion)
   - [class NNArchiveEntry](#class-nnarchiveentry)
   - [class NNArchiveOptions](#class-nnarchiveoptions)
   - [class NNArchiveVersionedConfig](#class-nnarchiveversionedconfig)
   - [class NNData](#class-nndata)
   - [class NNModelDescription](#class-nnmodeldescription)
   - [class NeuralDepthConfig](#class-neuraldepthconfig)
   - [class NeuralDepthProperties](#class-neuraldepthproperties)
   - [class NeuralNetworkProperties](#class-neuralnetworkproperties)
   - [class Node](#class-node)
   - [class NodeGroup](#class-nodegroup)
   - [class NodeState](#class-nodestate)
   - [class NodeStateApi](#class-nodestateapi)
   - [class NodesStateApi](#class-nodesstateapi)
   - [class ObjectTrackerProperties](#class-objecttrackerproperties)
   - [class OpenVINO](#class-openvino)
   - [class Pipeline](#class-pipeline)
   - [class PipelineEvent](#class-pipelineevent)
   - [class PipelineState](#class-pipelinestate)
   - [class PipelineStateApi](#class-pipelinestateapi)
   - [class Platform](#class-platform)
   - [class Point2f](#class-point2f)
   - [class Point3d](#class-point3d)
   - [class Point3f](#class-point3f)
   - [class Point3fRGBA](#class-point3frgba)
   - [class PointCloudConfig](#class-pointcloudconfig)
   - [class PointCloudData](#class-pointclouddata)
   - [class PointCloudProperties](#class-pointcloudproperties)
   - [class PointsAnnotation](#class-pointsannotation)
   - [class PointsAnnotationType](#class-pointsannotationtype)
   - [class ProcessorType](#class-processortype)
   - [class ProfilingData](#class-profilingdata)
   - [class Properties](#class-properties)
   - [class Quaterniond](#class-quaterniond)
   - [class RGBDData](#class-rgbddata)
   - [class RecordConfig](#class-recordconfig)
   - [class Rect](#class-rect)
   - [class RectificationProperties](#class-rectificationproperties)
   - [class RemoteConnection](#class-remoteconnection)
   - [class RotatedRect](#class-rotatedrect)
   - [class SPIInProperties](#class-spiinproperties)
   - [class SPIOutProperties](#class-spioutproperties)
   - [class ScriptProperties](#class-scriptproperties)
   - [class SerializationType](#class-serializationtype)
   - [class Size2f](#class-size2f)
   - [class SlugComponents](#class-slugcomponents)
   - [class SpatialDetectionNetworkProperties](#class-spatialdetectionnetworkproperties)
   - [class SpatialImgDetection](#class-spatialimgdetection)
   - [class SpatialImgDetections](#class-spatialimgdetections)
   - [class SpatialLocationCalculatorAlgorithm](#class-spatiallocationcalculatoralgorithm)
   - [class SpatialLocationCalculatorConfig](#class-spatiallocationcalculatorconfig)
   - [class SpatialLocationCalculatorConfigData](#class-spatiallocationcalculatorconfigdata)
   - [class SpatialLocationCalculatorConfigThresholds](#class-spatiallocationcalculatorconfigthresholds)
   - [class SpatialLocationCalculatorData](#class-spatiallocationcalculatordata)
   - [class SpatialLocationCalculatorProperties](#class-spatiallocationcalculatorproperties)
   - [class SpatialLocations](#class-spatiallocations)
   - [class StereoDepthConfig](#class-stereodepthconfig)
   - [class StereoDepthProperties](#class-stereodepthproperties)
   - [class StereoPair](#class-stereopair)
   - [class StereoRectification](#class-stereorectification)
   - [class SyncProperties](#class-syncproperties)
   - [class SystemInformation](#class-systeminformation)
   - [class SystemInformationRVC4](#class-systeminformationrvc4)
   - [class SystemLoggerProperties](#class-systemloggerproperties)
   - [class TensorInfo](#class-tensorinfo)
   - [class TextAnnotation](#class-textannotation)
   - [class ThermalAmbientParams](#class-thermalambientparams)
   - [class ThermalConfig](#class-thermalconfig)
   - [class ThermalFFCParams](#class-thermalffcparams)
   - [class ThermalGainMode](#class-thermalgainmode)
   - [class ThermalImageParams](#class-thermalimageparams)
   - [class ThermalProperties](#class-thermalproperties)
   - [class ThreadedNode](#class-threadednode)
   - [class Timestamp](#class-timestamp)
   - [class ToFConfig](#class-tofconfig)
   - [class ToFDepthConfidenceFilterConfig](#class-tofdepthconfidencefilterconfig)
   - [class ToFDepthConfidenceFilterProperties](#class-tofdepthconfidencefilterproperties)
   - [class ToFProperties](#class-tofproperties)
   - [class TrackedFeature](#class-trackedfeature)
   - [class TrackedFeatures](#class-trackedfeatures)
   - [class TrackerIdAssignmentPolicy](#class-trackeridassignmentpolicy)
   - [class TrackerType](#class-trackertype)
   - [class Tracklet](#class-tracklet)
   - [class Tracklets](#class-tracklets)
   - [class TransformData](#class-transformdata)
   - [class UVCProperties](#class-uvcproperties)
   - [class UsbSpeed](#class-usbspeed)
   - [class VectorCircleAnnotation](#class-vectorcircleannotation)
   - [class VectorColor](#class-vectorcolor)
   - [class VectorImgAnnotation](#class-vectorimgannotation)
   - [class VectorPoint2f](#class-vectorpoint2f)
   - [class VectorPointsAnnotation](#class-vectorpointsannotation)
   - [class VectorTextAnnotation](#class-vectortextannotation)
   - [class Version](#class-version)
   - [class VideoEncoderProperties](#class-videoencoderproperties)
   - [class VppConfig](#class-vppconfig)
   - [class VppProperties](#class-vppproperties)
   - [class WarpProperties](#class-warpproperties)
   - [class XLinkConnection](#class-xlinkconnection)
   - [class XLinkDeviceState](#class-xlinkdevicestate)
   - [class XLinkError](#class-xlinkerror)
   - [class XLinkError_t](#class-xlinkerror_t)
   - [class XLinkPlatform](#class-xlinkplatform)
   - [class XLinkProtocol](#class-xlinkprotocol)
   - [class XLinkReadError](#class-xlinkreaderror)
   - [class XLinkWriteError](#class-xlinkwriteerror)
   - [class YoloDecodingFamily](#class-yolodecodingfamily)
   - [class connectionInterface](#class-connectioninterface)
   - [class AprilTag](#class-apriltag)
   - [class BenchmarkIn](#class-benchmarkin)
   - [class BenchmarkOut](#class-benchmarkout)
   - [class Camera](#class-camera)
   - [class ColorCamera](#class-colorcamera)
   - [class DetectionNetwork](#class-detectionnetwork)
   - [class DetectionParser](#class-detectionparser)
   - [class DynamicCalibration](#class-dynamiccalibration)
   - [class EdgeDetector](#class-edgedetector)
   - [class FeatureTracker](#class-featuretracker)
   - [class HostNode](#class-hostnode)
   - [class IMU](#class-imu)
   - [class ImageAlign](#class-imagealign)
   - [class ImageFilters](#class-imagefilters)
   - [class ImageManip](#class-imagemanip)
   - [class MessageDemux](#class-messagedemux)
   - [class MonoCamera](#class-monocamera)
   - [class NeuralAssistedStereo](#class-neuralassistedstereo)
   - [class NeuralDepth](#class-neuraldepth)
   - [class NeuralNetwork](#class-neuralnetwork)
   - [class ObjectTracker](#class-objecttracker)
   - [class PointCloud](#class-pointcloud)
   - [class RGBD](#class-rgbd)
   - [class RTABMapSLAM](#class-rtabmapslam)
   - [class RTABMapVIO](#class-rtabmapvio)
   - [class RecordMetadataOnly](#class-recordmetadataonly)
   - [class RecordVideo](#class-recordvideo)
   - [class Rectification](#class-rectification)
   - [class ReplayMetadataOnly](#class-replaymetadataonly)
   - [class ReplayVideo](#class-replayvideo)
   - [class SPIIn](#class-spiin)
   - [class SPIOut](#class-spiout)
   - [class Script](#class-script)
   - [class SpatialDetectionNetwork](#class-spatialdetectionnetwork)
   - [class SpatialLocationCalculator](#class-spatiallocationcalculator)
   - [class StereoDepth](#class-stereodepth)
   - [class Sync](#class-sync)
   - [class SystemLogger](#class-systemlogger)
   - [class Thermal](#class-thermal)
   - [class ThreadedHostNode](#class-threadedhostnode)
   - [class ToF](#class-tof)
   - [class ToFBase](#class-tofbase)
   - [class ToFDepthConfidenceFilter](#class-tofdepthconfidencefilter)
   - [class UVC](#class-uvc)
   - [class VideoEncoder](#class-videoencoder)
   - [class Vpp](#class-vpp)
   - [class Warp](#class-warp)
5. [Summary](#summary)

---
## Imports

| # | Type | Module | Names / Alias | Line |
|---|------|--------|---------------|------|
| 1 | `from` | `None` | `internal` | L1 |
| 2 | `import` | `typing` | — | L4 |
| 3 | `from` | `pathlib` | `Path` | L6 |
| 4 | `from` | `typing` | `Set`, `Type`, `TypeVar` | L7 |
| 5 | `import` | `datetime` | — | L9 |
| 6 | `import` | `numpy` | — | L10 |
| 7 | `import` | `os` | — | L11 |
| 8 | `from` | `None` | `filters`, `modelzoo`, `nn_archive`, `node` | L12 |
| 9 | `from` | `_typeshed` | `Incomplete` | L13 |
| 10 | `from` | `depthai.filters.params` | `MedianFilter` | L14 |
| 11 | `from` | `typing` | `Callable`, `ClassVar`, `Iterable`, `Iterator`, `overload` | L15 |
| 12 | `from` | `pathlib` | `Path` | L19934 |
| 13 | `from` | `typing` | `Set` | L19935 |
| 14 | `import` | `datetime` | — | L19936 |
| 15 | `import` | `depthai` | — | L19937 |
| 16 | `import` | `os` | — | L19939 |
| 17 | `from` | `None` | `internal` | L19940 |
| 18 | `from` | `typing` | `Any`, `Callable`, `ClassVar`, `overload` | L19941 |

---
## Global Variables

| # | Name | Type Annotation | Value | Line |
|---|------|-----------------|-------|------|
| 1 | `json` | — | `dict` | L5 |
| 2 | `T` | — | `TypeVar('T')` | L8 |
| 3 | `LINE_LIST` | `PointsAnnotationType` | — | L17 |
| 4 | `LINE_LOOP` | `PointsAnnotationType` | — | L18 |
| 5 | `LINE_STRIP` | `PointsAnnotationType` | — | L19 |
| 6 | `POINTS` | `PointsAnnotationType` | — | L20 |
| 7 | `UNKNOWN` | `PointsAnnotationType` | — | L21 |
| 8 | `X_LINK_ALREADY_OPEN` | `XLinkError_t` | — | L22 |
| 9 | `X_LINK_ANY_PLATFORM` | `XLinkPlatform` | — | L23 |
| 10 | `X_LINK_ANY_PROTOCOL` | `XLinkProtocol` | — | L24 |
| 11 | `X_LINK_ANY_STATE` | `XLinkDeviceState` | — | L25 |
| 12 | `X_LINK_BOOTED` | `XLinkDeviceState` | — | L26 |
| 13 | `X_LINK_BOOTED_NON_EXCLUSIVE` | `XLinkDeviceState` | — | L27 |
| 14 | `X_LINK_BOOTLOADER` | `XLinkDeviceState` | — | L28 |
| 15 | `X_LINK_COMMUNICATION_FAIL` | `XLinkError_t` | — | L29 |
| 16 | `X_LINK_COMMUNICATION_NOT_OPEN` | `XLinkError_t` | — | L30 |
| 17 | `X_LINK_COMMUNICATION_UNKNOWN_ERROR` | `XLinkError_t` | — | L31 |
| 18 | `X_LINK_DEVICE_ALREADY_IN_USE` | `XLinkError_t` | — | L32 |
| 19 | `X_LINK_DEVICE_NOT_FOUND` | `XLinkError_t` | — | L33 |
| 20 | `X_LINK_ERROR` | `XLinkError_t` | — | L34 |
| 21 | `X_LINK_FLASH_BOOTED` | `XLinkDeviceState` | — | L35 |
| 22 | `X_LINK_GATE` | `XLinkDeviceState` | — | L36 |
| 23 | `X_LINK_GATE_BOOTED` | `XLinkDeviceState` | — | L37 |
| 24 | `X_LINK_GATE_SETUP` | `XLinkDeviceState` | — | L38 |
| 25 | `X_LINK_INIT_PCIE_ERROR` | `XLinkError_t` | — | L39 |
| 26 | `X_LINK_INIT_TCP_IP_ERROR` | `XLinkError_t` | — | L40 |
| 27 | `X_LINK_INIT_USB_ERROR` | `XLinkError_t` | — | L41 |
| 28 | `X_LINK_INSUFFICIENT_PERMISSIONS` | `XLinkError_t` | — | L42 |
| 29 | `X_LINK_IPC` | `XLinkProtocol` | — | L43 |
| 30 | `X_LINK_MYRIAD_2` | `XLinkPlatform` | — | L44 |
| 31 | `X_LINK_MYRIAD_X` | `XLinkPlatform` | — | L45 |
| 32 | `X_LINK_NMB_OF_PROTOCOLS` | `XLinkProtocol` | — | L46 |
| 33 | `X_LINK_NOT_IMPLEMENTED` | `XLinkError_t` | — | L47 |
| 34 | `X_LINK_OUT_OF_MEMORY` | `XLinkError_t` | — | L48 |
| 35 | `X_LINK_PCIE` | `XLinkProtocol` | — | L49 |
| 36 | `X_LINK_RVC3` | `XLinkPlatform` | — | L50 |
| 37 | `X_LINK_RVC4` | `XLinkPlatform` | — | L51 |
| 38 | `X_LINK_SUCCESS` | `XLinkError_t` | — | L52 |
| 39 | `X_LINK_TCP_IP` | `XLinkProtocol` | — | L53 |
| 40 | `X_LINK_TIMEOUT` | `XLinkError_t` | — | L54 |
| 41 | `X_LINK_UNBOOTED` | `XLinkDeviceState` | — | L55 |
| 42 | `X_LINK_USB_CDC` | `XLinkProtocol` | — | L56 |
| 43 | `X_LINK_USB_VSC` | `XLinkProtocol` | — | L57 |
| 44 | `__bootloader_version__` | `str` | — | L58 |
| 45 | `__build_datetime__` | `str` | — | L59 |
| 46 | `__commit__` | `str` | — | L60 |
| 47 | `__commit_datetime__` | `str` | — | L61 |
| 48 | `__device_rvc3_version__` | `str` | — | L62 |
| 49 | `__device_rvc4_version__` | `str` | — | L63 |
| 50 | `__device_version__` | `str` | — | L64 |
| 51 | `__init_subclass__` | `Callable` | — | L65 |
| 52 | `__version__` | `str` | — | L66 |
| 53 | `createSubnode` | `Callable` | — | L67 |

---
## Functions

### `def downloadModelsFromZoo(path: os.PathLike, cacheDirectory: os.PathLike = ..., apiKey: str = ..., progressFormat: str = ...) -> bool`
- **Line:** L19841
- **Docstring:** downloadModelsFromZoo(path: os.PathLike, cacheDirectory: os.PathLike = '', apiKey: str = '', progressFormat: str = 'none') -> bool

Helper function allowing one to download all models specified in yaml files in
the given path and store them in the cache directory

Parameter ``path:``:
    Path to the directory containing yaml files

Parameter ``cacheDirectory:``:
    Cache directory where the cached models are stored, default is "". If
    cacheDirectory is set to "", this function checks the DEPTHAI_ZOO_CACHE_PATH
    environment variable and uses that if set, otherwise the default is used
    (see getDefaultCachePath).

Parameter ``apiKey:``:
    API key for the model zoo, default is "". If apiKey is set to "", this
    function checks the DEPTHAI_ZOO_API_KEY environment variable and uses that
    if set. Otherwise, no API key is used.

Parameter ``progressFormat:``:
    Format to use for progress output (possible values: pretty, json, none),
    default is "pretty"

Returns:
    bool: True if all models were downloaded successfully, false otherwise

### `def getModelFromZoo(modelDescription: NNModelDescription, useCached: bool = ..., cacheDirectory: os.PathLike = ..., apiKey: str = ..., progressFormat: str = ...) -> os.PathLike`
- **Line:** L19868
- **Docstring:** getModelFromZoo(modelDescription: depthai.NNModelDescription, useCached: bool = True, cacheDirectory: os.PathLike = '', apiKey: str = '', progressFormat: str = 'none') -> os.PathLike

Get model from model zoo

Parameter ``modelDescription:``:
    Model description

Parameter ``useCached:``:
    Use cached model if present, default is true

Parameter ``cacheDirectory:``:
    Cache directory where the cached models are stored, default is "". If
    cacheDirectory is set to "", this function checks the DEPTHAI_ZOO_CACHE_PATH
    environment variable and uses that if set, otherwise the default value is
    used (see getDefaultCachePath).

Parameter ``apiKey:``:
    API key for the model zoo, default is "". If apiKey is set to "", this
    function checks the DEPTHAI_ZOO_API_KEY environment variable and uses that
    if set. Otherwise, no API key is used.

Parameter ``progressFormat:``:
    Format to use for progress output (possible values: pretty, json, none),
    default is "pretty"

Returns:
    std::filesystem::path: Path to the model in cache

### `def isDatatypeSubclassOf(arg0: DatatypeEnum, arg1: DatatypeEnum) -> bool`
- **Line:** L19897
- **Docstring:** isDatatypeSubclassOf(arg0: depthai.DatatypeEnum, arg1: depthai.DatatypeEnum) -> bool

### `def platform2string(arg0: Platform) -> str`
- **Line:** L19899
- **Docstring:** platform2string(arg0: depthai.Platform) -> str

Convert Platform enum to string

Parameter ``platform``:
    Platform enum

Returns:
    std::string String representation of Platform

### `def readModelType(modelPath: os.PathLike) -> ModelType`
- **Line:** L19910
- **Docstring:** readModelType(modelPath: os.PathLike) -> depthai.ModelType

Read model type from model path

Parameter ``modelPath``:
    Path to model

Returns:
    ModelType

### `def string2platform(arg0: str) -> Platform`
- **Line:** L19921
- **Docstring:** string2platform(arg0: str) -> depthai.Platform

Convert string to Platform enum

Parameter ``platform``:
    String representation of Platform

Returns:
    Platform Platform enum

---
## Classes

<a id="class-adatatype"></a>
### class `ADatatype`  — L69

> Abstract message

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L71 | __init__(self: depthai.ADatatype) -> None |

<a id="class-apriltag"></a>
### class `AprilTag`  — L74

> AprilTag structure.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `bottomLeft` | `Point2f` | — | L76 |
| `bottomRight` | `Point2f` | — | L77 |
| `decisionMargin` | `Incomplete` | — | L78 |
| `hamming` | `int` | — | L79 |
| `id` | `int` | — | L80 |
| `topLeft` | `Point2f` | — | L81 |
| `topRight` | `Point2f` | — | L82 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L83 | __init__(self: depthai.AprilTag) -> None |

<a id="class-apriltagconfig"></a>
### class `AprilTagConfig(Buffer)`  — L86

> AprilTagConfig message.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `decodeSharpening` | `float` | — | L145 |
| `family` | `AprilTagConfig.Family` | — | L146 |
| `maxHammingDistance` | `int` | — | L147 |
| `quadDecimate` | `int` | — | L148 |
| `quadSigma` | `float` | — | L149 |
| `quadThresholds` | `AprilTagConfig.QuadThresholds` | — | L150 |
| `refineEdges` | `bool` | — | L151 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L153 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self) -> None` | `(self)` | L162 | __init__(*args, **kwargs) |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def setFamily(self, family: AprilTagConfig.Family) -> AprilTagConfig` | `(self, family: AprilTagConfig.Family)` | L170 | setFamily(self: depthai.AprilTagConfig, family: depthai.AprilTagConfig.Family) -> depthai.AprilTagConfig |

**Nested Class:**

<a id="class-family"></a>
#### class `Family`  — L89

> Supported AprilTag families.

Members:

  TAG_36H11

  TAG_36H10

  TAG_25H9

  TAG_16H5

  TAG_CIR21H7

  TAG_STAND41H12

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L105 |
| `TAG_16H5` | `ClassVar[AprilTagConfig.Family]` | `...` | L106 |
| `TAG_25H9` | `ClassVar[AprilTagConfig.Family]` | `...` | L107 |
| `TAG_36H10` | `ClassVar[AprilTagConfig.Family]` | `...` | L108 |
| `TAG_36H11` | `ClassVar[AprilTagConfig.Family]` | `...` | L109 |
| `TAG_CIR21H7` | `ClassVar[AprilTagConfig.Family]` | `...` | L110 |
| `TAG_STAND41H12` | `ClassVar[AprilTagConfig.Family]` | `...` | L111 |
| `__entries` | `ClassVar[dict]` | `...` | L112 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L113 | __init__(self: depthai.AprilTagConfig.Family, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L115 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L117 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L119 | __index__(self: depthai.AprilTagConfig.Family) -> int |
| `def __int__(self) -> int` | `(self)` | L121 | __int__(self: depthai.AprilTagConfig.Family) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L123 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L126 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L132 | (arg0: depthai.AprilTagConfig.Family) -> int |

**Nested Class:**

<a id="class-quadthresholds"></a>
#### class `QuadThresholds`  — L135

> AprilTag quad threshold parameters.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `criticalDegree` | `float` | — | L137 |
| `deglitch` | `bool` | — | L138 |
| `maxLineFitMse` | `float` | — | L139 |
| `maxNmaxima` | `int` | — | L140 |
| `minClusterPixels` | `int` | — | L141 |
| `minWhiteBlackDiff` | `int` | — | L142 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L143 | __init__(self: depthai.AprilTagConfig.QuadThresholds) -> None |

<a id="class-apriltagproperties"></a>
### class `AprilTagProperties`  — L177

> Specify properties for AprilTag

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `initialConfig` | `AprilTagConfig` | — | L179 |
| `inputConfigSync` | `bool` | — | L180 |
| `numThreads` | `int` | — | L181 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L182 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-apriltags"></a>
### class `AprilTags(Buffer)`  — L185

> AprilTags message.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `aprilTags` | `list[AprilTag]` | — | L187 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L188 | __init__(self: depthai.AprilTags) -> None |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getSequenceNum(self) -> int` | `(self)` | L190 | getSequenceNum(self: depthai.AprilTags) -> int |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L195 | getTimestamp(self: depthai.AprilTags) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L200 | getTimestampDevice(self: depthai.AprilTags) -> datetime.timedelta |

<a id="class-asset"></a>
### class `Asset`  — L207

> Asset is identified with string key and can store arbitrary binary data

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `alignment` | `int` | — | L209 |
| `data` | `numpy.ndarray[numpy.uint8]` | — | L210 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L212 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: str) -> None` | `(self, arg0: str)` | L221 | __init__(*args, **kwargs) |

**📌 Properties (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def key(self) -> str` | `(self)` | L230 | (self: depthai.Asset) -> str |

<a id="class-assetmanager"></a>
### class `AssetManager`  — L233

> AssetManager can store assets and serialize

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L236 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: str) -> None` | `(self, arg0: str)` | L245 | __init__(*args, **kwargs) |

**🔹 Public Methods (12):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def addExisting(self, assets: list[Asset]) -> None` | `(self, assets: list[Asset])` | L253 | addExisting(self: depthai.AssetManager, assets: list[depthai.Asset]) -> None |
| `@overload` `def get(self, key: str) -> Asset` | `(self, key: str)` | L262 | get(*args, **kwargs) |
| `@overload` `def get(self, key: str) -> Asset` | `(self, key: str)` | L277 | get(*args, **kwargs) |
| `@overload` `def getAll(self) -> list[Asset]` | `(self)` | L292 | getAll(*args, **kwargs) |
| `@overload` `def getAll(self) -> list[Asset]` | `(self)` | L307 | getAll(*args, **kwargs) |
| `def getRootPath(self) -> str` | `(self)` | L321 | getRootPath(self: depthai.AssetManager) -> str |
| `def remove(self, key: str) -> None` | `(self, key: str)` | L329 | remove(self: depthai.AssetManager, key: str) -> None |
| `@overload` `def set(self, asset: Asset) -> Asset` | `(self, asset: Asset)` | L338 | set(*args, **kwargs) |
| `@overload` `def set(self, key: str, asset: Asset) -> Asset` | `(self, key: str, asset: Asset)` | L396 | set(*args, **kwargs) |
| `@overload` `def set(self, key: str, path: os.PathLike, alignment: int = ...) -> Asset` | `(self, key: str, path: os.PathLike, alignment: int = ...)` | L454 | set(*args, **kwargs) |
| `@overload` `def set(self, key: str, data, std, alignment: int = ...) -> Asset` | `(self, key: str, data, std, alignment: int = ...)` | L512 | set(*args, **kwargs) |
| `def size(self) -> int` | `(self)` | L569 | size(self: depthai.AssetManager) -> int |

<a id="class-benchmarkreport"></a>
### class `BenchmarkReport(Buffer)`  — L576

> BenchmarkReport message.

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L578 | __init__(self: depthai.BenchmarkReport) -> None |

**📌 Properties (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def averageLatency(self) -> float` | `(self)` | L581 | (arg0: depthai.BenchmarkReport) -> float |
| `@property` `def fps(self) -> float` | `(self)` | L584 | (arg0: depthai.BenchmarkReport) -> float |
| `@property` `def latencies(self) -> list[float]` | `(self)` | L587 | (arg0: depthai.BenchmarkReport) -> list[float] |
| `@property` `def numMessagesReceived(self) -> float` | `(self)` | L590 | (arg0: depthai.BenchmarkReport) -> float |
| `@property` `def timeTotal(self) -> float` | `(self)` | L593 | (arg0: depthai.BenchmarkReport) -> float |

<a id="class-blockpipelineevent"></a>
### class `BlockPipelineEvent`  — L596

**🔧 Dunder Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L597 | Initialize self.  See help(type(self)) for accurate signature. |
| `def __enter__(self) -> BlockPipelineEvent` | `(self)` | L605 | __enter__(self: depthai.BlockPipelineEvent) -> depthai.BlockPipelineEvent |
| `def __exit__(self, arg0: object, arg1: object, arg2: object) -> None` | `(self, arg0: object, arg1: object, arg2: object)` | L607 | __exit__(self: depthai.BlockPipelineEvent, arg0: object, arg1: object, arg2: object) -> None |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def cancel(self) -> None` | `(self)` | L599 | cancel(self: depthai.BlockPipelineEvent) -> None |
| `def setEndTimestamp(self, timestamp: datetime.timedelta) -> None` | `(self, timestamp: datetime.timedelta)` | L601 | setEndTimestamp(self: depthai.BlockPipelineEvent, timestamp: datetime.timedelta) -> None |
| `def setQueueSize(self, size: int) -> None` | `(self, size: int)` | L603 | setQueueSize(self: depthai.BlockPipelineEvent, size: int) -> None |

<a id="class-boardconfig"></a>
### class `BoardConfig`  — L610

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `emmc` | `bool | None` | — | L1105 |
| `gpio` | `BoardConfig.GPIOMap` | — | L1106 |
| `logDevicePrints` | `bool | None` | — | L1107 |
| `logPath` | `str | None` | — | L1108 |
| `logSizeMax` | `int | None` | — | L1109 |
| `logVerbosity` | `LogLevel | None` | — | L1110 |
| `mipi4LaneRgb` | `bool | None` | — | L1111 |
| `network` | `BoardConfig.Network` | — | L1112 |
| `pcieInternalClock` | `bool | None` | — | L1113 |
| `sysctl` | `list[str]` | — | L1114 |
| `uart` | `BoardConfig.UARTMap` | — | L1115 |
| `usb` | `BoardConfig.USB` | — | L1116 |
| `usb3PhyInternalClock` | `bool | None` | — | L1117 |
| `uvc` | `BoardConfig.UVC | None` | — | L1118 |
| `watchdogInitialDelayMs` | `int | None` | — | L1119 |
| `watchdogTimeoutMs` | `int | None` | — | L1120 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L1121 | __init__(self: depthai.BoardConfig) -> None |

**Nested Class:**

<a id="class-gpio"></a>
#### class `GPIO`  — L611

> GPIO config

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `ALT_MODE_0` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L813 |
| `ALT_MODE_1` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L814 |
| `ALT_MODE_2` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L815 |
| `ALT_MODE_3` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L816 |
| `ALT_MODE_4` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L817 |
| `ALT_MODE_5` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L818 |
| `ALT_MODE_6` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L819 |
| `BUS_KEEPER` | `ClassVar[BoardConfig.GPIO.Pull]` | `...` | L820 |
| `DIRECT` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L821 |
| `HIGH` | `ClassVar[BoardConfig.GPIO.Level]` | `...` | L822 |
| `INPUT` | `ClassVar[BoardConfig.GPIO.Direction]` | `...` | L823 |
| `LOW` | `ClassVar[BoardConfig.GPIO.Level]` | `...` | L824 |
| `MA_12` | `ClassVar[BoardConfig.GPIO.Drive]` | `...` | L825 |
| `MA_2` | `ClassVar[BoardConfig.GPIO.Drive]` | `...` | L826 |
| `MA_4` | `ClassVar[BoardConfig.GPIO.Drive]` | `...` | L827 |
| `MA_8` | `ClassVar[BoardConfig.GPIO.Drive]` | `...` | L828 |
| `NO_PULL` | `ClassVar[BoardConfig.GPIO.Pull]` | `...` | L829 |
| `OUTPUT` | `ClassVar[BoardConfig.GPIO.Direction]` | `...` | L830 |
| `PULL_DOWN` | `ClassVar[BoardConfig.GPIO.Pull]` | `...` | L831 |
| `PULL_UP` | `ClassVar[BoardConfig.GPIO.Pull]` | `...` | L832 |
| `direction` | `BoardConfig.GPIO.Direction` | — | L833 |
| `drive` | `BoardConfig.GPIO.Drive` | — | L834 |
| `level` | `BoardConfig.GPIO.Level` | — | L835 |
| `mode` | `BoardConfig.GPIO.Mode` | — | L836 |
| `pull` | `BoardConfig.GPIO.Pull` | — | L837 |
| `schmitt` | `bool` | — | L838 |
| `slewFast` | `bool` | — | L839 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L841 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: BoardConfig.GPIO.Direction) -> None` | `(self, arg0: BoardConfig.GPIO.Direction)` | L858 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: BoardConfig.GPIO.Direction, arg1: BoardConfig.GPIO.Level) -> None` | `(self, arg0: BoardConfig.GPIO.Direction, arg1: BoardConfig.GPIO.Level)` | L875 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: BoardConfig.GPIO.Direction, arg1: BoardConfig.GPIO.Level, arg2: BoardConfig.GPIO.Pull) -> None` | `(self, arg0: BoardConfig.GPIO.Direction, arg1: BoardConfig.GPIO.Level, arg2: BoardConfig.GPIO.Pull)` | L892 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: BoardConfig.GPIO.Direction, arg1: BoardConfig.GPIO.Mode) -> None` | `(self, arg0: BoardConfig.GPIO.Direction, arg1: BoardConfig.GPIO.Mode)` | L909 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: BoardConfig.GPIO.Direction, arg1: BoardConfig.GPIO.Mode, arg2: BoardConfig.GPIO.Pull) -> None` | `(self, arg0: BoardConfig.GPIO.Direction, arg1: BoardConfig.GPIO.Mode, arg2: BoardConfig.GPIO.Pull)` | L926 | __init__(*args, **kwargs) |

**Nested Class:**

<a id="class-direction"></a>
##### class `Direction`  — L614

> Members:

  INPUT : 

  OUTPUT : 

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L622 |
| `INPUT` | `ClassVar[BoardConfig.GPIO.Direction]` | `...` | L623 |
| `OUTPUT` | `ClassVar[BoardConfig.GPIO.Direction]` | `...` | L624 |
| `__entries` | `ClassVar[dict]` | `...` | L625 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L626 | __init__(self: depthai.BoardConfig.GPIO.Direction, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L628 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L630 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L632 | __index__(self: depthai.BoardConfig.GPIO.Direction) -> int |
| `def __int__(self) -> int` | `(self)` | L634 | __int__(self: depthai.BoardConfig.GPIO.Direction) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L636 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L639 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L645 | (arg0: depthai.BoardConfig.GPIO.Direction) -> int |

**Nested Class:**

<a id="class-drive"></a>
##### class `Drive`  — L648

> Drive strength in mA (2, 4, 8 and 12mA)

Members:

  MA_2 : 

  MA_4 : 

  MA_8 : 

  MA_12 : 

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L660 |
| `MA_12` | `ClassVar[BoardConfig.GPIO.Drive]` | `...` | L661 |
| `MA_2` | `ClassVar[BoardConfig.GPIO.Drive]` | `...` | L662 |
| `MA_4` | `ClassVar[BoardConfig.GPIO.Drive]` | `...` | L663 |
| `MA_8` | `ClassVar[BoardConfig.GPIO.Drive]` | `...` | L664 |
| `__entries` | `ClassVar[dict]` | `...` | L665 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L666 | __init__(self: depthai.BoardConfig.GPIO.Drive, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L668 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L670 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L672 | __index__(self: depthai.BoardConfig.GPIO.Drive) -> int |
| `def __int__(self) -> int` | `(self)` | L674 | __int__(self: depthai.BoardConfig.GPIO.Drive) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L676 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L679 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L685 | (arg0: depthai.BoardConfig.GPIO.Drive) -> int |

**Nested Class:**

<a id="class-level"></a>
##### class `Level`  — L688

> Members:

  LOW : 

  HIGH : 

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L696 |
| `HIGH` | `ClassVar[BoardConfig.GPIO.Level]` | `...` | L697 |
| `LOW` | `ClassVar[BoardConfig.GPIO.Level]` | `...` | L698 |
| `__entries` | `ClassVar[dict]` | `...` | L699 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L700 | __init__(self: depthai.BoardConfig.GPIO.Level, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L702 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L704 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L706 | __index__(self: depthai.BoardConfig.GPIO.Level) -> int |
| `def __int__(self) -> int` | `(self)` | L708 | __int__(self: depthai.BoardConfig.GPIO.Level) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L710 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L713 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L719 | (arg0: depthai.BoardConfig.GPIO.Level) -> int |

**Nested Class:**

<a id="class-mode"></a>
##### class `Mode`  — L722

> Members:

  ALT_MODE_0 : 

  ALT_MODE_1 : 

  ALT_MODE_2 : 

  ALT_MODE_3 : 

  ALT_MODE_4 : 

  ALT_MODE_5 : 

  ALT_MODE_6 : 

  DIRECT : 

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L742 |
| `ALT_MODE_0` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L743 |
| `ALT_MODE_1` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L744 |
| `ALT_MODE_2` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L745 |
| `ALT_MODE_3` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L746 |
| `ALT_MODE_4` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L747 |
| `ALT_MODE_5` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L748 |
| `ALT_MODE_6` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L749 |
| `DIRECT` | `ClassVar[BoardConfig.GPIO.Mode]` | `...` | L750 |
| `__entries` | `ClassVar[dict]` | `...` | L751 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L752 | __init__(self: depthai.BoardConfig.GPIO.Mode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L754 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L756 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L758 | __index__(self: depthai.BoardConfig.GPIO.Mode) -> int |
| `def __int__(self) -> int` | `(self)` | L760 | __int__(self: depthai.BoardConfig.GPIO.Mode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L762 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L765 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L771 | (arg0: depthai.BoardConfig.GPIO.Mode) -> int |

**Nested Class:**

<a id="class-pull"></a>
##### class `Pull`  — L774

> Members:

  NO_PULL : 

  PULL_UP : 

  PULL_DOWN : 

  BUS_KEEPER : 

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L786 |
| `BUS_KEEPER` | `ClassVar[BoardConfig.GPIO.Pull]` | `...` | L787 |
| `NO_PULL` | `ClassVar[BoardConfig.GPIO.Pull]` | `...` | L788 |
| `PULL_DOWN` | `ClassVar[BoardConfig.GPIO.Pull]` | `...` | L789 |
| `PULL_UP` | `ClassVar[BoardConfig.GPIO.Pull]` | `...` | L790 |
| `__entries` | `ClassVar[dict]` | `...` | L791 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L792 | __init__(self: depthai.BoardConfig.GPIO.Pull, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L794 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L796 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L798 | __index__(self: depthai.BoardConfig.GPIO.Pull) -> int |
| `def __int__(self) -> int` | `(self)` | L800 | __int__(self: depthai.BoardConfig.GPIO.Pull) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L802 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L805 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L811 | (arg0: depthai.BoardConfig.GPIO.Pull) -> int |

**Nested Class:**

<a id="class-gpiomap"></a>
#### class `GPIOMap`  — L943

**🔧 Dunder Methods (9):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L944 | __init__(self: depthai.BoardConfig.GPIOMap) -> None |
| `def __bool__(self) -> bool` | `(self)` | L952 | __bool__(self: depthai.BoardConfig.GPIOMap) -> bool |
| `@overload` `def __contains__(self, arg0: int) -> bool` | `(self, arg0: int)` | L958 | __contains__(*args, **kwargs) |
| `@overload` `def __contains__(self, arg0: object) -> bool` | `(self, arg0: object)` | L967 | __contains__(*args, **kwargs) |
| `def __delitem__(self, arg0: int) -> None` | `(self, arg0: int)` | L975 | __delitem__(self: depthai.BoardConfig.GPIOMap, arg0: int) -> None |
| `def __getitem__(self, arg0: int) -> BoardConfig.GPIO` | `(self, arg0: int)` | L977 | __getitem__(self: depthai.BoardConfig.GPIOMap, arg0: int) -> depthai.BoardConfig.GPIO |
| `def __iter__(self) -> Iterator[int]` | `(self)` | L979 | __iter__(self: depthai.BoardConfig.GPIOMap) -> Iterator[int] |
| `def __len__(self) -> int` | `(self)` | L981 | __len__(self: depthai.BoardConfig.GPIOMap) -> int |
| `def __setitem__(self, arg0: int, arg1: BoardConfig.GPIO) -> None` | `(self, arg0: int, arg1: BoardConfig.GPIO)` | L983 | __setitem__(self: depthai.BoardConfig.GPIOMap, arg0: int, arg1: depthai.BoardConfig.GPIO) -> None |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def items(self) -> BoardConfig.ItemsView` | `(self)` | L946 | items(self: depthai.BoardConfig.GPIOMap) -> depthai.BoardConfig.ItemsView |
| `def keys(self) -> BoardConfig.KeysView` | `(self)` | L948 | keys(self: depthai.BoardConfig.GPIOMap) -> depthai.BoardConfig.KeysView |
| `def values(self) -> BoardConfig.ValuesView` | `(self)` | L950 | values(self: depthai.BoardConfig.GPIOMap) -> depthai.BoardConfig.ValuesView |

**Nested Class:**

<a id="class-itemsview"></a>
#### class `ItemsView`  — L986

**🔧 Dunder Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L987 | Initialize self.  See help(type(self)) for accurate signature. |
| `def __iter__(self) -> Iterator` | `(self)` | L989 | __iter__(self: depthai.BoardConfig.ItemsView) -> Iterator |
| `def __len__(self) -> int` | `(self)` | L991 | __len__(self: depthai.BoardConfig.ItemsView) -> int |

**Nested Class:**

<a id="class-keysview"></a>
#### class `KeysView`  — L994

**🔧 Dunder Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L995 | Initialize self.  See help(type(self)) for accurate signature. |
| `def __contains__(self, arg0: object) -> bool` | `(self, arg0: object)` | L997 | __contains__(self: depthai.BoardConfig.KeysView, arg0: object) -> bool |
| `def __iter__(self) -> Iterator` | `(self)` | L999 | __iter__(self: depthai.BoardConfig.KeysView) -> Iterator |
| `def __len__(self) -> int` | `(self)` | L1001 | __len__(self: depthai.BoardConfig.KeysView) -> int |

**Nested Class:**

<a id="class-network"></a>
#### class `Network`  — L1004

> Network configuration

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `mtu` | `int` | — | L1006 |
| `xlinkTcpNoDelay` | `bool` | — | L1007 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L1008 | __init__(self: depthai.BoardConfig.Network) -> None |

**Nested Class:**

<a id="class-uart"></a>
#### class `UART`  — L1011

> UART instance config

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `tmp` | `int` | — | L1013 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L1014 | __init__(self: depthai.BoardConfig.UART) -> None |

**Nested Class:**

<a id="class-uartmap"></a>
#### class `UARTMap`  — L1017

**🔧 Dunder Methods (9):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L1018 | __init__(self: depthai.BoardConfig.UARTMap) -> None |
| `def __bool__(self) -> bool` | `(self)` | L1026 | __bool__(self: depthai.BoardConfig.UARTMap) -> bool |
| `@overload` `def __contains__(self, arg0: int) -> bool` | `(self, arg0: int)` | L1032 | __contains__(*args, **kwargs) |
| `@overload` `def __contains__(self, arg0: object) -> bool` | `(self, arg0: object)` | L1041 | __contains__(*args, **kwargs) |
| `def __delitem__(self, arg0: int) -> None` | `(self, arg0: int)` | L1049 | __delitem__(self: depthai.BoardConfig.UARTMap, arg0: int) -> None |
| `def __getitem__(self, arg0: int) -> BoardConfig.UART` | `(self, arg0: int)` | L1051 | __getitem__(self: depthai.BoardConfig.UARTMap, arg0: int) -> depthai.BoardConfig.UART |
| `def __iter__(self) -> Iterator[int]` | `(self)` | L1053 | __iter__(self: depthai.BoardConfig.UARTMap) -> Iterator[int] |
| `def __len__(self) -> int` | `(self)` | L1055 | __len__(self: depthai.BoardConfig.UARTMap) -> int |
| `def __setitem__(self, arg0: int, arg1: BoardConfig.UART) -> None` | `(self, arg0: int, arg1: BoardConfig.UART)` | L1057 | __setitem__(self: depthai.BoardConfig.UARTMap, arg0: int, arg1: depthai.BoardConfig.UART) -> None |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def items(self) -> BoardConfig.ItemsView` | `(self)` | L1020 | items(self: depthai.BoardConfig.UARTMap) -> depthai.BoardConfig.ItemsView |
| `def keys(self) -> BoardConfig.KeysView` | `(self)` | L1022 | keys(self: depthai.BoardConfig.UARTMap) -> depthai.BoardConfig.KeysView |
| `def values(self) -> BoardConfig.ValuesView` | `(self)` | L1024 | values(self: depthai.BoardConfig.UARTMap) -> depthai.BoardConfig.ValuesView |

**Nested Class:**

<a id="class-usb"></a>
#### class `USB`  — L1060

> USB related config

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `flashBootedPid` | `int` | — | L1062 |
| `flashBootedVid` | `int` | — | L1063 |
| `manufacturer` | `str` | — | L1064 |
| `maxSpeed` | `UsbSpeed` | — | L1065 |
| `pid` | `int` | — | L1066 |
| `productName` | `str` | — | L1067 |
| `vid` | `int` | — | L1068 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L1069 | __init__(self: depthai.BoardConfig.USB) -> None |

**Nested Class:**

<a id="class-uvc"></a>
#### class `UVC`  — L1072

> UVC configuration for USB descriptor

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `cameraName` | `str` | — | L1074 |
| `enable` | `bool` | — | L1075 |
| `frameType` | `ImgFrame.Type` | — | L1076 |
| `height` | `int` | — | L1077 |
| `width` | `int` | — | L1078 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L1080 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: int, arg1: int) -> None` | `(self, arg0: int, arg1: int)` | L1089 | __init__(*args, **kwargs) |

**Nested Class:**

<a id="class-valuesview"></a>
#### class `ValuesView`  — L1098

**🔧 Dunder Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L1099 | Initialize self.  See help(type(self)) for accurate signature. |
| `def __iter__(self) -> Iterator` | `(self)` | L1101 | __iter__(self: depthai.BoardConfig.ValuesView) -> Iterator |
| `def __len__(self) -> int` | `(self)` | L1103 | __len__(self: depthai.BoardConfig.ValuesView) -> int |

<a id="class-buffer"></a>
### class `Buffer(ADatatype)`  — L1124

> Base message - buffer of binary data

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L1127 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: int) -> None` | `(self, arg0: int)` | L1136 | __init__(*args, **kwargs) |

**🔹 Public Methods (11):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getData(self) -> numpy.ndarray[numpy.uint8]` | `(self)` | L1144 | getData(self: object) -> numpy.ndarray[numpy.uint8] |
| `def getSequenceNum(self) -> int` | `(self)` | L1152 | getSequenceNum(self: depthai.Buffer) -> int |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L1157 | getTimestamp(self: depthai.Buffer) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L1162 | getTimestampDevice(self: depthai.Buffer) -> datetime.timedelta |
| `def getVisualizationMessage(self) -> ImgAnnotations | ImgFrame | None` | `(self)` | L1168 | getVisualizationMessage(self: depthai.Buffer) -> Union[depthai.ImgAnnotations, depthai.ImgFrame, None] |
| `@overload` `def setData(self, arg0, std) -> None` | `(self, arg0, std)` | L1178 | setData(*args, **kwargs) |
| `@overload` `def setData(self, arg0: numpy.ndarray[numpy.uint8]) -> None` | `(self, arg0: numpy.ndarray[numpy.uint8])` | L1198 | setData(*args, **kwargs) |
| `@overload` `def setData(self, arg0: Buffer) -> None` | `(self, arg0: Buffer)` | L1218 | setData(*args, **kwargs) |
| `def setSequenceNum(self, arg0: int) -> None` | `(self, arg0: int)` | L1237 | setSequenceNum(self: depthai.Buffer, arg0: int) -> None |
| `def setTimestamp(self, arg0: datetime.timedelta) -> None` | `(self, arg0: datetime.timedelta)` | L1242 | setTimestamp(self: depthai.Buffer, arg0: datetime.timedelta) -> None |
| `def setTimestampDevice(self, arg0: datetime.timedelta) -> None` | `(self, arg0: datetime.timedelta)` | L1247 | setTimestampDevice(self: depthai.Buffer, arg0: datetime.timedelta) -> None |

<a id="class-calibrationhandler"></a>
### class `CalibrationHandler`  — L1253

> CalibrationHandler is an interface to read/load/write structured calibration and
device data. The following fields are protected and aren't allowed to be
overridden by default: - boardName - boardRev - boardConf - hardwareConf -
batchName - batchTime - boardOptions - productName

**🔧 Dunder Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L1259 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, eepromDataPath: os.PathLike, validateExtrinsics: bool = ...) -> None` | `(self, eepromDataPath: os.PathLike, validateExtrinsics: bool = ...)` | L1303 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, calibrationDataPath: os.PathLike, boardConfigPath: os.PathLike, validateExtrinsics: bool = ...) -> None` | `(self, calibrationDataPath: os.PathLike, boardConfigPath: os.PathLike, validateExtrinsics: bool = ...)` | L1347 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, eepromData: EepromData, validateExtrinsics: bool = ...) -> None` | `(self, eepromData: EepromData, validateExtrinsics: bool = ...)` | L1391 | __init__(*args, **kwargs) |

**⚡ Static Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@staticmethod` `def fromJson(eepromDataJson: json, validateExtrinsics: bool | None = ...) -> CalibrationHandler` | `(eepromDataJson: json, validateExtrinsics: bool | None = ...)` | L1454 | fromJson(eepromDataJson: json, validateExtrinsics: Optional[bool] = None) -> depthai.CalibrationHandler |

**🔹 Public Methods (35):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def eepromToJson(self) -> json` | `(self)` | L1434 | eepromToJson(self: depthai.CalibrationHandler) -> json |
| `def eepromToJsonFile(self, destPath: os.PathLike) -> bool` | `(self, destPath: os.PathLike)` | L1442 | eepromToJsonFile(self: depthai.CalibrationHandler, destPath: os.PathLike) -> bool |
| `def getBaselineDistance(self, cam1: CameraBoardSocket = ..., cam2: CameraBoardSocket = ..., useSpecTranslation: bool = ...) -> float` | `(self, cam1: CameraBoardSocket = ..., cam2: CameraBoardSocket = ..., useSpecTranslation: bool = ...)` | L1465 | getBaselineDistance(self: depthai.CalibrationHandler, cam1: depthai.CameraBoardSocket = <CameraBoardSocket.???: 2>, cam2: depthai.CameraBoardSocket = <CameraBoardSocket.???: 1>, useSpecTranslation: bool = True) -> float |
| `def getCameraExtrinsics(self, srcCamera: CameraBoardSocket, dstCamera: CameraBoardSocket, useSpecTranslation: bool = ...) -> list[list[float]]` | `(self, srcCamera: CameraBoardSocket, dstCamera: CameraBoardSocket, useSpecTranslation: bool = ...)` | L1484 | getCameraExtrinsics(self: depthai.CalibrationHandler, srcCamera: depthai.CameraBoardSocket, dstCamera: depthai.CameraBoardSocket, useSpecTranslation: bool = False) -> list[list[float]] |
| `def getCameraIntrinsics(self, cameraId: CameraBoardSocket, resizeWidth: int = ..., resizeHeight: int = ..., topLeftPixelId: Point2f = ..., bottomRightPixelId: Point2f = ..., keepAspectRatio: bool = ...) -> list[list[float]]` | `(self, cameraId: CameraBoardSocket, resizeWidth: int = ..., resizeHeight: int = ..., topLeftPixelId: Point2f = ..., bottomRightPixelId: Point2f = ..., keepAspectRatio: bool = ...)` | L1510 | getCameraIntrinsics(*args, **kwargs) |
| `def getCameraRotationMatrix(self, srcCamera: CameraBoardSocket, dstCamera: CameraBoardSocket) -> list[list[float]]` | `(self, srcCamera: CameraBoardSocket, dstCamera: CameraBoardSocket)` | L1612 | getCameraRotationMatrix(self: depthai.CalibrationHandler, srcCamera: depthai.CameraBoardSocket, dstCamera: depthai.CameraBoardSocket) -> list[list[float]] |
| `def getCameraToImuExtrinsics(self, cameraId: CameraBoardSocket, useSpecTranslation: bool = ...) -> list[list[float]]` | `(self, cameraId: CameraBoardSocket, useSpecTranslation: bool = ...)` | L1629 | getCameraToImuExtrinsics(self: depthai.CalibrationHandler, cameraId: depthai.CameraBoardSocket, useSpecTranslation: bool = False) -> list[list[float]] |
| `def getCameraTranslationVector(self, srcCamera: CameraBoardSocket, dstCamera: CameraBoardSocket, useSpecTranslation: bool = ...) -> list[float]` | `(self, srcCamera: CameraBoardSocket, dstCamera: CameraBoardSocket, useSpecTranslation: bool = ...)` | L1652 | getCameraTranslationVector(self: depthai.CalibrationHandler, srcCamera: depthai.CameraBoardSocket, dstCamera: depthai.CameraBoardSocket, useSpecTranslation: bool = True) -> list[float] |
| `def getDefaultIntrinsics(self, cameraId: CameraBoardSocket) -> tuple[list[list[float]], int, int]` | `(self, cameraId: CameraBoardSocket)` | L1671 | getDefaultIntrinsics(self: depthai.CalibrationHandler, cameraId: depthai.CameraBoardSocket) -> tuple[list[list[float]], int, int] |
| `def getDistortionCoefficients(self, cameraId: CameraBoardSocket) -> list[float]` | `(self, cameraId: CameraBoardSocket)` | L1687 | getDistortionCoefficients(self: depthai.CalibrationHandler, cameraId: depthai.CameraBoardSocket) -> list[float] |
| `def getDistortionModel(self, cameraId: CameraBoardSocket) -> CameraModel` | `(self, cameraId: CameraBoardSocket)` | L1704 | getDistortionModel(self: depthai.CalibrationHandler, cameraId: depthai.CameraBoardSocket) -> depthai.CameraModel |
| `def getEepromData(self) -> EepromData` | `(self)` | L1715 | getEepromData(self: depthai.CalibrationHandler) -> depthai.EepromData |
| `def getFov(self, cameraId: CameraBoardSocket, useSpec: bool = ...) -> float` | `(self, cameraId: CameraBoardSocket, useSpec: bool = ...)` | L1723 | getFov(self: depthai.CalibrationHandler, cameraId: depthai.CameraBoardSocket, useSpec: bool = True) -> float |
| `def getHousingCalibration(self, srcCamera: CameraBoardSocket, housingCS: HousingCoordinateSystem, useSpecTranslation: bool = ...) -> list[list[float]]` | `(self, srcCamera: CameraBoardSocket, housingCS: HousingCoordinateSystem, useSpecTranslation: bool = ...)` | L1738 | getHousingCalibration(self: depthai.CalibrationHandler, srcCamera: depthai.CameraBoardSocket, housingCS: depthai.HousingCoordinateSystem, useSpecTranslation: bool = True) -> list[list[float]] |
| `def getImuToCameraExtrinsics(self, cameraId: CameraBoardSocket, useSpecTranslation: bool = ...) -> list[list[float]]` | `(self, cameraId: CameraBoardSocket, useSpecTranslation: bool = ...)` | L1768 | getImuToCameraExtrinsics(self: depthai.CalibrationHandler, cameraId: depthai.CameraBoardSocket, useSpecTranslation: bool = False) -> list[list[float]] |
| `def getLensPosition(self, cameraId: CameraBoardSocket) -> int` | `(self, cameraId: CameraBoardSocket)` | L1791 | getLensPosition(self: depthai.CalibrationHandler, cameraId: depthai.CameraBoardSocket) -> int |
| `def getStereoLeftCameraId(self) -> CameraBoardSocket` | `(self)` | L1802 | getStereoLeftCameraId(self: depthai.CalibrationHandler) -> depthai.CameraBoardSocket |
| `def getStereoLeftRectificationRotation(self) -> list[list[float]]` | `(self)` | L1810 | getStereoLeftRectificationRotation(self: depthai.CalibrationHandler) -> list[list[float]] |
| `def getStereoRightCameraId(self) -> CameraBoardSocket` | `(self)` | L1818 | getStereoRightCameraId(self: depthai.CalibrationHandler) -> depthai.CameraBoardSocket |
| `def getStereoRightRectificationRotation(self) -> list[list[float]]` | `(self)` | L1827 | getStereoRightRectificationRotation(self: depthai.CalibrationHandler) -> list[list[float]] |
| `@overload` `def setBoardInfo(self, boardName: str, boardRev: str) -> None` | `(self, boardName: str, boardRev: str)` | L1836 | setBoardInfo(*args, **kwargs) |
| `@overload` `def setBoardInfo(self, productName: str, boardName: str, boardRev: str, boardConf: str, hardwareConf: str, batchName: str, batchTime: int, boardOptions: int, boardCustom: str = ...) -> None` | `(self, productName: str, boardName: str, boardRev: str, boardConf: str, hardwareConf: str, batchName: str, batchTime: int, boardOptions: int, boardCustom: str = ...)` | L1913 | setBoardInfo(*args, **kwargs) |
| `@overload` `def setBoardInfo(self, deviceName: str, productName: str, boardName: str, boardRev: str, boardConf: str, hardwareConf: str, batchName: str, batchTime: int, boardOptions: int, boardCustom: str = ...) -> None` | `(self, deviceName: str, productName: str, boardName: str, boardRev: str, boardConf: str, hardwareConf: str, batchName: str, batchTime: int, boardOptions: int, boardCustom: str = ...)` | L1990 | setBoardInfo(*args, **kwargs) |
| `def setCameraExtrinsics(self, srcCameraId: CameraBoardSocket, destCameraId: CameraBoardSocket, rotationMatrix: list[list[float]], translation: list[float], specTranslation: list[float] = ...) -> None` | `(self, srcCameraId: CameraBoardSocket, destCameraId: CameraBoardSocket, rotationMatrix: list[list[float]], translation: list[float], specTranslation: list[float] = ...)` | L2066 | setCameraExtrinsics(self: depthai.CalibrationHandler, srcCameraId: depthai.CameraBoardSocket, destCameraId: depthai.CameraBoardSocket, rotationMatrix: list[list[float]], translation: list[float], specTranslation: list[float] = [0.0, 0.0, 0.0]) -> None |
| `def setCameraIntrinsics(self, cameraId: CameraBoardSocket, intrinsics: list[list[float]], frameSize: Size2f) -> None` | `(self, cameraId: CameraBoardSocket, intrinsics: list[list[float]], frameSize: Size2f)` | L2087 | setCameraIntrinsics(*args, **kwargs) |
| `def setCameraType(self, cameraId: CameraBoardSocket, cameraModel: CameraModel) -> None` | `(self, cameraId: CameraBoardSocket, cameraModel: CameraModel)` | L2147 | setCameraType(self: depthai.CalibrationHandler, cameraId: depthai.CameraBoardSocket, cameraModel: depthai.CameraModel) -> None |
| `def setDeviceName(self, deviceName: str) -> None` | `(self, deviceName: str)` | L2158 | setDeviceName(self: depthai.CalibrationHandler, deviceName: str) -> None |
| `def setDistortionCoefficients(self, cameraId: CameraBoardSocket, distortionCoefficients: list[float]) -> None` | `(self, cameraId: CameraBoardSocket, distortionCoefficients: list[float])` | L2166 | setDistortionCoefficients(self: depthai.CalibrationHandler, cameraId: depthai.CameraBoardSocket, distortionCoefficients: list[float]) -> None |
| `def setFov(self, cameraId: CameraBoardSocket, hfov: float) -> None` | `(self, cameraId: CameraBoardSocket, hfov: float)` | L2177 | setFov(self: depthai.CalibrationHandler, cameraId: depthai.CameraBoardSocket, hfov: float) -> None |
| `def setImuExtrinsics(self, destCameraId: CameraBoardSocket, rotationMatrix: list[list[float]], translation: list[float], specTranslation: list[float] = ...) -> None` | `(self, destCameraId: CameraBoardSocket, rotationMatrix: list[list[float]], translation: list[float], specTranslation: list[float] = ...)` | L2188 | setImuExtrinsics(self: depthai.CalibrationHandler, destCameraId: depthai.CameraBoardSocket, rotationMatrix: list[list[float]], translation: list[float], specTranslation: list[float] = [0.0, 0.0, 0.0]) -> None |
| `def setLensPosition(self, cameraId: CameraBoardSocket, lensPosition: int) -> None` | `(self, cameraId: CameraBoardSocket, lensPosition: int)` | L2205 | setLensPosition(self: depthai.CalibrationHandler, cameraId: depthai.CameraBoardSocket, lensPosition: int) -> None |
| `def setProductName(self, productName: str) -> None` | `(self, productName: str)` | L2216 | setProductName(self: depthai.CalibrationHandler, productName: str) -> None |
| `def setStereoLeft(self, cameraId: CameraBoardSocket, rectifiedRotation: list[list[float]]) -> None` | `(self, cameraId: CameraBoardSocket, rectifiedRotation: list[list[float]])` | L2224 | setStereoLeft(self: depthai.CalibrationHandler, cameraId: depthai.CameraBoardSocket, rectifiedRotation: list[list[float]]) -> None |
| `def setStereoRight(self, cameraId: CameraBoardSocket, rectifiedRotation: list[list[float]]) -> None` | `(self, cameraId: CameraBoardSocket, rectifiedRotation: list[list[float]])` | L2238 | setStereoRight(self: depthai.CalibrationHandler, cameraId: depthai.CameraBoardSocket, rectifiedRotation: list[list[float]]) -> None |
| `def validateCalibrationHandler(self, throwOnError: bool = ...) -> None` | `(self, throwOnError: bool = ...)` | L2252 | validateCalibrationHandler(self: depthai.CalibrationHandler, throwOnError: bool = True) -> None |

<a id="class-calibrationquality"></a>
### class `CalibrationQuality(Buffer)`  — L2262

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `info` | `str` | — | L2263 |
| `qualityData` | `CalibrationQualityData | None` | — | L2264 |

**🔧 Dunder Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L2266 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, qualityData: CalibrationQualityData, info: str) -> None` | `(self, qualityData: CalibrationQualityData, info: str)` | L2277 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, info: str) -> None` | `(self, info: str)` | L2288 | __init__(*args, **kwargs) |

<a id="class-calibrationqualitydata"></a>
### class `CalibrationQualityData`  — L2299

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `depthErrorDifference` | `list[float]` | — | L2300 |
| `rotationChange` | `Incomplete` | — | L2301 |
| `sampsonErrorCurrent` | `float` | — | L2302 |
| `sampsonErrorNew` | `float` | — | L2303 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L2304 | __init__(self: depthai.CalibrationQualityData) -> None |

<a id="class-cameraboardsocket"></a>
### class `CameraBoardSocket`  — L2307

> Which Camera socket to use.

AUTO denotes that the decision will be made by device

Members:

  AUTO

  CAM_A

  CAM_B

  CAM_C

  CAM_D

  VERTICAL

  CAM_E

  CAM_F

  CAM_G

  CAM_H

  RGB : **Deprecated:** Use CAM_A or address camera by name instead

  LEFT : **Deprecated:** Use CAM_B or address camera by name instead

  RIGHT : **Deprecated:** Use CAM_C or address camera by name instead

  CENTER : **Deprecated:** Use CAM_A or address camera by name instead

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `CENTER` | `ClassVar[CameraBoardSocket]` | `...` | L2341 |
| `LEFT` | `ClassVar[CameraBoardSocket]` | `...` | L2342 |
| `RGB` | `ClassVar[CameraBoardSocket]` | `...` | L2343 |
| `RIGHT` | `ClassVar[CameraBoardSocket]` | `...` | L2344 |
| `__members__` | `ClassVar[dict]` | `...` | L2345 |
| `AUTO` | `ClassVar[CameraBoardSocket]` | `...` | L2346 |
| `CAM_A` | `ClassVar[CameraBoardSocket]` | `...` | L2347 |
| `CAM_B` | `ClassVar[CameraBoardSocket]` | `...` | L2348 |
| `CAM_C` | `ClassVar[CameraBoardSocket]` | `...` | L2349 |
| `CAM_D` | `ClassVar[CameraBoardSocket]` | `...` | L2350 |
| `CAM_E` | `ClassVar[CameraBoardSocket]` | `...` | L2351 |
| `CAM_F` | `ClassVar[CameraBoardSocket]` | `...` | L2352 |
| `CAM_G` | `ClassVar[CameraBoardSocket]` | `...` | L2353 |
| `CAM_H` | `ClassVar[CameraBoardSocket]` | `...` | L2354 |
| `VERTICAL` | `ClassVar[CameraBoardSocket]` | `...` | L2355 |
| `__entries` | `ClassVar[dict]` | `...` | L2356 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L2357 | __init__(self: depthai.CameraBoardSocket, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L2359 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L2361 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L2363 | __index__(self: depthai.CameraBoardSocket) -> int |
| `def __int__(self) -> int` | `(self)` | L2365 | __int__(self: depthai.CameraBoardSocket) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L2367 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L2370 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L2376 | (arg0: depthai.CameraBoardSocket) -> int |

<a id="class-cameracontrol"></a>
### class `CameraControl(Buffer)`  — L2379

> CameraControl message. Specifies various camera control commands like:

- Still capture

- Auto/manual focus

- Auto/manual white balance

- Auto/manual exposure

- Anti banding

- ...

By default the camera enables 3A, with auto-focus in `CONTINUOUS_VIDEO` mode,
auto-white-balance in `AUTO` mode, and auto-exposure with anti-banding for 50Hz
mains frequency.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `aeLockMode` | `bool` | — | L2928 |
| `aeMaxExposureTimeUs` | `int` | — | L2929 |
| `afRegion` | `Incomplete` | — | L2930 |
| `antiBandingMode` | `CameraControl.AntiBandingMode` | — | L2931 |
| `autoFocusMode` | `CameraControl.AutoFocusMode` | — | L2932 |
| `awbLockMode` | `bool` | — | L2933 |
| `awbMode` | `CameraControl.AutoWhiteBalanceMode` | — | L2934 |
| `brightness` | `int` | — | L2935 |
| `captureIntent` | `CameraControl.CaptureIntent` | — | L2936 |
| `chromaDenoise` | `int` | — | L2937 |
| `cmdMask` | `int` | — | L2938 |
| `contrast` | `int` | — | L2939 |
| `controlMode` | `CameraControl.ControlMode` | — | L2940 |
| `effectMode` | `CameraControl.EffectMode` | — | L2941 |
| `expCompensation` | `int` | — | L2942 |
| `expManual` | `Incomplete` | — | L2943 |
| `lensPosition` | `int` | — | L2944 |
| `lumaDenoise` | `int` | — | L2945 |
| `saturation` | `int` | — | L2946 |
| `sceneMode` | `CameraControl.SceneMode` | — | L2947 |
| `sharpness` | `int` | — | L2948 |
| `wbColorTemp` | `int` | — | L2949 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L2951 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self) -> None` | `(self)` | L2960 | __init__(*args, **kwargs) |

**🔹 Public Methods (51):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def clearCommand(self, arg0: CameraControl.Command) -> None` | `(self, arg0: CameraControl.Command)` | L2968 | clearCommand(self: depthai.CameraControl, arg0: depthai.CameraControl.Command) -> None |
| `def clearMiscControls(self) -> None` | `(self)` | L2970 | clearMiscControls(self: depthai.CameraControl) -> None |
| `def getCaptureStill(self) -> bool` | `(self)` | L2975 | getCaptureStill(self: depthai.CameraControl) -> bool |
| `def getCommand(self, arg0: CameraControl.Command) -> bool` | `(self, arg0: CameraControl.Command)` | L2983 | getCommand(self: depthai.CameraControl, arg0: depthai.CameraControl.Command) -> bool |
| `def getExposureTime(self) -> datetime.timedelta` | `(self)` | L2985 | getExposureTime(self: depthai.CameraControl) -> datetime.timedelta |
| `def getHdr(self) -> bool` | `(self)` | L2990 | getHdr(self: depthai.CameraControl) -> bool |
| `def getLensPosition(self) -> int` | `(self)` | L2998 | getLensPosition(self: depthai.CameraControl) -> int |
| `def getLensPositionRaw(self) -> float` | `(self)` | L3003 | getLensPositionRaw(self: depthai.CameraControl) -> float |
| `def getMiscControls(self) -> list[tuple[str, str]]` | `(self)` | L3008 | getMiscControls(self: depthai.CameraControl) -> list[tuple[str, str]] |
| `def getSensitivity(self) -> int` | `(self)` | L3016 | getSensitivity(self: depthai.CameraControl) -> int |
| `def setAntiBandingMode(self, mode: CameraControl.AntiBandingMode) -> CameraControl` | `(self, mode: CameraControl.AntiBandingMode)` | L3021 | setAntiBandingMode(self: depthai.CameraControl, mode: depthai.CameraControl.AntiBandingMode) -> depthai.CameraControl |
| `def setAutoExposureCompensation(self, compensation: int) -> CameraControl` | `(self, compensation: int)` | L3035 | setAutoExposureCompensation(self: depthai.CameraControl, compensation: int) -> depthai.CameraControl |
| `def setAutoExposureEnable(self) -> CameraControl` | `(self)` | L3045 | setAutoExposureEnable(self: depthai.CameraControl) -> depthai.CameraControl |
| `@overload` `def setAutoExposureLimit(self, maxExposureTimeUs: int) -> CameraControl` | `(self, maxExposureTimeUs: int)` | L3051 | setAutoExposureLimit(*args, **kwargs) |
| `@overload` `def setAutoExposureLimit(self, maxExposureTime: datetime.timedelta) -> CameraControl` | `(self, maxExposureTime: datetime.timedelta)` | L3074 | setAutoExposureLimit(*args, **kwargs) |
| `def setAutoExposureLock(self, lock: bool) -> CameraControl` | `(self, lock: bool)` | L3096 | setAutoExposureLock(self: depthai.CameraControl, lock: bool) -> depthai.CameraControl |
| `def setAutoExposureRegion(self, startX: int, startY: int, width: int, height: int) -> CameraControl` | `(self, startX: int, startY: int, width: int, height: int)` | L3105 | setAutoExposureRegion(self: depthai.CameraControl, startX: int, startY: int, width: int, height: int) -> depthai.CameraControl |
| `def setAutoFocusLensRange(self, infinityPosition: int, macroPosition: int) -> CameraControl` | `(self, infinityPosition: int, macroPosition: int)` | L3123 | setAutoFocusLensRange(self: depthai.CameraControl, infinityPosition: int, macroPosition: int) -> depthai.CameraControl |
| `def setAutoFocusMode(self, mode: CameraControl.AutoFocusMode) -> CameraControl` | `(self, mode: CameraControl.AutoFocusMode)` | L3130 | setAutoFocusMode(self: depthai.CameraControl, mode: depthai.CameraControl.AutoFocusMode) -> depthai.CameraControl |
| `def setAutoFocusRegion(self, startX: int, startY: int, width: int, height: int) -> CameraControl` | `(self, startX: int, startY: int, width: int, height: int)` | L3135 | setAutoFocusRegion(self: depthai.CameraControl, startX: int, startY: int, width: int, height: int) -> depthai.CameraControl |
| `def setAutoFocusTrigger(self) -> CameraControl` | `(self)` | L3153 | setAutoFocusTrigger(self: depthai.CameraControl) -> depthai.CameraControl |
| `def setAutoWhiteBalanceLock(self, lock: bool) -> CameraControl` | `(self, lock: bool)` | L3158 | setAutoWhiteBalanceLock(self: depthai.CameraControl, lock: bool) -> depthai.CameraControl |
| `def setAutoWhiteBalanceMode(self, mode: CameraControl.AutoWhiteBalanceMode) -> CameraControl` | `(self, mode: CameraControl.AutoWhiteBalanceMode)` | L3166 | setAutoWhiteBalanceMode(self: depthai.CameraControl, mode: depthai.CameraControl.AutoWhiteBalanceMode) -> depthai.CameraControl |
| `def setBrightness(self, value: int) -> CameraControl` | `(self, value: int)` | L3174 | setBrightness(self: depthai.CameraControl, value: int) -> depthai.CameraControl |
| `def setCaptureIntent(self, mode: CameraControl.CaptureIntent) -> CameraControl` | `(self, mode: CameraControl.CaptureIntent)` | L3182 | setCaptureIntent(self: depthai.CameraControl, mode: depthai.CameraControl.CaptureIntent) -> depthai.CameraControl |
| `def setCaptureStill(self, capture: bool) -> CameraControl` | `(self, capture: bool)` | L3190 | setCaptureStill(self: depthai.CameraControl, capture: bool) -> depthai.CameraControl |
| `def setChromaDenoise(self, value: int) -> CameraControl` | `(self, value: int)` | L3195 | setChromaDenoise(self: depthai.CameraControl, value: int) -> depthai.CameraControl |
| `def setCommand(self, arg0: CameraControl.Command, arg1: bool) -> None` | `(self, arg0: CameraControl.Command, arg1: bool)` | L3203 | setCommand(self: depthai.CameraControl, arg0: depthai.CameraControl.Command, arg1: bool) -> None |
| `def setContrast(self, value: int) -> CameraControl` | `(self, value: int)` | L3205 | setContrast(self: depthai.CameraControl, value: int) -> depthai.CameraControl |
| `def setControlMode(self, mode: CameraControl.ControlMode) -> CameraControl` | `(self, mode: CameraControl.ControlMode)` | L3213 | setControlMode(self: depthai.CameraControl, mode: depthai.CameraControl.ControlMode) -> depthai.CameraControl |
| `def setEffectMode(self, mode: CameraControl.EffectMode) -> CameraControl` | `(self, mode: CameraControl.EffectMode)` | L3221 | setEffectMode(self: depthai.CameraControl, mode: depthai.CameraControl.EffectMode) -> depthai.CameraControl |
| `def setExternalTrigger(self, numFramesBurst: int, numFramesDiscard: int) -> CameraControl` | `(self, numFramesBurst: int, numFramesDiscard: int)` | L3229 | setExternalTrigger(self: depthai.CameraControl, numFramesBurst: int, numFramesDiscard: int) -> depthai.CameraControl |
| `def setFrameSyncMode(self, mode: CameraControl.FrameSyncMode) -> CameraControl` | `(self, mode: CameraControl.FrameSyncMode)` | L3238 | setFrameSyncMode(self: depthai.CameraControl, mode: depthai.CameraControl.FrameSyncMode) -> depthai.CameraControl |
| `def setHdr(self, enable: bool) -> CameraControl` | `(self, enable: bool)` | L3244 | setHdr(self: depthai.CameraControl, enable: bool) -> depthai.CameraControl |
| `def setLumaDenoise(self, value: int) -> CameraControl` | `(self, value: int)` | L3252 | setLumaDenoise(self: depthai.CameraControl, value: int) -> depthai.CameraControl |
| `@overload` `def setManualExposure(self, exposureTimeUs: int, sensitivityIso: int) -> CameraControl` | `(self, exposureTimeUs: int, sensitivityIso: int)` | L3261 | setManualExposure(*args, **kwargs) |
| `@overload` `def setManualExposure(self, exposureTime: datetime.timedelta, sensitivityIso: int) -> CameraControl` | `(self, exposureTime: datetime.timedelta, sensitivityIso: int)` | L3286 | setManualExposure(*args, **kwargs) |
| `def setManualFocus(self, lensPosition: int) -> CameraControl` | `(self, lensPosition: int)` | L3310 | setManualFocus(self: depthai.CameraControl, lensPosition: int) -> depthai.CameraControl |
| `def setManualFocusRaw(self, lensPositionRaw: float) -> CameraControl` | `(self, lensPositionRaw: float)` | L3318 | setManualFocusRaw(self: depthai.CameraControl, lensPositionRaw: float) -> depthai.CameraControl |
| `def setManualWhiteBalance(self, colorTemperatureK: int) -> CameraControl` | `(self, colorTemperatureK: int)` | L3329 | setManualWhiteBalance(self: depthai.CameraControl, colorTemperatureK: int) -> depthai.CameraControl |
| `@overload` `def setMisc(self, control: str, value: str) -> CameraControl` | `(self, control: str, value: str)` | L3338 | setMisc(*args, **kwargs) |
| `@overload` `def setMisc(self, control: str, value: int) -> CameraControl` | `(self, control: str, value: int)` | L3376 | setMisc(*args, **kwargs) |
| `@overload` `def setMisc(self, control: str, value: float) -> CameraControl` | `(self, control: str, value: float)` | L3414 | setMisc(*args, **kwargs) |
| `def setSaturation(self, value: int) -> CameraControl` | `(self, value: int)` | L3451 | setSaturation(self: depthai.CameraControl, value: int) -> depthai.CameraControl |
| `def setSceneMode(self, mode: CameraControl.SceneMode) -> CameraControl` | `(self, mode: CameraControl.SceneMode)` | L3459 | setSceneMode(self: depthai.CameraControl, mode: depthai.CameraControl.SceneMode) -> depthai.CameraControl |
| `def setSharpness(self, value: int) -> CameraControl` | `(self, value: int)` | L3467 | setSharpness(self: depthai.CameraControl, value: int) -> depthai.CameraControl |
| `def setStartStreaming(self) -> CameraControl` | `(self)` | L3475 | setStartStreaming(self: depthai.CameraControl) -> depthai.CameraControl |
| `def setStopStreaming(self) -> CameraControl` | `(self)` | L3480 | setStopStreaming(self: depthai.CameraControl) -> depthai.CameraControl |
| `def setStrobeDisable(self) -> CameraControl` | `(self)` | L3485 | setStrobeDisable(self: depthai.CameraControl) -> depthai.CameraControl |
| `def setStrobeExternal(self, gpioNumber: int, activeLevel: int) -> CameraControl` | `(self, gpioNumber: int, activeLevel: int)` | L3490 | setStrobeExternal(self: depthai.CameraControl, gpioNumber: int, activeLevel: int) -> depthai.CameraControl |
| `def setStrobeSensor(self, activeLevel: int) -> CameraControl` | `(self, activeLevel: int)` | L3497 | setStrobeSensor(self: depthai.CameraControl, activeLevel: int) -> depthai.CameraControl |

**Nested Class:**

<a id="class-antibandingmode"></a>
#### class `AntiBandingMode`  — L2398

> Members:

  OFF

  MAINS_50_HZ

  MAINS_60_HZ

  AUTO

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L2410 |
| `AUTO` | `ClassVar[CameraControl.AntiBandingMode]` | `...` | L2411 |
| `MAINS_50_HZ` | `ClassVar[CameraControl.AntiBandingMode]` | `...` | L2412 |
| `MAINS_60_HZ` | `ClassVar[CameraControl.AntiBandingMode]` | `...` | L2413 |
| `OFF` | `ClassVar[CameraControl.AntiBandingMode]` | `...` | L2414 |
| `__entries` | `ClassVar[dict]` | `...` | L2415 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L2416 | __init__(self: depthai.CameraControl.AntiBandingMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L2418 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L2420 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L2422 | __index__(self: depthai.CameraControl.AntiBandingMode) -> int |
| `def __int__(self) -> int` | `(self)` | L2424 | __int__(self: depthai.CameraControl.AntiBandingMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L2426 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L2429 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L2435 | (arg0: depthai.CameraControl.AntiBandingMode) -> int |

**Nested Class:**

<a id="class-autofocusmode"></a>
#### class `AutoFocusMode`  — L2438

> Members:

  OFF

  AUTO

  MACRO

  CONTINUOUS_VIDEO

  CONTINUOUS_PICTURE

  EDOF

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L2454 |
| `AUTO` | `ClassVar[CameraControl.AutoFocusMode]` | `...` | L2455 |
| `CONTINUOUS_PICTURE` | `ClassVar[CameraControl.AutoFocusMode]` | `...` | L2456 |
| `CONTINUOUS_VIDEO` | `ClassVar[CameraControl.AutoFocusMode]` | `...` | L2457 |
| `EDOF` | `ClassVar[CameraControl.AutoFocusMode]` | `...` | L2458 |
| `MACRO` | `ClassVar[CameraControl.AutoFocusMode]` | `...` | L2459 |
| `OFF` | `ClassVar[CameraControl.AutoFocusMode]` | `...` | L2460 |
| `__entries` | `ClassVar[dict]` | `...` | L2461 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L2462 | __init__(self: depthai.CameraControl.AutoFocusMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L2464 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L2466 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L2468 | __index__(self: depthai.CameraControl.AutoFocusMode) -> int |
| `def __int__(self) -> int` | `(self)` | L2470 | __int__(self: depthai.CameraControl.AutoFocusMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L2472 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L2475 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L2481 | (arg0: depthai.CameraControl.AutoFocusMode) -> int |

**Nested Class:**

<a id="class-autowhitebalancemode"></a>
#### class `AutoWhiteBalanceMode`  — L2484

> Members:

  OFF

  AUTO

  INCANDESCENT

  FLUORESCENT

  WARM_FLUORESCENT

  DAYLIGHT

  CLOUDY_DAYLIGHT

  TWILIGHT

  SHADE

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L2506 |
| `AUTO` | `ClassVar[CameraControl.AutoWhiteBalanceMode]` | `...` | L2507 |
| `CLOUDY_DAYLIGHT` | `ClassVar[CameraControl.AutoWhiteBalanceMode]` | `...` | L2508 |
| `DAYLIGHT` | `ClassVar[CameraControl.AutoWhiteBalanceMode]` | `...` | L2509 |
| `FLUORESCENT` | `ClassVar[CameraControl.AutoWhiteBalanceMode]` | `...` | L2510 |
| `INCANDESCENT` | `ClassVar[CameraControl.AutoWhiteBalanceMode]` | `...` | L2511 |
| `OFF` | `ClassVar[CameraControl.AutoWhiteBalanceMode]` | `...` | L2512 |
| `SHADE` | `ClassVar[CameraControl.AutoWhiteBalanceMode]` | `...` | L2513 |
| `TWILIGHT` | `ClassVar[CameraControl.AutoWhiteBalanceMode]` | `...` | L2514 |
| `WARM_FLUORESCENT` | `ClassVar[CameraControl.AutoWhiteBalanceMode]` | `...` | L2515 |
| `__entries` | `ClassVar[dict]` | `...` | L2516 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L2517 | __init__(self: depthai.CameraControl.AutoWhiteBalanceMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L2519 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L2521 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L2523 | __index__(self: depthai.CameraControl.AutoWhiteBalanceMode) -> int |
| `def __int__(self) -> int` | `(self)` | L2525 | __int__(self: depthai.CameraControl.AutoWhiteBalanceMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L2527 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L2530 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L2536 | (arg0: depthai.CameraControl.AutoWhiteBalanceMode) -> int |

**Nested Class:**

<a id="class-captureintent"></a>
#### class `CaptureIntent`  — L2539

> Members:

  CUSTOM

  PREVIEW

  STILL_CAPTURE

  VIDEO_RECORD

  VIDEO_SNAPSHOT

  ZERO_SHUTTER_LAG

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L2555 |
| `CUSTOM` | `ClassVar[CameraControl.CaptureIntent]` | `...` | L2556 |
| `PREVIEW` | `ClassVar[CameraControl.CaptureIntent]` | `...` | L2557 |
| `STILL_CAPTURE` | `ClassVar[CameraControl.CaptureIntent]` | `...` | L2558 |
| `VIDEO_RECORD` | `ClassVar[CameraControl.CaptureIntent]` | `...` | L2559 |
| `VIDEO_SNAPSHOT` | `ClassVar[CameraControl.CaptureIntent]` | `...` | L2560 |
| `ZERO_SHUTTER_LAG` | `ClassVar[CameraControl.CaptureIntent]` | `...` | L2561 |
| `__entries` | `ClassVar[dict]` | `...` | L2562 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L2563 | __init__(self: depthai.CameraControl.CaptureIntent, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L2565 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L2567 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L2569 | __index__(self: depthai.CameraControl.CaptureIntent) -> int |
| `def __int__(self) -> int` | `(self)` | L2571 | __int__(self: depthai.CameraControl.CaptureIntent) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L2573 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L2576 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L2582 | (arg0: depthai.CameraControl.CaptureIntent) -> int |

**Nested Class:**

<a id="class-command"></a>
#### class `Command`  — L2585

> Members:

  START_STREAM

  STOP_STREAM

  STILL_CAPTURE

  MOVE_LENS

  AF_TRIGGER

  AE_MANUAL

  AE_AUTO

  AWB_MODE

  SCENE_MODE

  ANTIBANDING_MODE

  EXPOSURE_COMPENSATION

  AE_LOCK

  AE_TARGET_FPS_RANGE

  AWB_LOCK

  CAPTURE_INTENT

  CONTROL_MODE

  FRAME_DURATION

  SENSITIVITY

  EFFECT_MODE

  AF_MODE

  NOISE_REDUCTION_STRENGTH

  SATURATION

  BRIGHTNESS

  STREAM_FORMAT

  RESOLUTION

  SHARPNESS

  CUSTOM_USECASE

  CUSTOM_CAPT_MODE

  CUSTOM_EXP_BRACKETS

  CUSTOM_CAPTURE

  CONTRAST

  AE_REGION

  AF_REGION

  LUMA_DENOISE

  CHROMA_DENOISE

  WB_COLOR_TEMP

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L2661 |
| `AE_AUTO` | `ClassVar[CameraControl.Command]` | `...` | L2662 |
| `AE_LOCK` | `ClassVar[CameraControl.Command]` | `...` | L2663 |
| `AE_MANUAL` | `ClassVar[CameraControl.Command]` | `...` | L2664 |
| `AE_REGION` | `ClassVar[CameraControl.Command]` | `...` | L2665 |
| `AE_TARGET_FPS_RANGE` | `ClassVar[CameraControl.Command]` | `...` | L2666 |
| `AF_MODE` | `ClassVar[CameraControl.Command]` | `...` | L2667 |
| `AF_REGION` | `ClassVar[CameraControl.Command]` | `...` | L2668 |
| `AF_TRIGGER` | `ClassVar[CameraControl.Command]` | `...` | L2669 |
| `ANTIBANDING_MODE` | `ClassVar[CameraControl.Command]` | `...` | L2670 |
| `AWB_LOCK` | `ClassVar[CameraControl.Command]` | `...` | L2671 |
| `AWB_MODE` | `ClassVar[CameraControl.Command]` | `...` | L2672 |
| `BRIGHTNESS` | `ClassVar[CameraControl.Command]` | `...` | L2673 |
| `CAPTURE_INTENT` | `ClassVar[CameraControl.Command]` | `...` | L2674 |
| `CHROMA_DENOISE` | `ClassVar[CameraControl.Command]` | `...` | L2675 |
| `CONTRAST` | `ClassVar[CameraControl.Command]` | `...` | L2676 |
| `CONTROL_MODE` | `ClassVar[CameraControl.Command]` | `...` | L2677 |
| `CUSTOM_CAPTURE` | `ClassVar[CameraControl.Command]` | `...` | L2678 |
| `CUSTOM_CAPT_MODE` | `ClassVar[CameraControl.Command]` | `...` | L2679 |
| `CUSTOM_EXP_BRACKETS` | `ClassVar[CameraControl.Command]` | `...` | L2680 |
| `CUSTOM_USECASE` | `ClassVar[CameraControl.Command]` | `...` | L2681 |
| `EFFECT_MODE` | `ClassVar[CameraControl.Command]` | `...` | L2682 |
| `EXPOSURE_COMPENSATION` | `ClassVar[CameraControl.Command]` | `...` | L2683 |
| `FRAME_DURATION` | `ClassVar[CameraControl.Command]` | `...` | L2684 |
| `LUMA_DENOISE` | `ClassVar[CameraControl.Command]` | `...` | L2685 |
| `MOVE_LENS` | `ClassVar[CameraControl.Command]` | `...` | L2686 |
| `NOISE_REDUCTION_STRENGTH` | `ClassVar[CameraControl.Command]` | `...` | L2687 |
| `RESOLUTION` | `ClassVar[CameraControl.Command]` | `...` | L2688 |
| `SATURATION` | `ClassVar[CameraControl.Command]` | `...` | L2689 |
| `SCENE_MODE` | `ClassVar[CameraControl.Command]` | `...` | L2690 |
| `SENSITIVITY` | `ClassVar[CameraControl.Command]` | `...` | L2691 |
| `SHARPNESS` | `ClassVar[CameraControl.Command]` | `...` | L2692 |
| `START_STREAM` | `ClassVar[CameraControl.Command]` | `...` | L2693 |
| `STILL_CAPTURE` | `ClassVar[CameraControl.Command]` | `...` | L2694 |
| `STOP_STREAM` | `ClassVar[CameraControl.Command]` | `...` | L2695 |
| `STREAM_FORMAT` | `ClassVar[CameraControl.Command]` | `...` | L2696 |
| `WB_COLOR_TEMP` | `ClassVar[CameraControl.Command]` | `...` | L2697 |
| `__entries` | `ClassVar[dict]` | `...` | L2698 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L2699 | __init__(self: depthai.CameraControl.Command, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L2701 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L2703 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L2705 | __index__(self: depthai.CameraControl.Command) -> int |
| `def __int__(self) -> int` | `(self)` | L2707 | __int__(self: depthai.CameraControl.Command) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L2709 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L2712 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L2718 | (arg0: depthai.CameraControl.Command) -> int |

**Nested Class:**

<a id="class-controlmode"></a>
#### class `ControlMode`  — L2721

> Members:

  OFF

  AUTO

  USE_SCENE_MODE

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L2731 |
| `AUTO` | `ClassVar[CameraControl.ControlMode]` | `...` | L2732 |
| `OFF` | `ClassVar[CameraControl.ControlMode]` | `...` | L2733 |
| `USE_SCENE_MODE` | `ClassVar[CameraControl.ControlMode]` | `...` | L2734 |
| `__entries` | `ClassVar[dict]` | `...` | L2735 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L2736 | __init__(self: depthai.CameraControl.ControlMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L2738 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L2740 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L2742 | __index__(self: depthai.CameraControl.ControlMode) -> int |
| `def __int__(self) -> int` | `(self)` | L2744 | __int__(self: depthai.CameraControl.ControlMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L2746 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L2749 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L2755 | (arg0: depthai.CameraControl.ControlMode) -> int |

**Nested Class:**

<a id="class-effectmode"></a>
#### class `EffectMode`  — L2758

> Members:

  OFF

  MONO

  NEGATIVE

  SOLARIZE

  SEPIA

  POSTERIZE

  WHITEBOARD

  BLACKBOARD

  AQUA

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L2780 |
| `AQUA` | `ClassVar[CameraControl.EffectMode]` | `...` | L2781 |
| `BLACKBOARD` | `ClassVar[CameraControl.EffectMode]` | `...` | L2782 |
| `MONO` | `ClassVar[CameraControl.EffectMode]` | `...` | L2783 |
| `NEGATIVE` | `ClassVar[CameraControl.EffectMode]` | `...` | L2784 |
| `OFF` | `ClassVar[CameraControl.EffectMode]` | `...` | L2785 |
| `POSTERIZE` | `ClassVar[CameraControl.EffectMode]` | `...` | L2786 |
| `SEPIA` | `ClassVar[CameraControl.EffectMode]` | `...` | L2787 |
| `SOLARIZE` | `ClassVar[CameraControl.EffectMode]` | `...` | L2788 |
| `WHITEBOARD` | `ClassVar[CameraControl.EffectMode]` | `...` | L2789 |
| `__entries` | `ClassVar[dict]` | `...` | L2790 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L2791 | __init__(self: depthai.CameraControl.EffectMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L2793 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L2795 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L2797 | __index__(self: depthai.CameraControl.EffectMode) -> int |
| `def __int__(self) -> int` | `(self)` | L2799 | __int__(self: depthai.CameraControl.EffectMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L2801 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L2804 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L2810 | (arg0: depthai.CameraControl.EffectMode) -> int |

**Nested Class:**

<a id="class-framesyncmode"></a>
#### class `FrameSyncMode`  — L2813

> Members:

  OFF

  OUTPUT

  INPUT

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L2823 |
| `INPUT` | `ClassVar[CameraControl.FrameSyncMode]` | `...` | L2824 |
| `OFF` | `ClassVar[CameraControl.FrameSyncMode]` | `...` | L2825 |
| `OUTPUT` | `ClassVar[CameraControl.FrameSyncMode]` | `...` | L2826 |
| `__entries` | `ClassVar[dict]` | `...` | L2827 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L2828 | __init__(self: depthai.CameraControl.FrameSyncMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L2830 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L2832 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L2834 | __index__(self: depthai.CameraControl.FrameSyncMode) -> int |
| `def __int__(self) -> int` | `(self)` | L2836 | __int__(self: depthai.CameraControl.FrameSyncMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L2838 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L2841 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L2847 | (arg0: depthai.CameraControl.FrameSyncMode) -> int |

**Nested Class:**

<a id="class-scenemode"></a>
#### class `SceneMode`  — L2850

> Members:

  UNSUPPORTED

  FACE_PRIORITY

  ACTION

  PORTRAIT

  LANDSCAPE

  NIGHT

  NIGHT_PORTRAIT

  THEATRE

  BEACH

  SNOW

  SUNSET

  STEADYPHOTO

  FIREWORKS

  SPORTS

  PARTY

  CANDLELIGHT

  BARCODE

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L2888 |
| `ACTION` | `ClassVar[CameraControl.SceneMode]` | `...` | L2889 |
| `BARCODE` | `ClassVar[CameraControl.SceneMode]` | `...` | L2890 |
| `BEACH` | `ClassVar[CameraControl.SceneMode]` | `...` | L2891 |
| `CANDLELIGHT` | `ClassVar[CameraControl.SceneMode]` | `...` | L2892 |
| `FACE_PRIORITY` | `ClassVar[CameraControl.SceneMode]` | `...` | L2893 |
| `FIREWORKS` | `ClassVar[CameraControl.SceneMode]` | `...` | L2894 |
| `LANDSCAPE` | `ClassVar[CameraControl.SceneMode]` | `...` | L2895 |
| `NIGHT` | `ClassVar[CameraControl.SceneMode]` | `...` | L2896 |
| `NIGHT_PORTRAIT` | `ClassVar[CameraControl.SceneMode]` | `...` | L2897 |
| `PARTY` | `ClassVar[CameraControl.SceneMode]` | `...` | L2898 |
| `PORTRAIT` | `ClassVar[CameraControl.SceneMode]` | `...` | L2899 |
| `SNOW` | `ClassVar[CameraControl.SceneMode]` | `...` | L2900 |
| `SPORTS` | `ClassVar[CameraControl.SceneMode]` | `...` | L2901 |
| `STEADYPHOTO` | `ClassVar[CameraControl.SceneMode]` | `...` | L2902 |
| `SUNSET` | `ClassVar[CameraControl.SceneMode]` | `...` | L2903 |
| `THEATRE` | `ClassVar[CameraControl.SceneMode]` | `...` | L2904 |
| `UNSUPPORTED` | `ClassVar[CameraControl.SceneMode]` | `...` | L2905 |
| `__entries` | `ClassVar[dict]` | `...` | L2906 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L2907 | __init__(self: depthai.CameraControl.SceneMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L2909 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L2911 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L2913 | __index__(self: depthai.CameraControl.SceneMode) -> int |
| `def __int__(self) -> int` | `(self)` | L2915 | __int__(self: depthai.CameraControl.SceneMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L2917 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L2920 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L2926 | (arg0: depthai.CameraControl.SceneMode) -> int |

<a id="class-cameraexposureoffset"></a>
### class `CameraExposureOffset`  — L3504

> Members:

START

MIDDLE

END

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L3512 |
| `END` | `ClassVar[CameraExposureOffset]` | `...` | L3513 |
| `MIDDLE` | `ClassVar[CameraExposureOffset]` | `...` | L3514 |
| `START` | `ClassVar[CameraExposureOffset]` | `...` | L3515 |
| `__entries` | `ClassVar[dict]` | `...` | L3516 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L3517 | __init__(self: depthai.CameraExposureOffset, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L3519 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L3521 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L3523 | __index__(self: depthai.CameraExposureOffset) -> int |
| `def __int__(self) -> int` | `(self)` | L3525 | __int__(self: depthai.CameraExposureOffset) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L3527 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L3530 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L3536 | (arg0: depthai.CameraExposureOffset) -> int |

<a id="class-camerafeatures"></a>
### class `CameraFeatures`  — L3539

> CameraFeatures structure

Characterizes detected cameras on board

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `calibrationResolution` | `CameraSensorConfig | None` | — | L3543 |
| `configs` | `list[CameraSensorConfig]` | — | L3544 |
| `hasAutofocus` | `bool` | — | L3545 |
| `hasAutofocusIC` | `bool` | — | L3546 |
| `height` | `int` | — | L3547 |
| `name` | `str` | — | L3548 |
| `orientation` | `CameraImageOrientation` | — | L3549 |
| `sensorName` | `str` | — | L3550 |
| `socket` | `CameraBoardSocket` | — | L3551 |
| `supportedTypes` | `list[CameraSensorType]` | — | L3552 |
| `width` | `int` | — | L3553 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L3554 | __init__(self: depthai.CameraFeatures) -> None |

<a id="class-cameraimageorientation"></a>
### class `CameraImageOrientation`  — L3557

> Camera sensor image orientation / pixel readout. This exposes direct sensor
settings. 90 or 270 degrees rotation is not available.

AUTO denotes that the decision will be made by device (e.g. on OAK-1/megaAI:
ROTATE_180_DEG).

Members:

  AUTO

  NORMAL

  HORIZONTAL_MIRROR

  VERTICAL_FLIP

  ROTATE_180_DEG

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L3575 |
| `AUTO` | `ClassVar[CameraImageOrientation]` | `...` | L3576 |
| `HORIZONTAL_MIRROR` | `ClassVar[CameraImageOrientation]` | `...` | L3577 |
| `NORMAL` | `ClassVar[CameraImageOrientation]` | `...` | L3578 |
| `ROTATE_180_DEG` | `ClassVar[CameraImageOrientation]` | `...` | L3579 |
| `VERTICAL_FLIP` | `ClassVar[CameraImageOrientation]` | `...` | L3580 |
| `__entries` | `ClassVar[dict]` | `...` | L3581 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L3582 | __init__(self: depthai.CameraImageOrientation, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L3584 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L3586 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L3588 | __index__(self: depthai.CameraImageOrientation) -> int |
| `def __int__(self) -> int` | `(self)` | L3590 | __int__(self: depthai.CameraImageOrientation) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L3592 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L3595 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L3601 | (arg0: depthai.CameraImageOrientation) -> int |

<a id="class-camerainfo"></a>
### class `CameraInfo`  — L3604

> CameraInfo structure

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `cameraType` | `CameraModel` | — | L3606 |
| `distortionCoeff` | `list[float]` | — | L3607 |
| `extrinsics` | `Extrinsics` | — | L3608 |
| `height` | `int` | — | L3609 |
| `intrinsicMatrix` | `list[list[float]]` | — | L3610 |
| `specHfovDeg` | `float` | — | L3611 |
| `width` | `int` | — | L3612 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L3613 | __init__(self: depthai.CameraInfo) -> None |

<a id="class-cameramodel"></a>
### class `CameraModel`  — L3616

> Which CameraModel to initialize the calibration with.

Members:

  Perspective

  Fisheye

  Equirectangular

  RadialDivision

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L3628 |
| `Equirectangular` | `ClassVar[CameraModel]` | `...` | L3629 |
| `Fisheye` | `ClassVar[CameraModel]` | `...` | L3630 |
| `Perspective` | `ClassVar[CameraModel]` | `...` | L3631 |
| `RadialDivision` | `ClassVar[CameraModel]` | `...` | L3632 |
| `__entries` | `ClassVar[dict]` | `...` | L3633 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L3634 | __init__(self: depthai.CameraModel, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L3636 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L3638 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L3640 | __index__(self: depthai.CameraModel) -> int |
| `def __int__(self) -> int` | `(self)` | L3642 | __int__(self: depthai.CameraModel) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L3644 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L3647 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L3653 | (arg0: depthai.CameraModel) -> int |

<a id="class-camerasensorconfig"></a>
### class `CameraSensorConfig`  — L3656

> Sensor config

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `fov` | `Rect` | — | L3658 |
| `height` | `int` | — | L3659 |
| `maxFps` | `float` | — | L3660 |
| `minFps` | `float` | — | L3661 |
| `type` | `CameraSensorType` | — | L3662 |
| `width` | `int` | — | L3663 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L3664 | __init__(self: depthai.CameraSensorConfig) -> None |

<a id="class-camerasensortype"></a>
### class `CameraSensorType`  — L3667

> Camera sensor type

Members:

  COLOR

  MONO

  TOF

  THERMAL

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L3679 |
| `COLOR` | `ClassVar[CameraSensorType]` | `...` | L3680 |
| `MONO` | `ClassVar[CameraSensorType]` | `...` | L3681 |
| `THERMAL` | `ClassVar[CameraSensorType]` | `...` | L3682 |
| `TOF` | `ClassVar[CameraSensorType]` | `...` | L3683 |
| `__entries` | `ClassVar[dict]` | `...` | L3684 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L3685 | __init__(self: depthai.CameraSensorType, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L3687 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L3689 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L3691 | __index__(self: depthai.CameraSensorType) -> int |
| `def __int__(self) -> int` | `(self)` | L3693 | __int__(self: depthai.CameraSensorType) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L3695 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L3698 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L3704 | (arg0: depthai.CameraSensorType) -> int |

<a id="class-capability"></a>
### class `Capability`  — L3707

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L3708 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-capabilityrangefloat"></a>
### class `CapabilityRangeFloat`  — L3711

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L3712 | Initialize self.  See help(type(self)) for accurate signature. |

**🔹 Public Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def discrete(self, arg0: list[float]) -> None` | `(self, arg0: list[float])` | L3714 | discrete(self: depthai.CapabilityRangeFloat, arg0: list[float]) -> None |
| `def fixed(self, arg0: float) -> None` | `(self, arg0: float)` | L3716 | fixed(self: depthai.CapabilityRangeFloat, arg0: float) -> None |
| `@overload` `def minMax(self, arg0: tuple[float, float]) -> None` | `(self, arg0: tuple[float, float])` | L3719 | minMax(*args, **kwargs) |
| `@overload` `def minMax(self, arg0: tuple[float, float]) -> None` | `(self, arg0: tuple[float, float])` | L3730 | minMax(*args, **kwargs) |
| `@overload` `def minMax(self, arg0: float, arg1: float) -> None` | `(self, arg0: float, arg1: float)` | L3741 | minMax(*args, **kwargs) |

<a id="class-capabilityrangefloatpair"></a>
### class `CapabilityRangeFloatPair`  — L3752

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L3753 | Initialize self.  See help(type(self)) for accurate signature. |

**🔹 Public Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def discrete(self, arg0: list[tuple[float, float]]) -> None` | `(self, arg0: list[tuple[float, float]])` | L3755 | discrete(self: depthai.CapabilityRangeFloatPair, arg0: list[tuple[float, float]]) -> None |
| `def fixed(self, arg0: tuple[float, float]) -> None` | `(self, arg0: tuple[float, float])` | L3757 | fixed(self: depthai.CapabilityRangeFloatPair, arg0: tuple[float, float]) -> None |
| `@overload` `def minMax(self, arg0: tuple[tuple[float, float], tuple[float, float]]) -> None` | `(self, arg0: tuple[tuple[float, float], tuple[float, float]])` | L3760 | minMax(*args, **kwargs) |
| `@overload` `def minMax(self, arg0: tuple[tuple[float, float], tuple[float, float]]) -> None` | `(self, arg0: tuple[tuple[float, float], tuple[float, float]])` | L3771 | minMax(*args, **kwargs) |
| `@overload` `def minMax(self, arg0: tuple[float, float], arg1: tuple[float, float]) -> None` | `(self, arg0: tuple[float, float], arg1: tuple[float, float])` | L3782 | minMax(*args, **kwargs) |

<a id="class-capabilityrangeuint"></a>
### class `CapabilityRangeUint`  — L3793

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L3794 | Initialize self.  See help(type(self)) for accurate signature. |

**🔹 Public Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def discrete(self, arg0: list[int]) -> None` | `(self, arg0: list[int])` | L3796 | discrete(self: depthai.CapabilityRangeUint, arg0: list[int]) -> None |
| `def fixed(self, arg0: int) -> None` | `(self, arg0: int)` | L3798 | fixed(self: depthai.CapabilityRangeUint, arg0: int) -> None |
| `@overload` `def minMax(self, arg0: tuple[int, int]) -> None` | `(self, arg0: tuple[int, int])` | L3801 | minMax(*args, **kwargs) |
| `@overload` `def minMax(self, arg0: tuple[int, int]) -> None` | `(self, arg0: tuple[int, int])` | L3812 | minMax(*args, **kwargs) |
| `@overload` `def minMax(self, arg0: int, arg1: int) -> None` | `(self, arg0: int, arg1: int)` | L3823 | minMax(*args, **kwargs) |

<a id="class-capabilityrangeuintpair"></a>
### class `CapabilityRangeUintPair`  — L3834

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L3835 | Initialize self.  See help(type(self)) for accurate signature. |

**🔹 Public Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def discrete(self, arg0: list[tuple[int, int]]) -> None` | `(self, arg0: list[tuple[int, int]])` | L3837 | discrete(self: depthai.CapabilityRangeUintPair, arg0: list[tuple[int, int]]) -> None |
| `def fixed(self, arg0: tuple[int, int]) -> None` | `(self, arg0: tuple[int, int])` | L3839 | fixed(self: depthai.CapabilityRangeUintPair, arg0: tuple[int, int]) -> None |
| `@overload` `def minMax(self, arg0: tuple[tuple[int, int], tuple[int, int]]) -> None` | `(self, arg0: tuple[tuple[int, int], tuple[int, int]])` | L3842 | minMax(*args, **kwargs) |
| `@overload` `def minMax(self, arg0: tuple[tuple[int, int], tuple[int, int]]) -> None` | `(self, arg0: tuple[tuple[int, int], tuple[int, int]])` | L3853 | minMax(*args, **kwargs) |
| `@overload` `def minMax(self, arg0: tuple[int, int], arg1: tuple[int, int]) -> None` | `(self, arg0: tuple[int, int], arg1: tuple[int, int])` | L3864 | minMax(*args, **kwargs) |

<a id="class-chiptemperature"></a>
### class `ChipTemperature`  — L3875

> Chip temperature information.

Multiple temperature measurement points and their average

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `average` | `float` | — | L3879 |
| `css` | `float` | — | L3880 |
| `dss` | `float` | — | L3881 |
| `mss` | `float` | — | L3882 |
| `upa` | `float` | — | L3883 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L3884 | __init__(self: depthai.ChipTemperature) -> None |

<a id="class-chiptemperaturervc4"></a>
### class `ChipTemperatureRVC4`  — L3887

> Chip temperature information.

Multiple temperature measurement points and their average

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `average` | `float` | — | L3891 |
| `camera` | `float` | — | L3892 |
| `cpuss` | `float` | — | L3893 |
| `ddr` | `float` | — | L3894 |
| `gpuss` | `float` | — | L3895 |
| `mdmss` | `float` | — | L3896 |
| `video` | `float` | — | L3897 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L3898 | __init__(self: depthai.ChipTemperatureRVC4) -> None |

<a id="class-circleannotation"></a>
### class `CircleAnnotation`  — L3901

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `diameter` | `float` | — | L3902 |
| `fillColor` | `Color` | — | L3903 |
| `outlineColor` | `Color` | — | L3904 |
| `position` | `Point2f` | — | L3905 |
| `thickness` | `float` | — | L3906 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L3907 | __init__(self: depthai.CircleAnnotation) -> None |

<a id="class-clock"></a>
### class `Clock`  — L3910

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L3911 | Initialize self.  See help(type(self)) for accurate signature. |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def now(self) -> datetime.timedelta` | `(self)` | L3913 | now() -> datetime.timedelta |

<a id="class-color"></a>
### class `Color`  — L3916

> Color structure

r,g,b,a color values with values in range [0.0, 1.0]

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `a` | `float` | — | L3920 |
| `b` | `float` | — | L3921 |
| `g` | `float` | — | L3922 |
| `r` | `float` | — | L3923 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L3925 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, r: float, g: float, b: float, a: float = ...) -> None` | `(self, r: float, g: float, b: float, a: float = ...)` | L3934 | __init__(*args, **kwargs) |

<a id="class-colorcameraproperties"></a>
### class `ColorCameraProperties`  — L3943

> Specify properties for ColorCamera such as camera ID, ...

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `boardSocket` | `CameraBoardSocket` | — | L4104 |
| `calibAlpha` | `float` | — | L4105 |
| `eventFilter` | `list[FrameEvent]` | — | L4106 |
| `fps` | `float` | — | L4107 |
| `imageOrientation` | `CameraImageOrientation` | — | L4108 |
| `initialControl` | `CameraControl` | — | L4109 |
| `isp3aFps` | `int` | — | L4110 |
| `ispScale` | `Incomplete` | — | L4111 |
| `numFramesPoolIsp` | `int` | — | L4112 |
| `numFramesPoolPreview` | `int` | — | L4113 |
| `numFramesPoolRaw` | `int` | — | L4114 |
| `numFramesPoolStill` | `int` | — | L4115 |
| `numFramesPoolVideo` | `int` | — | L4116 |
| `previewHeight` | `int` | — | L4117 |
| `previewKeepAspectRatio` | `bool` | — | L4118 |
| `previewWidth` | `int` | — | L4119 |
| `resolution` | `ColorCameraProperties.SensorResolution` | — | L4120 |
| `sensorCropX` | `float` | — | L4121 |
| `sensorCropY` | `float` | — | L4122 |
| `stillHeight` | `int` | — | L4123 |
| `stillWidth` | `int` | — | L4124 |
| `videoHeight` | `int` | — | L4125 |
| `videoWidth` | `int` | — | L4126 |
| `warpMeshHeight` | `int` | — | L4127 |
| `warpMeshSource` | `ColorCameraProperties.WarpMeshSource` | — | L4128 |
| `warpMeshStepHeight` | `int` | — | L4129 |
| `warpMeshStepWidth` | `int` | — | L4130 |
| `warpMeshUri` | `str` | — | L4131 |
| `warpMeshWidth` | `int` | — | L4132 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L4133 | Initialize self.  See help(type(self)) for accurate signature. |

**Nested Class:**

<a id="class-colororder"></a>
#### class `ColorOrder`  — L3946

> For 24 bit color these can be either RGB or BGR

Members:

  BGR

  RGB

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L3954 |
| `BGR` | `ClassVar[ColorCameraProperties.ColorOrder]` | `...` | L3955 |
| `RGB` | `ClassVar[ColorCameraProperties.ColorOrder]` | `...` | L3956 |
| `__entries` | `ClassVar[dict]` | `...` | L3957 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L3958 | __init__(self: depthai.ColorCameraProperties.ColorOrder, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L3960 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L3962 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L3964 | __index__(self: depthai.ColorCameraProperties.ColorOrder) -> int |
| `def __int__(self) -> int` | `(self)` | L3966 | __int__(self: depthai.ColorCameraProperties.ColorOrder) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L3968 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L3971 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L3977 | (arg0: depthai.ColorCameraProperties.ColorOrder) -> int |

**Nested Class:**

<a id="class-sensorresolution"></a>
#### class `SensorResolution`  — L3980

> Select the camera sensor resolution

Members:

  THE_1080_P

  THE_1200_P

  THE_4_K

  THE_5_MP

  THE_12_MP

  THE_4000X3000

  THE_13_MP

  THE_5312X6000

  THE_48_MP

  THE_720_P

  THE_800_P

  THE_240X180

  THE_1280X962

  THE_2000X1500

  THE_2028X1520

  THE_2104X1560

  THE_1440X1080

  THE_1352X1012

  THE_2024X1520

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L4022 |
| `THE_1080_P` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4023 |
| `THE_1200_P` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4024 |
| `THE_1280X962` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4025 |
| `THE_12_MP` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4026 |
| `THE_1352X1012` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4027 |
| `THE_13_MP` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4028 |
| `THE_1440X1080` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4029 |
| `THE_2000X1500` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4030 |
| `THE_2024X1520` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4031 |
| `THE_2028X1520` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4032 |
| `THE_2104X1560` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4033 |
| `THE_240X180` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4034 |
| `THE_4000X3000` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4035 |
| `THE_48_MP` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4036 |
| `THE_4_K` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4037 |
| `THE_5312X6000` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4038 |
| `THE_5_MP` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4039 |
| `THE_720_P` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4040 |
| `THE_800_P` | `ClassVar[ColorCameraProperties.SensorResolution]` | `...` | L4041 |
| `__entries` | `ClassVar[dict]` | `...` | L4042 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L4043 | __init__(self: depthai.ColorCameraProperties.SensorResolution, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L4045 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L4047 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L4049 | __index__(self: depthai.ColorCameraProperties.SensorResolution) -> int |
| `def __int__(self) -> int` | `(self)` | L4051 | __int__(self: depthai.ColorCameraProperties.SensorResolution) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L4053 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L4056 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L4062 | (arg0: depthai.ColorCameraProperties.SensorResolution) -> int |

**Nested Class:**

<a id="class-warpmeshsource"></a>
#### class `WarpMeshSource`  — L4065

> Warp mesh source

Members:

  AUTO

  NONE

  CALIBRATION

  URI

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L4077 |
| `AUTO` | `ClassVar[ColorCameraProperties.WarpMeshSource]` | `...` | L4078 |
| `CALIBRATION` | `ClassVar[ColorCameraProperties.WarpMeshSource]` | `...` | L4079 |
| `NONE` | `ClassVar[ColorCameraProperties.WarpMeshSource]` | `...` | L4080 |
| `URI` | `ClassVar[ColorCameraProperties.WarpMeshSource]` | `...` | L4081 |
| `__entries` | `ClassVar[dict]` | `...` | L4082 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L4083 | __init__(self: depthai.ColorCameraProperties.WarpMeshSource, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L4085 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L4087 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L4089 | __index__(self: depthai.ColorCameraProperties.WarpMeshSource) -> int |
| `def __int__(self) -> int` | `(self)` | L4091 | __int__(self: depthai.ColorCameraProperties.WarpMeshSource) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L4093 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L4096 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L4102 | (arg0: depthai.ColorCameraProperties.WarpMeshSource) -> int |

<a id="class-colormap"></a>
### class `Colormap`  — L4136

> Camera sensor type

Members:

  NONE

  JET

  TURBO

  STEREO_JET

  STEREO_TURBO

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L4150 |
| `JET` | `ClassVar[Colormap]` | `...` | L4151 |
| `NONE` | `ClassVar[Colormap]` | `...` | L4152 |
| `STEREO_JET` | `ClassVar[Colormap]` | `...` | L4153 |
| `STEREO_TURBO` | `ClassVar[Colormap]` | `...` | L4154 |
| `TURBO` | `ClassVar[Colormap]` | `...` | L4155 |
| `__entries` | `ClassVar[dict]` | `...` | L4156 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L4157 | __init__(self: depthai.Colormap, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L4159 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L4161 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L4163 | __index__(self: depthai.Colormap) -> int |
| `def __int__(self) -> int` | `(self)` | L4165 | __int__(self: depthai.Colormap) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L4167 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L4170 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L4176 | (arg0: depthai.Colormap) -> int |

<a id="class-coveragedata"></a>
### class `CoverageData(Buffer)`  — L4179

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `coverageAcquired` | `float` | — | L4180 |
| `coveragePerCellA` | `list[list[float]]` | — | L4181 |
| `coveragePerCellB` | `list[list[float]]` | — | L4182 |
| `dataAcquired` | `float` | — | L4183 |
| `meanCoverage` | `float` | — | L4184 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L4185 | __init__(self: depthai.CoverageData) -> None |

<a id="class-cpuusage"></a>
### class `CpuUsage`  — L4188

> CpuUsage structure

Average usage in percent and time span of the average (since last query)

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `average` | `float` | — | L4192 |
| `msTime` | `int` | — | L4193 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L4194 | __init__(self: depthai.CpuUsage) -> None |

<a id="class-crashdump"></a>
### class `CrashDump`  — L4197

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `crashReports` | `list[CrashDump.CrashReport]` | — | L4243 |
| `depthaiCommitHash` | `str` | — | L4244 |
| `deviceId` | `str` | — | L4245 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L4246 | __init__(self: depthai.CrashDump) -> None |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def serializeToJson(self) -> json` | `(self)` | L4248 | serializeToJson(self: depthai.CrashDump) -> json |

**Nested Class:**

<a id="class-crashreport"></a>
#### class `CrashReport`  — L4198

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `crashedThreadId` | `int` | — | L4237 |
| `errorSource` | `str` | — | L4238 |
| `processor` | `ProcessorType` | — | L4239 |
| `threadCallstack` | `list[CrashDump.CrashReport.ThreadCallstack]` | — | L4240 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L4241 | __init__(self: depthai.CrashDump.CrashReport) -> None |

**Nested Class:**

<a id="class-errorsourceinfo"></a>
##### class `ErrorSourceInfo`  — L4199

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `assertContext` | `CrashDump.CrashReport.ErrorSourceInfo.AssertContext` | — | L4213 |
| `errorId` | `int` | — | L4214 |
| `trapContext` | `CrashDump.CrashReport.ErrorSourceInfo.TrapContext` | — | L4215 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L4216 | __init__(self: depthai.CrashDump.CrashReport.ErrorSourceInfo) -> None |

**Nested Class:**

<a id="class-assertcontext"></a>
###### class `AssertContext`  — L4200

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `fileName` | `str` | — | L4201 |
| `functionName` | `str` | — | L4202 |
| `line` | `int` | — | L4203 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L4204 | __init__(self: depthai.CrashDump.CrashReport.ErrorSourceInfo.AssertContext) -> None |

**Nested Class:**

<a id="class-trapcontext"></a>
###### class `TrapContext`  — L4207

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `trapAddress` | `int` | — | L4208 |
| `trapName` | `str` | — | L4209 |
| `trapNumber` | `int` | — | L4210 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L4211 | __init__(self: depthai.CrashDump.CrashReport.ErrorSourceInfo.TrapContext) -> None |

**Nested Class:**

<a id="class-threadcallstack"></a>
##### class `ThreadCallstack`  — L4219

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `callStack` | `list[CrashDump.CrashReport.ThreadCallstack.CallstackContext]` | — | L4227 |
| `instructionPointer` | `int` | — | L4228 |
| `stackBottom` | `int` | — | L4229 |
| `stackPointer` | `int` | — | L4230 |
| `stackTop` | `int` | — | L4231 |
| `threadId` | `int` | — | L4232 |
| `threadName` | `str` | — | L4233 |
| `threadStatus` | `str` | — | L4234 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L4235 | __init__(self: depthai.CrashDump.CrashReport.ThreadCallstack) -> None |

**Nested Class:**

<a id="class-callstackcontext"></a>
###### class `CallstackContext`  — L4220

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `callSite` | `int` | — | L4221 |
| `calledTarget` | `int` | — | L4222 |
| `context` | `str` | — | L4223 |
| `framePointer` | `int` | — | L4224 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L4225 | __init__(self: depthai.CrashDump.CrashReport.ThreadCallstack.CallstackContext) -> None |

<a id="class-datatypeenum"></a>
### class `DatatypeEnum`  — L4251

> Members:

  ADatatype

  Buffer

  ImgFrame

  EncodedFrame

  NNData

  ImageManipConfig

  CameraControl

  ImgDetections

  SpatialImgDetections

  SystemInformation

  SystemInformationRVC4

  SpatialLocationCalculatorConfig

  SpatialLocationCalculatorData

  EdgeDetectorConfig

  AprilTagConfig

  AprilTags

  Tracklets

  IMUData

  StereoDepthConfig

  FeatureTrackerConfig

  ThermalConfig

  ToFConfig

  VppConfig

  TrackedFeatures

  BenchmarkReport

  MessageGroup

  TransformData

  PointCloudConfig

  PointCloudData

  ImageAlignConfig

  ImgAnnotations

  RGBDData

  PipelineEvent

  PipelineState

  ImageFiltersConfig

  ToFDepthConfidenceFilterConfig

  DynamicCalibrationControl

  DynamicCalibrationResult

  CalibrationQuality

  CoverageData

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L4335 |
| `ADatatype` | `ClassVar[DatatypeEnum]` | `...` | L4336 |
| `AprilTagConfig` | `ClassVar[DatatypeEnum]` | `...` | L4337 |
| `AprilTags` | `ClassVar[DatatypeEnum]` | `...` | L4338 |
| `BenchmarkReport` | `ClassVar[DatatypeEnum]` | `...` | L4339 |
| `Buffer` | `ClassVar[DatatypeEnum]` | `...` | L4340 |
| `CalibrationQuality` | `ClassVar[DatatypeEnum]` | `...` | L4341 |
| `CameraControl` | `ClassVar[DatatypeEnum]` | `...` | L4342 |
| `CoverageData` | `ClassVar[DatatypeEnum]` | `...` | L4343 |
| `DynamicCalibrationControl` | `ClassVar[DatatypeEnum]` | `...` | L4344 |
| `DynamicCalibrationResult` | `ClassVar[DatatypeEnum]` | `...` | L4345 |
| `EdgeDetectorConfig` | `ClassVar[DatatypeEnum]` | `...` | L4346 |
| `EncodedFrame` | `ClassVar[DatatypeEnum]` | `...` | L4347 |
| `FeatureTrackerConfig` | `ClassVar[DatatypeEnum]` | `...` | L4348 |
| `IMUData` | `ClassVar[DatatypeEnum]` | `...` | L4349 |
| `ImageAlignConfig` | `ClassVar[DatatypeEnum]` | `...` | L4350 |
| `ImageFiltersConfig` | `ClassVar[DatatypeEnum]` | `...` | L4351 |
| `ImageManipConfig` | `ClassVar[DatatypeEnum]` | `...` | L4352 |
| `ImgAnnotations` | `ClassVar[DatatypeEnum]` | `...` | L4353 |
| `ImgDetections` | `ClassVar[DatatypeEnum]` | `...` | L4354 |
| `ImgFrame` | `ClassVar[DatatypeEnum]` | `...` | L4355 |
| `MessageGroup` | `ClassVar[DatatypeEnum]` | `...` | L4356 |
| `NNData` | `ClassVar[DatatypeEnum]` | `...` | L4357 |
| `PipelineEvent` | `ClassVar[DatatypeEnum]` | `...` | L4358 |
| `PipelineState` | `ClassVar[DatatypeEnum]` | `...` | L4359 |
| `PointCloudConfig` | `ClassVar[DatatypeEnum]` | `...` | L4360 |
| `PointCloudData` | `ClassVar[DatatypeEnum]` | `...` | L4361 |
| `RGBDData` | `ClassVar[DatatypeEnum]` | `...` | L4362 |
| `SpatialImgDetections` | `ClassVar[DatatypeEnum]` | `...` | L4363 |
| `SpatialLocationCalculatorConfig` | `ClassVar[DatatypeEnum]` | `...` | L4364 |
| `SpatialLocationCalculatorData` | `ClassVar[DatatypeEnum]` | `...` | L4365 |
| `StereoDepthConfig` | `ClassVar[DatatypeEnum]` | `...` | L4366 |
| `SystemInformation` | `ClassVar[DatatypeEnum]` | `...` | L4367 |
| `SystemInformationRVC4` | `ClassVar[DatatypeEnum]` | `...` | L4368 |
| `ThermalConfig` | `ClassVar[DatatypeEnum]` | `...` | L4369 |
| `ToFConfig` | `ClassVar[DatatypeEnum]` | `...` | L4370 |
| `ToFDepthConfidenceFilterConfig` | `ClassVar[DatatypeEnum]` | `...` | L4371 |
| `TrackedFeatures` | `ClassVar[DatatypeEnum]` | `...` | L4372 |
| `Tracklets` | `ClassVar[DatatypeEnum]` | `...` | L4373 |
| `TransformData` | `ClassVar[DatatypeEnum]` | `...` | L4374 |
| `VppConfig` | `ClassVar[DatatypeEnum]` | `...` | L4375 |
| `__entries` | `ClassVar[dict]` | `...` | L4376 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L4377 | __init__(self: depthai.DatatypeEnum, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L4379 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L4381 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L4383 | __index__(self: depthai.DatatypeEnum) -> int |
| `def __int__(self) -> int` | `(self)` | L4385 | __int__(self: depthai.DatatypeEnum) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L4387 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L4390 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L4396 | (arg0: depthai.DatatypeEnum) -> int |

<a id="class-depthunit"></a>
### class `DepthUnit`  — L4399

> Measurement unit for depth data

Members:

  METER

  CENTIMETER

  MILLIMETER

  INCH

  FOOT

  CUSTOM

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L4415 |
| `CENTIMETER` | `ClassVar[DepthUnit]` | `...` | L4416 |
| `CUSTOM` | `ClassVar[DepthUnit]` | `...` | L4417 |
| `FOOT` | `ClassVar[DepthUnit]` | `...` | L4418 |
| `INCH` | `ClassVar[DepthUnit]` | `...` | L4419 |
| `METER` | `ClassVar[DepthUnit]` | `...` | L4420 |
| `MILLIMETER` | `ClassVar[DepthUnit]` | `...` | L4421 |
| `__entries` | `ClassVar[dict]` | `...` | L4422 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L4423 | __init__(self: depthai.DepthUnit, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L4425 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L4427 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L4429 | __index__(self: depthai.DepthUnit) -> int |
| `def __int__(self) -> int` | `(self)` | L4431 | __int__(self: depthai.DepthUnit) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L4433 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L4436 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L4442 | (arg0: depthai.DepthUnit) -> int |

<a id="class-detectionnetworktype"></a>
### class `DetectionNetworkType`  — L4445

> Members:

YOLO

MOBILENET

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L4451 |
| `MOBILENET` | `ClassVar[DetectionNetworkType]` | `...` | L4452 |
| `YOLO` | `ClassVar[DetectionNetworkType]` | `...` | L4453 |
| `__entries` | `ClassVar[dict]` | `...` | L4454 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L4455 | __init__(self: depthai.DetectionNetworkType, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L4457 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L4459 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L4461 | __index__(self: depthai.DetectionNetworkType) -> int |
| `def __int__(self) -> int` | `(self)` | L4463 | __int__(self: depthai.DetectionNetworkType) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L4465 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L4468 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L4474 | (arg0: depthai.DetectionNetworkType) -> int |

<a id="class-detectionparseroptions"></a>
### class `DetectionParserOptions`  — L4477

> DetectionParserOptions

Specifies how to parse output of detection networks

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `anchorMasks` | `dict[str, list[int]]` | — | L4481 |
| `anchors` | `list[float]` | — | L4482 |
| `anchorsV2` | `list[list[list[float]]]` | — | L4483 |
| `classes` | `int` | — | L4484 |
| `confidenceThreshold` | `float` | — | L4485 |
| `coordinates` | `int` | — | L4486 |
| `decodeKeypoints` | `bool` | — | L4487 |
| `decodingFamily` | `YoloDecodingFamily` | — | L4488 |
| `iouThreshold` | `float` | — | L4489 |
| `keypointEdges` | `Incomplete` | — | L4490 |
| `nnFamily` | `DetectionNetworkType` | — | L4491 |
| `numKeypoints` | `int | None` | — | L4492 |
| `outputNames` | `list[str]` | — | L4493 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L4494 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-detectionparserproperties"></a>
### class `DetectionParserProperties`  — L4497

> Specify properties for DetectionParser

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `parser` | `DetectionParserOptions` | — | L4499 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L4500 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-device"></a>
### class `Device(DeviceBase)`  — L4503

> Represents the DepthAI device with the methods to interact with it. Implements
the host-side queues to connect with XLinkIn and XLinkOut nodes

**🔧 Dunder Methods (10):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L4554 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, maxUsbSpeed: UsbSpeed) -> None` | `(self, maxUsbSpeed: UsbSpeed)` | L4645 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, deviceInfo: DeviceInfo, maxUsbSpeed: UsbSpeed) -> None` | `(self, deviceInfo: DeviceInfo, maxUsbSpeed: UsbSpeed)` | L4736 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, deviceDesc: DeviceInfo, pathToCmd: os.PathLike) -> None` | `(self, deviceDesc: DeviceInfo, pathToCmd: os.PathLike)` | L4827 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, config: Device.Config) -> None` | `(self, config: Device.Config)` | L4918 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, config: Device.Config, deviceInfo: DeviceInfo) -> None` | `(self, config: Device.Config, deviceInfo: DeviceInfo)` | L5009 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, deviceInfo: DeviceInfo) -> None` | `(self, deviceInfo: DeviceInfo)` | L5100 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, deviceInfo: DeviceInfo, maxUsbSpeed: UsbSpeed) -> None` | `(self, deviceInfo: DeviceInfo, maxUsbSpeed: UsbSpeed)` | L5191 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, nameOrDeviceId: str) -> None` | `(self, nameOrDeviceId: str)` | L5282 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, nameOrDeviceId: str, maxUsbSpeed: UsbSpeed) -> None` | `(self, nameOrDeviceId: str, maxUsbSpeed: UsbSpeed)` | L5373 | __init__(*args, **kwargs) |

**🔹 Public Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getPlatform(self) -> Platform` | `(self)` | L5463 | getPlatform(self: depthai.Device) -> depthai.Platform |
| `def getPlatformAsString(self) -> str` | `(self)` | L5471 | getPlatformAsString(self: depthai.Device) -> str |

**Nested Class:**

<a id="class-config"></a>
#### class `Config`  — L4507

> Device specific configuration

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `board` | `BoardConfig` | — | L4509 |
| `logLevel` | `LogLevel | None` | — | L4510 |
| `nonExclusiveMode` | `bool` | — | L4511 |
| `outputLogLevel` | `LogLevel | None` | — | L4512 |
| `version` | `OpenVINO.Version` | — | L4513 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L4514 | __init__(self: depthai.Device.Config) -> None |

**Nested Class:**

<a id="class-reconnectionstatus"></a>
#### class `ReconnectionStatus`  — L4517

> Members:

  RECONNECT_FAILED

  RECONNECTED

  RECONNECTING

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L4527 |
| `RECONNECTED` | `ClassVar[Device.ReconnectionStatus]` | `...` | L4528 |
| `RECONNECTING` | `ClassVar[Device.ReconnectionStatus]` | `...` | L4529 |
| `RECONNECT_FAILED` | `ClassVar[Device.ReconnectionStatus]` | `...` | L4530 |
| `__entries` | `ClassVar[dict]` | `...` | L4531 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L4532 | __init__(self: depthai.Device.ReconnectionStatus, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L4534 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L4536 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L4538 | __index__(self: depthai.Device.ReconnectionStatus) -> int |
| `def __int__(self) -> int` | `(self)` | L4540 | __int__(self: depthai.Device.ReconnectionStatus) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L4542 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L4545 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L4551 | (arg0: depthai.Device.ReconnectionStatus) -> int |

<a id="class-devicebase"></a>
### class `DeviceBase`  — L5480

> The core of depthai device for RAII, connects to device and maintains watchdog,
timesync, ...

**🔧 Dunder Methods (12):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L5484 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, maxUsbSpeed: UsbSpeed) -> None` | `(self, maxUsbSpeed: UsbSpeed)` | L5575 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, deviceInfo: DeviceInfo, maxUsbSpeed: UsbSpeed) -> None` | `(self, deviceInfo: DeviceInfo, maxUsbSpeed: UsbSpeed)` | L5666 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, deviceDesc: DeviceInfo, pathToCmd: os.PathLike) -> None` | `(self, deviceDesc: DeviceInfo, pathToCmd: os.PathLike)` | L5757 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, config: Device.Config) -> None` | `(self, config: Device.Config)` | L5848 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, config: Device.Config, deviceInfo: DeviceInfo) -> None` | `(self, config: Device.Config, deviceInfo: DeviceInfo)` | L5939 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, deviceInfo: DeviceInfo) -> None` | `(self, deviceInfo: DeviceInfo)` | L6030 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, deviceInfo: DeviceInfo, maxUsbSpeed: UsbSpeed) -> None` | `(self, deviceInfo: DeviceInfo, maxUsbSpeed: UsbSpeed)` | L6121 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, nameOrDeviceId: str) -> None` | `(self, nameOrDeviceId: str)` | L6212 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, nameOrDeviceId: str, maxUsbSpeed: UsbSpeed) -> None` | `(self, nameOrDeviceId: str, maxUsbSpeed: UsbSpeed)` | L6303 | __init__(*args, **kwargs) |
| `def __enter__(self) -> DeviceBase` | `(self)` | L7191 | __enter__(self: depthai.DeviceBase) -> depthai.DeviceBase |
| `def __exit__(self, arg0: object, arg1: object, arg2: object) -> None` | `(self, arg0: object, arg1: object, arg2: object)` | L7193 | __exit__(self: depthai.DeviceBase, arg0: object, arg1: object, arg2: object) -> None |

**⚡ Static Methods (8):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@staticmethod` `def getAllAvailableDevices() -> list[DeviceInfo]` | `()` | L6473 | getAllAvailableDevices() -> list[depthai.DeviceInfo] |
| `@staticmethod` `def getAllConnectedDevices() -> list[DeviceInfo]` | `()` | L6482 | getAllConnectedDevices() -> list[depthai.DeviceInfo] |
| `@overload` `@staticmethod` `def getAnyAvailableDevice(timeout: datetime.timedelta) -> tuple[bool, DeviceInfo]` | `(timeout: datetime.timedelta)` | L6493 | getAnyAvailableDevice(*args, **kwargs) |
| `@overload` `@staticmethod` `def getAnyAvailableDevice() -> tuple[bool, DeviceInfo]` | `()` | L6518 | getAnyAvailableDevice(*args, **kwargs) |
| `@staticmethod` `def getDeviceById(deviceId: str) -> tuple[bool, DeviceInfo]` | `(deviceId: str)` | L6641 | getDeviceById(deviceId: str) -> tuple[bool, depthai.DeviceInfo] |
| `@staticmethod` `def getEmbeddedDeviceBinary(*args, **kwargs)` | `(*args, **kwargs)` | L6678 | getEmbeddedDeviceBinary(*args, **kwargs) |
| `@staticmethod` `def getFirstAvailableDevice(skipInvalidDevices: bool = ...) -> tuple[bool, DeviceInfo]` | `(skipInvalidDevices: bool = ...)` | L6714 | getFirstAvailableDevice(skipInvalidDevices: bool = True) -> tuple[bool, depthai.DeviceInfo] |
| `@staticmethod` `def getGlobalProfilingData() -> ProfilingData` | `()` | L6725 | getGlobalProfilingData() -> depthai.ProfilingData |

**🔹 Public Methods (66):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def addLogCallback(self, callback: Callable[[LogMessage], None]) -> int` | `(self, callback: Callable[[LogMessage], None])` | L6393 | addLogCallback(self: depthai.DeviceBase, callback: Callable[[depthai.LogMessage], None]) -> int |
| `def close(self) -> None` | `(self)` | L6405 | close(self: depthai.DeviceBase) -> None |
| `def crashDevice(self) -> None` | `(self)` | L6410 | crashDevice(self: depthai.DeviceBase) -> None |
| `def factoryResetCalibration(self) -> None` | `(self)` | L6417 | factoryResetCalibration(self: depthai.DeviceBase) -> None |
| `def flashCalibration(self, arg0: CalibrationHandler) -> None` | `(self, arg0: CalibrationHandler)` | L6425 | flashCalibration(self: depthai.DeviceBase, arg0: depthai.CalibrationHandler) -> None |
| `def flashEepromClear(self) -> None` | `(self)` | L6436 | flashEepromClear(self: depthai.DeviceBase) -> None |
| `def flashFactoryCalibration(self, arg0: CalibrationHandler) -> None` | `(self, arg0: CalibrationHandler)` | L6448 | flashFactoryCalibration(self: depthai.DeviceBase, arg0: depthai.CalibrationHandler) -> None |
| `def flashFactoryEepromClear(self) -> None` | `(self)` | L6460 | flashFactoryEepromClear(self: depthai.DeviceBase) -> None |
| `def getAvailableStereoPairs(self) -> list[StereoPair]` | `(self)` | L6541 | getAvailableStereoPairs(self: depthai.DeviceBase) -> list[depthai.StereoPair] |
| `def getBootloaderVersion(self) -> Version | None` | `(self)` | L6551 | getBootloaderVersion(self: depthai.DeviceBase) -> Optional[depthai.Version] |
| `def getCalibration(self) -> CalibrationHandler` | `(self)` | L6559 | getCalibration(self: depthai.DeviceBase) -> depthai.CalibrationHandler |
| `def getCameraSensorNames(self) -> dict[CameraBoardSocket, str]` | `(self)` | L6571 | getCameraSensorNames(self: depthai.DeviceBase) -> dict[depthai.CameraBoardSocket, str] |
| `def getChipTemperature(self) -> ChipTemperature` | `(self)` | L6579 | getChipTemperature(self: depthai.DeviceBase) -> depthai.ChipTemperature |
| `def getCmxMemoryUsage(self) -> MemoryInfo` | `(self)` | L6587 | getCmxMemoryUsage(self: depthai.DeviceBase) -> depthai.MemoryInfo |
| `def getConnectedCameraFeatures(self) -> list[CameraFeatures]` | `(self)` | L6595 | getConnectedCameraFeatures(self: depthai.DeviceBase) -> list[depthai.CameraFeatures] |
| `def getConnectedCameras(self) -> list[CameraBoardSocket]` | `(self)` | L6603 | getConnectedCameras(self: depthai.DeviceBase) -> list[depthai.CameraBoardSocket] |
| `def getConnectedIMU(self) -> str` | `(self)` | L6611 | getConnectedIMU(self: depthai.DeviceBase) -> str |
| `def getConnectionInterfaces(self) -> list[connectionInterface]` | `(self)` | L6619 | getConnectionInterfaces(self: depthai.DeviceBase) -> list[depthai.connectionInterface] |
| `def getCrashDump(self, clearCrashDump: bool = ...) -> CrashDump` | `(self, clearCrashDump: bool = ...)` | L6627 | getCrashDump(self: depthai.DeviceBase, clearCrashDump: bool = True) -> depthai.CrashDump |
| `def getDdrMemoryUsage(self) -> MemoryInfo` | `(self)` | L6632 | getDdrMemoryUsage(self: depthai.DeviceBase) -> depthai.MemoryInfo |
| `def getDeviceId(self) -> str` | `(self)` | L6653 | getDeviceId(self: depthai.DeviceBase) -> str |
| `def getDeviceInfo(self) -> DeviceInfo` | `(self)` | L6661 | getDeviceInfo(self: depthai.DeviceBase) -> depthai.DeviceInfo |
| `def getDeviceName(self) -> object` | `(self)` | L6669 | getDeviceName(self: depthai.DeviceBase) -> object |
| `def getEmbeddedIMUFirmwareVersion(self) -> Version` | `(self)` | L6705 | getEmbeddedIMUFirmwareVersion(self: depthai.DeviceBase) -> depthai.Version |
| `def getIMUFirmwareUpdateStatus(self) -> tuple[bool, float]` | `(self)` | L6733 | getIMUFirmwareUpdateStatus(self: depthai.DeviceBase) -> tuple[bool, float] |
| `def getIMUFirmwareVersion(self) -> Version` | `(self)` | L6743 | getIMUFirmwareVersion(self: depthai.DeviceBase) -> depthai.Version |
| `def getIrDrivers(self) -> list[tuple[str, int, int]]` | `(self)` | L6751 | getIrDrivers(self: depthai.DeviceBase) -> list[tuple[str, int, int]] |
| `def getLeonCssCpuUsage(self) -> CpuUsage` | `(self)` | L6760 | getLeonCssCpuUsage(self: depthai.DeviceBase) -> depthai.CpuUsage |
| `def getLeonCssHeapUsage(self) -> MemoryInfo` | `(self)` | L6768 | getLeonCssHeapUsage(self: depthai.DeviceBase) -> depthai.MemoryInfo |
| `def getLeonMssCpuUsage(self) -> CpuUsage` | `(self)` | L6776 | getLeonMssCpuUsage(self: depthai.DeviceBase) -> depthai.CpuUsage |
| `def getLeonMssHeapUsage(self) -> MemoryInfo` | `(self)` | L6784 | getLeonMssHeapUsage(self: depthai.DeviceBase) -> depthai.MemoryInfo |
| `def getLogLevel(self) -> LogLevel` | `(self)` | L6792 | getLogLevel(self: depthai.DeviceBase) -> depthai.LogLevel |
| `def getLogOutputLevel(self) -> LogLevel` | `(self)` | L6800 | getLogOutputLevel(self: depthai.DeviceBase) -> depthai.LogLevel |
| `def getMxId(self) -> str` | `(self)` | L6808 | getMxId(self: depthai.DeviceBase) -> str |
| `def getProcessMemoryUsage(self) -> int` | `(self)` | L6816 | getProcessMemoryUsage(self: depthai.DeviceBase) -> int |
| `def getProductName(self) -> object` | `(self)` | L6824 | getProductName(self: depthai.DeviceBase) -> object |
| `def getProfilingData(self) -> ProfilingData` | `(self)` | L6832 | getProfilingData(self: depthai.DeviceBase) -> depthai.ProfilingData |
| `def getStereoPairs(self) -> list[StereoPair]` | `(self)` | L6840 | getStereoPairs(self: depthai.DeviceBase) -> list[depthai.StereoPair] |
| `def getSystemInformationLoggingRate(self) -> float` | `(self)` | L6848 | getSystemInformationLoggingRate(self: depthai.DeviceBase) -> float |
| `def getUsbSpeed(self) -> UsbSpeed` | `(self)` | L6856 | getUsbSpeed(self: depthai.DeviceBase) -> depthai.UsbSpeed |
| `def getXLinkChunkSize(self) -> int` | `(self)` | L6864 | getXLinkChunkSize(self: depthai.DeviceBase) -> int |
| `def hasCrashDump(self) -> bool` | `(self)` | L6872 | hasCrashDump(self: depthai.DeviceBase) -> bool |
| `def isClosed(self) -> bool` | `(self)` | L6877 | isClosed(self: depthai.DeviceBase) -> bool |
| `def isEepromAvailable(self) -> bool` | `(self)` | L6888 | isEepromAvailable(self: depthai.DeviceBase) -> bool |
| `def isNeuralDepthSupported(self) -> bool` | `(self)` | L6896 | isNeuralDepthSupported(self: depthai.DeviceBase) -> bool |
| `def isPipelineRunning(self) -> bool` | `(self)` | L6904 | isPipelineRunning(self: depthai.DeviceBase) -> bool |
| `def readCalibration(self) -> CalibrationHandler` | `(self)` | L6912 | readCalibration(self: depthai.DeviceBase) -> depthai.CalibrationHandler |
| `def readCalibration2(self) -> CalibrationHandler` | `(self)` | L6922 | readCalibration2(self: depthai.DeviceBase) -> depthai.CalibrationHandler |
| `def readCalibrationOrDefault(self) -> CalibrationHandler` | `(self)` | L6935 | readCalibrationOrDefault(self: depthai.DeviceBase) -> depthai.CalibrationHandler |
| `def readCalibrationRaw(self) -> bytes` | `(self)` | L6945 | readCalibrationRaw(self: depthai.DeviceBase) -> bytes |
| `def readFactoryCalibration(self) -> CalibrationHandler` | `(self)` | L6956 | readFactoryCalibration(self: depthai.DeviceBase) -> depthai.CalibrationHandler |
| `def readFactoryCalibrationOrDefault(self) -> CalibrationHandler` | `(self)` | L6969 | readFactoryCalibrationOrDefault(self: depthai.DeviceBase) -> depthai.CalibrationHandler |
| `def readFactoryCalibrationRaw(self) -> bytes` | `(self)` | L6979 | readFactoryCalibrationRaw(self: depthai.DeviceBase) -> bytes |
| `def removeLogCallback(self, callbackId: int) -> bool` | `(self, callbackId: int)` | L6990 | removeLogCallback(self: depthai.DeviceBase, callbackId: int) -> bool |
| `def setCalibration(self, arg0: CalibrationHandler) -> None` | `(self, arg0: CalibrationHandler)` | L7001 | setCalibration(self: depthai.DeviceBase, arg0: depthai.CalibrationHandler) -> None |
| `def setIrFloodLightIntensity(self, intensity: float, mask: int = ...) -> bool` | `(self, intensity: float, mask: int = ...)` | L7013 | setIrFloodLightIntensity(self: depthai.DeviceBase, intensity: float, mask: int = -1) -> bool |
| `def setIrLaserDotProjectorIntensity(self, intensity: float, mask: int = ...) -> bool` | `(self, intensity: float, mask: int = ...)` | L7033 | setIrLaserDotProjectorIntensity(self: depthai.DeviceBase, intensity: float, mask: int = -1) -> bool |
| `def setLogLevel(self, level: LogLevel) -> None` | `(self, level: LogLevel)` | L7054 | setLogLevel(self: depthai.DeviceBase, level: depthai.LogLevel) -> None |
| `def setLogOutputLevel(self, level: LogLevel) -> None` | `(self, level: LogLevel)` | L7063 | setLogOutputLevel(self: depthai.DeviceBase, level: depthai.LogLevel) -> None |
| `def setMaxReconnectionAttempts(self, maxAttempts: int, callback: Callable[[Device.ReconnectionStatus], None] = ...) -> None` | `(self, maxAttempts: int, callback: Callable[[Device.ReconnectionStatus], None] = ...)` | L7072 | setMaxReconnectionAttempts(self: depthai.DeviceBase, maxAttempts: int, callback: Callable[[depthai.Device.ReconnectionStatus], None] = None) -> None |
| `def setSystemInformationLoggingRate(self, rateHz: float) -> None` | `(self, rateHz: float)` | L7083 | setSystemInformationLoggingRate(self: depthai.DeviceBase, rateHz: float) -> None |
| `@overload` `def setTimesync(self, arg0: datetime.timedelta, arg1: int, arg2: bool) -> None` | `(self, arg0: datetime.timedelta, arg1: int, arg2: bool)` | L7094 | setTimesync(*args, **kwargs) |
| `@overload` `def setTimesync(self, enable: bool) -> None` | `(self, enable: bool)` | L7124 | setTimesync(*args, **kwargs) |
| `def setXLinkChunkSize(self, sizeBytes: int) -> None` | `(self, sizeBytes: int)` | L7153 | setXLinkChunkSize(self: depthai.DeviceBase, sizeBytes: int) -> None |
| `def startIMUFirmwareUpdate(self, forceUpdate: bool = ...) -> bool` | `(self, forceUpdate: bool = ...)` | L7164 | startIMUFirmwareUpdate(self: depthai.DeviceBase, forceUpdate: bool = False) -> bool |
| `def tryFlashCalibration(self, calibrationDataHandler: CalibrationHandler) -> bool` | `(self, calibrationDataHandler: CalibrationHandler)` | L7180 | tryFlashCalibration(self: depthai.DeviceBase, calibrationDataHandler: depthai.CalibrationHandler) -> bool |

<a id="class-devicebootloader"></a>
### class `DeviceBootloader`  — L7196

> Represents the DepthAI bootloader with the methods to interact with it.

**🔧 Dunder Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, devInfo: DeviceInfo, allowFlashingBootloader: bool = ...) -> None` | `(self, devInfo: DeviceInfo, allowFlashingBootloader: bool = ...)` | L7394 | __init__(*args, **kwargs) |
| `def __enter__(self) -> DeviceBootloader` | `(self)` | L8144 | __enter__(self: depthai.DeviceBootloader) -> depthai.DeviceBootloader |
| `def __exit__(self, arg0: object, arg1: object, arg2: object) -> None` | `(self, arg0: object, arg1: object, arg2: object)` | L8146 | __exit__(self: depthai.DeviceBootloader, arg0: object, arg1: object, arg2: object) -> None |

**⚡ Static Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@staticmethod` `def createDepthaiApplicationPackage(*args, **kwargs)` | `(*args, **kwargs)` | L7461 | createDepthaiApplicationPackage(*args, **kwargs) |
| `@staticmethod` `def getAllAvailableDevices() -> list[DeviceInfo]` | `()` | L7901 | getAllAvailableDevices() -> list[depthai.DeviceInfo] |
| `@staticmethod` `def getEmbeddedBootloaderBinary(*args, **kwargs)` | `(*args, **kwargs)` | L7910 | getEmbeddedBootloaderBinary(arg0: depthai.DeviceBootloader.Type) -> std::vector<unsigned char,std::allocator<unsigned char> > |
| `@staticmethod` `def getEmbeddedBootloaderVersion() -> Version` | `()` | L7917 | getEmbeddedBootloaderVersion() -> depthai.Version |
| `@staticmethod` `def getFirstAvailableDevice() -> tuple[bool, DeviceInfo]` | `()` | L7924 | getFirstAvailableDevice() -> tuple[bool, depthai.DeviceInfo] |
| `@overload` `@staticmethod` `def saveDepthaiApplicationPackage(path: os.PathLike, pipeline: Pipeline, pathToCmd: os.PathLike = ..., compress: bool = ..., applicationName: str = ..., checkChecksum: bool = ...) -> None` | `(path: os.PathLike, pipeline: Pipeline, pathToCmd: os.PathLike = ..., compress: bool = ..., applicationName: str = ..., checkChecksum: bool = ...)` | L8064 | saveDepthaiApplicationPackage(*args, **kwargs) |
| `@overload` `@staticmethod` `def saveDepthaiApplicationPackage(path: os.PathLike, pipeline: Pipeline, compress: bool, applicationName: str = ..., checkChecksum: bool = ...) -> None` | `(path: os.PathLike, pipeline: Pipeline, compress: bool, applicationName: str = ..., checkChecksum: bool = ...)` | L8105 | saveDepthaiApplicationPackage(*args, **kwargs) |

**🔹 Public Methods (32):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def bootMemory(self, fw, std) -> None` | `(self, fw, std)` | L7437 | bootMemory(self: depthai.DeviceBootloader, fw: std::vector<unsigned char,std::allocator<unsigned char> >) -> None |
| `def bootUsbRomBootloader(self) -> None` | `(self)` | L7447 | bootUsbRomBootloader(self: depthai.DeviceBootloader) -> None |
| `def close(self) -> None` | `(self)` | L7455 | close(self: depthai.DeviceBootloader) -> None |
| `@overload` `def flash(self, progressCallback: Callable[[float], None], pipeline: Pipeline, compress: bool = ..., applicationName: str = ..., memory: DeviceBootloader.Memory = ..., checkChecksum: bool = ...) -> tuple[bool, str]` | `(self, progressCallback: Callable[[float], None], pipeline: Pipeline, compress: bool = ..., applicationName: str = ..., memory: DeviceBootloader.Memory = ..., checkChecksum: bool = ...)` | L7501 | flash(*args, **kwargs) |
| `@overload` `def flash(self, pipeline: Pipeline, compress: bool = ..., applicationName: str = ..., memory: DeviceBootloader.Memory = ..., checkChecksum: bool = ...) -> tuple[bool, str]` | `(self, pipeline: Pipeline, compress: bool = ..., applicationName: str = ..., memory: DeviceBootloader.Memory = ..., checkChecksum: bool = ...)` | L7536 | flash(*args, **kwargs) |
| `def flashBootHeader(self, memory: DeviceBootloader.Memory, frequency: int = ..., location: int = ..., dummyCycles: int = ..., offset: int = ...) -> tuple[bool, str]` | `(self, memory: DeviceBootloader.Memory, frequency: int = ..., location: int = ..., dummyCycles: int = ..., offset: int = ...)` | L7570 | flashBootHeader(self: depthai.DeviceBootloader, memory: depthai.DeviceBootloader.Memory, frequency: int = -1, location: int = -1, dummyCycles: int = -1, offset: int = -1) -> tuple[bool, str] |
| `@overload` `def flashBootloader(self, progressCallback: Callable[[float], None], path: os.PathLike = ...) -> tuple[bool, str]` | `(self, progressCallback: Callable[[float], None], path: os.PathLike = ...)` | L7594 | flashBootloader(*args, **kwargs) |
| `@overload` `def flashBootloader(self, memory: DeviceBootloader.Memory, type: DeviceBootloader.Type, progressCallback: Callable[[float], None], path: os.PathLike = ...) -> tuple[bool, str]` | `(self, memory: DeviceBootloader.Memory, type: DeviceBootloader.Type, progressCallback: Callable[[float], None], path: os.PathLike = ...)` | L7627 | flashBootloader(*args, **kwargs) |
| `def flashClear(self, memory: DeviceBootloader.Memory = ...) -> tuple[bool, str]` | `(self, memory: DeviceBootloader.Memory = ...)` | L7659 | flashClear(self: depthai.DeviceBootloader, memory: depthai.DeviceBootloader.Memory = <Memory.AUTO: -1>) -> tuple[bool, str] |
| `def flashConfig(self, config: DeviceBootloader.Config, memory: DeviceBootloader.Memory = ..., type: DeviceBootloader.Type = ...) -> tuple[bool, str]` | `(self, config: DeviceBootloader.Config, memory: DeviceBootloader.Memory = ..., type: DeviceBootloader.Type = ...)` | L7665 | flashConfig(self: depthai.DeviceBootloader, config: depthai.DeviceBootloader.Config, memory: depthai.DeviceBootloader.Memory = <Memory.AUTO: -1>, type: depthai.DeviceBootloader.Type = <Type.AUTO: -1>) -> tuple[bool, str] |
| `def flashConfigClear(self, memory: DeviceBootloader.Memory = ..., type: DeviceBootloader.Type = ...) -> tuple[bool, str]` | `(self, memory: DeviceBootloader.Memory = ..., type: DeviceBootloader.Type = ...)` | L7679 | flashConfigClear(self: depthai.DeviceBootloader, memory: depthai.DeviceBootloader.Memory = <Memory.AUTO: -1>, type: depthai.DeviceBootloader.Type = <Type.AUTO: -1>) -> tuple[bool, str] |
| `def flashConfigData(self, configData: json, memory: DeviceBootloader.Memory = ..., type: DeviceBootloader.Type = ...) -> tuple[bool, str]` | `(self, configData: json, memory: DeviceBootloader.Memory = ..., type: DeviceBootloader.Type = ...)` | L7690 | flashConfigData(self: depthai.DeviceBootloader, configData: json, memory: depthai.DeviceBootloader.Memory = <Memory.AUTO: -1>, type: depthai.DeviceBootloader.Type = <Type.AUTO: -1>) -> tuple[bool, str] |
| `def flashConfigFile(self, configData: os.PathLike, memory: DeviceBootloader.Memory = ..., type: DeviceBootloader.Type = ...) -> tuple[bool, str]` | `(self, configData: os.PathLike, memory: DeviceBootloader.Memory = ..., type: DeviceBootloader.Type = ...)` | L7704 | flashConfigFile(self: depthai.DeviceBootloader, configData: os.PathLike, memory: depthai.DeviceBootloader.Memory = <Memory.AUTO: -1>, type: depthai.DeviceBootloader.Type = <Type.AUTO: -1>) -> tuple[bool, str] |
| `@overload` `def flashCustom(self, memory: DeviceBootloader.Memory, offset: int, data, std, progressCallback: Callable[[float], None] = ...) -> tuple[bool, str]` | `(self, memory: DeviceBootloader.Memory, offset: int, data, std, progressCallback: Callable[[float], None] = ...)` | L7719 | flashCustom(*args, **kwargs) |
| `@overload` `def flashCustom(self, memory: DeviceBootloader.Memory, offset: int, filename: str, progressCallback: Callable[[float], None] = ...) -> tuple[bool, str]` | `(self, memory: DeviceBootloader.Memory, offset: int, filename: str, progressCallback: Callable[[float], None] = ...)` | L7758 | flashCustom(*args, **kwargs) |
| `@overload` `def flashDepthaiApplicationPackage(self, progressCallback: Callable[[float], None], package, std, memory: DeviceBootloader.Memory = ...) -> tuple[bool, str]` | `(self, progressCallback: Callable[[float], None], package, std, memory: DeviceBootloader.Memory = ...)` | L7797 | flashDepthaiApplicationPackage(*args, **kwargs) |
| `@overload` `def flashDepthaiApplicationPackage(self, package, std, memory: DeviceBootloader.Memory = ...) -> tuple[bool, str]` | `(self, package, std, memory: DeviceBootloader.Memory = ...)` | L7822 | flashDepthaiApplicationPackage(*args, **kwargs) |
| `def flashFastBootHeader(self, memory: DeviceBootloader.Memory, frequency: int = ..., location: int = ..., dummyCycles: int = ..., offset: int = ...) -> tuple[bool, str]` | `(self, memory: DeviceBootloader.Memory, frequency: int = ..., location: int = ..., dummyCycles: int = ..., offset: int = ...)` | L7846 | flashFastBootHeader(self: depthai.DeviceBootloader, memory: depthai.DeviceBootloader.Memory, frequency: int = -1, location: int = -1, dummyCycles: int = -1, offset: int = -1) -> tuple[bool, str] |
| `def flashGpioModeBootHeader(self, memory: DeviceBootloader.Memory, mode: int) -> tuple[bool, str]` | `(self, memory: DeviceBootloader.Memory, mode: int)` | L7871 | flashGpioModeBootHeader(self: depthai.DeviceBootloader, memory: depthai.DeviceBootloader.Memory, mode: int) -> tuple[bool, str] |
| `def flashUsbRecoveryBootHeader(self, memory: DeviceBootloader.Memory) -> tuple[bool, str]` | `(self, memory: DeviceBootloader.Memory)` | L7879 | flashUsbRecoveryBootHeader(self: depthai.DeviceBootloader, memory: depthai.DeviceBootloader.Memory) -> tuple[bool, str] |
| `def flashUserBootloader(self, progressCallback: Callable[[float], None], path: os.PathLike = ...) -> tuple[bool, str]` | `(self, progressCallback: Callable[[float], None], path: os.PathLike = ...)` | L7887 | flashUserBootloader(self: depthai.DeviceBootloader, progressCallback: Callable[[float], None], path: os.PathLike = '') -> tuple[bool, str] |
| `def getMemoryInfo(self, arg0: DeviceBootloader.Memory) -> DeviceBootloader.MemoryInfo` | `(self, arg0: DeviceBootloader.Memory)` | L7934 | getMemoryInfo(self: depthai.DeviceBootloader, arg0: depthai.DeviceBootloader.Memory) -> depthai.DeviceBootloader.MemoryInfo |
| `def getType(self) -> DeviceBootloader.Type` | `(self)` | L7942 | getType(self: depthai.DeviceBootloader) -> depthai.DeviceBootloader.Type |
| `def getVersion(self) -> Version` | `(self)` | L7948 | getVersion(self: depthai.DeviceBootloader) -> depthai.Version |
| `def isAllowedFlashingBootloader(self) -> bool` | `(self)` | L7954 | isAllowedFlashingBootloader(self: depthai.DeviceBootloader) -> bool |
| `def isEmbeddedVersion(self) -> bool` | `(self)` | L7960 | isEmbeddedVersion(self: depthai.DeviceBootloader) -> bool |
| `def isUserBootloader(self) -> bool` | `(self)` | L7968 | isUserBootloader(self: depthai.DeviceBootloader) -> bool |
| `def isUserBootloaderSupported(self) -> bool` | `(self)` | L7974 | isUserBootloaderSupported(self: depthai.DeviceBootloader) -> bool |
| `def readApplicationInfo(self, memory: DeviceBootloader.Memory) -> DeviceBootloader.ApplicationInfo` | `(self, memory: DeviceBootloader.Memory)` | L7982 | readApplicationInfo(self: depthai.DeviceBootloader, memory: depthai.DeviceBootloader.Memory) -> depthai.DeviceBootloader.ApplicationInfo |
| `def readConfig(self, memory: DeviceBootloader.Memory = ..., type: DeviceBootloader.Type = ...) -> DeviceBootloader.Config` | `(self, memory: DeviceBootloader.Memory = ..., type: DeviceBootloader.Type = ...)` | L7990 | readConfig(self: depthai.DeviceBootloader, memory: depthai.DeviceBootloader.Memory = <Memory.AUTO: -1>, type: depthai.DeviceBootloader.Type = <Type.AUTO: -1>) -> depthai.DeviceBootloader.Config |
| `def readConfigData(self, memory: DeviceBootloader.Memory = ..., type: DeviceBootloader.Type = ...) -> json` | `(self, memory: DeviceBootloader.Memory = ..., type: DeviceBootloader.Type = ...)` | L8004 | readConfigData(self: depthai.DeviceBootloader, memory: depthai.DeviceBootloader.Memory = <Memory.AUTO: -1>, type: depthai.DeviceBootloader.Type = <Type.AUTO: -1>) -> json |
| `def readCustom(self, memory: DeviceBootloader.Memory, offset: int, size: int, filename: str, progressCallback: Callable[[float], None] = ...) -> tuple[bool, str]` | `(self, memory: DeviceBootloader.Memory, offset: int, size: int, filename: str, progressCallback: Callable[[float], None] = ...)` | L8018 | readCustom(*args, **kwargs) |

**Nested Class:**

<a id="class-applicationinfo"></a>
#### class `ApplicationInfo`  — L7199

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `applicationName` | `str` | — | L7200 |
| `firmwareVersion` | `str` | — | L7201 |
| `hasApplication` | `bool` | — | L7202 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L7203 | __init__(self: depthai.DeviceBootloader.ApplicationInfo) -> None |

**Nested Class:**

<a id="class-config"></a>
#### class `Config`  — L7206

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `appMem` | `DeviceBootloader.Memory` | — | L7207 |
| `network` | `DeviceBootloader.NetworkConfig` | — | L7208 |
| `usb` | `DeviceBootloader.UsbConfig` | — | L7209 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L7210 | __init__(self: depthai.DeviceBootloader.Config) -> None |

**🔹 Public Methods (19):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def fromJson(self) -> DeviceBootloader.Config` | `(self)` | L7212 | fromJson(self: json) -> depthai.DeviceBootloader.Config |
| `def getDnsAltIPv4(self) -> str` | `(self)` | L7214 | getDnsAltIPv4(self: depthai.DeviceBootloader.Config) -> str |
| `def getDnsIPv4(self) -> str` | `(self)` | L7216 | getDnsIPv4(self: depthai.DeviceBootloader.Config) -> str |
| `def getIPv4(self) -> str` | `(self)` | L7218 | getIPv4(self: depthai.DeviceBootloader.Config) -> str |
| `def getIPv4Gateway(self) -> str` | `(self)` | L7220 | getIPv4Gateway(self: depthai.DeviceBootloader.Config) -> str |
| `def getIPv4Mask(self) -> str` | `(self)` | L7222 | getIPv4Mask(self: depthai.DeviceBootloader.Config) -> str |
| `def getMacAddress(self) -> str` | `(self)` | L7224 | getMacAddress(self: depthai.DeviceBootloader.Config) -> str |
| `def getNetworkTimeout(self) -> datetime.timedelta` | `(self)` | L7226 | getNetworkTimeout(self: depthai.DeviceBootloader.Config) -> datetime.timedelta |
| `def getUsbMaxSpeed(self) -> UsbSpeed` | `(self)` | L7228 | getUsbMaxSpeed(self: depthai.DeviceBootloader.Config) -> depthai.UsbSpeed |
| `def getUsbTimeout(self) -> datetime.timedelta` | `(self)` | L7230 | getUsbTimeout(self: depthai.DeviceBootloader.Config) -> datetime.timedelta |
| `def isStaticIPV4(self) -> bool` | `(self)` | L7232 | isStaticIPV4(self: depthai.DeviceBootloader.Config) -> bool |
| `def setDnsIPv4(self, arg0: str, arg1: str) -> None` | `(self, arg0: str, arg1: str)` | L7234 | setDnsIPv4(self: depthai.DeviceBootloader.Config, arg0: str, arg1: str) -> None |
| `def setDynamicIPv4(self, arg0: str, arg1: str, arg2: str) -> None` | `(self, arg0: str, arg1: str, arg2: str)` | L7236 | setDynamicIPv4(self: depthai.DeviceBootloader.Config, arg0: str, arg1: str, arg2: str) -> None |
| `def setMacAddress(self, arg0: str) -> None` | `(self, arg0: str)` | L7238 | setMacAddress(self: depthai.DeviceBootloader.Config, arg0: str) -> None |
| `def setNetworkTimeout(self, arg0: datetime.timedelta) -> None` | `(self, arg0: datetime.timedelta)` | L7240 | setNetworkTimeout(self: depthai.DeviceBootloader.Config, arg0: datetime.timedelta) -> None |
| `def setStaticIPv4(self, arg0: str, arg1: str, arg2: str) -> None` | `(self, arg0: str, arg1: str, arg2: str)` | L7242 | setStaticIPv4(self: depthai.DeviceBootloader.Config, arg0: str, arg1: str, arg2: str) -> None |
| `def setUsbMaxSpeed(self, arg0: UsbSpeed) -> None` | `(self, arg0: UsbSpeed)` | L7244 | setUsbMaxSpeed(self: depthai.DeviceBootloader.Config, arg0: depthai.UsbSpeed) -> None |
| `def setUsbTimeout(self, arg0: datetime.timedelta) -> None` | `(self, arg0: datetime.timedelta)` | L7246 | setUsbTimeout(self: depthai.DeviceBootloader.Config, arg0: datetime.timedelta) -> None |
| `def toJson(self) -> json` | `(self)` | L7248 | toJson(self: depthai.DeviceBootloader.Config) -> json |

**Nested Class:**

<a id="class-memory"></a>
#### class `Memory`  — L7251

> Members:

AUTO

FLASH

EMMC

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L7259 |
| `AUTO` | `ClassVar[DeviceBootloader.Memory]` | `...` | L7260 |
| `EMMC` | `ClassVar[DeviceBootloader.Memory]` | `...` | L7261 |
| `FLASH` | `ClassVar[DeviceBootloader.Memory]` | `...` | L7262 |
| `__entries` | `ClassVar[dict]` | `...` | L7263 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L7264 | __init__(self: depthai.DeviceBootloader.Memory, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L7266 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L7268 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L7270 | __index__(self: depthai.DeviceBootloader.Memory) -> int |
| `def __int__(self) -> int` | `(self)` | L7272 | __int__(self: depthai.DeviceBootloader.Memory) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L7274 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L7277 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L7283 | (arg0: depthai.DeviceBootloader.Memory) -> int |

**Nested Class:**

<a id="class-memoryinfo"></a>
#### class `MemoryInfo`  — L7286

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `available` | `bool` | — | L7287 |
| `info` | `str` | — | L7288 |
| `size` | `int` | — | L7289 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L7290 | __init__(self: depthai.DeviceBootloader.MemoryInfo) -> None |

**Nested Class:**

<a id="class-networkconfig"></a>
#### class `NetworkConfig`  — L7293

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `ipv4` | `int` | — | L7294 |
| `ipv4Dns` | `int` | — | L7295 |
| `ipv4DnsAlt` | `int` | — | L7296 |
| `ipv4Gateway` | `int` | — | L7297 |
| `ipv4Mask` | `int` | — | L7298 |
| `ipv6` | `Incomplete` | — | L7299 |
| `ipv6Dns` | `Incomplete` | — | L7300 |
| `ipv6DnsAlt` | `Incomplete` | — | L7301 |
| `ipv6Gateway` | `Incomplete` | — | L7302 |
| `ipv6Prefix` | `int` | — | L7303 |
| `mac` | `Incomplete` | — | L7304 |
| `staticIpv4` | `bool` | — | L7305 |
| `staticIpv6` | `bool` | — | L7306 |
| `timeoutMs` | `int` | — | L7307 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L7308 | __init__(self: depthai.DeviceBootloader.NetworkConfig) -> None |

**Nested Class:**

<a id="class-section"></a>
#### class `Section`  — L7311

> Members:

AUTO

HEADER

BOOTLOADER

BOOTLOADER_CONFIG

APPLICATION

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L7323 |
| `APPLICATION` | `ClassVar[DeviceBootloader.Section]` | `...` | L7324 |
| `AUTO` | `ClassVar[DeviceBootloader.Section]` | `...` | L7325 |
| `BOOTLOADER` | `ClassVar[DeviceBootloader.Section]` | `...` | L7326 |
| `BOOTLOADER_CONFIG` | `ClassVar[DeviceBootloader.Section]` | `...` | L7327 |
| `HEADER` | `ClassVar[DeviceBootloader.Section]` | `...` | L7328 |
| `__entries` | `ClassVar[dict]` | `...` | L7329 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L7330 | __init__(self: depthai.DeviceBootloader.Section, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L7332 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L7334 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L7336 | __index__(self: depthai.DeviceBootloader.Section) -> int |
| `def __int__(self) -> int` | `(self)` | L7338 | __int__(self: depthai.DeviceBootloader.Section) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L7340 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L7343 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L7349 | (arg0: depthai.DeviceBootloader.Section) -> int |

**Nested Class:**

<a id="class-type"></a>
#### class `Type`  — L7352

> Members:

AUTO

USB

NETWORK

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L7360 |
| `AUTO` | `ClassVar[DeviceBootloader.Type]` | `...` | L7361 |
| `NETWORK` | `ClassVar[DeviceBootloader.Type]` | `...` | L7362 |
| `USB` | `ClassVar[DeviceBootloader.Type]` | `...` | L7363 |
| `__entries` | `ClassVar[dict]` | `...` | L7364 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L7365 | __init__(self: depthai.DeviceBootloader.Type, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L7367 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L7369 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L7371 | __index__(self: depthai.DeviceBootloader.Type) -> int |
| `def __int__(self) -> int` | `(self)` | L7373 | __int__(self: depthai.DeviceBootloader.Type) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L7375 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L7378 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L7384 | (arg0: depthai.DeviceBootloader.Type) -> int |

**Nested Class:**

<a id="class-usbconfig"></a>
#### class `UsbConfig`  — L7387

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `maxUsbSpeed` | `int` | — | L7388 |
| `pid` | `int` | — | L7389 |
| `timeoutMs` | `int` | — | L7390 |
| `vid` | `int` | — | L7391 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L7392 | __init__(self: depthai.DeviceBootloader.UsbConfig) -> None |

<a id="class-devicedesc"></a>
### class `DeviceDesc`  — L8149

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `mxid` | `str` | — | L8150 |
| `name` | `str` | — | L8151 |
| `platform` | `XLinkPlatform` | — | L8152 |
| `protocol` | `XLinkProtocol` | — | L8153 |
| `state` | `XLinkDeviceState` | — | L8154 |
| `status` | `XLinkError_t` | — | L8155 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L8156 | __init__(self: depthai.DeviceDesc) -> None |

<a id="class-deviceinfo"></a>
### class `DeviceInfo`  — L8159

> Describes a connected device

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `deviceId` | `str` | — | L8161 |
| `name` | `str` | — | L8162 |
| `platform` | `XLinkPlatform` | — | L8163 |
| `protocol` | `XLinkProtocol` | — | L8164 |
| `state` | `XLinkDeviceState` | — | L8165 |
| `status` | `XLinkError_t` | — | L8166 |

**🔧 Dunder Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L8168 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, name: str, deviceId: str, state: XLinkDeviceState, protocol: XLinkProtocol, platform: XLinkPlatform, status: XLinkError_t) -> None` | `(self, name: str, deviceId: str, state: XLinkDeviceState, protocol: XLinkProtocol, platform: XLinkPlatform, status: XLinkError_t)` | L8187 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, deviceIdOrName: str) -> None` | `(self, deviceIdOrName: str)` | L8206 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: DeviceDesc) -> None` | `(self, arg0: DeviceDesc)` | L8225 | __init__(*args, **kwargs) |

**🔹 Public Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getDeviceId(self) -> str` | `(self)` | L8243 | getDeviceId(self: depthai.DeviceInfo) -> str |
| `def getXLinkDeviceDesc(self) -> DeviceDesc` | `(self)` | L8245 | getXLinkDeviceDesc(self: depthai.DeviceInfo) -> depthai.DeviceDesc |

<a id="class-devicemodelzoo"></a>
### class `DeviceModelZoo`  — L8248

> On device models, relevant for RVC4 platform

Members:

  NEURAL_DEPTH_LARGE

  NEURAL_DEPTH_MEDIUM

  NEURAL_DEPTH_SMALL

  NEURAL_DEPTH_NANO

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L8260 |
| `NEURAL_DEPTH_LARGE` | `ClassVar[DeviceModelZoo]` | `...` | L8261 |
| `NEURAL_DEPTH_MEDIUM` | `ClassVar[DeviceModelZoo]` | `...` | L8262 |
| `NEURAL_DEPTH_NANO` | `ClassVar[DeviceModelZoo]` | `...` | L8263 |
| `NEURAL_DEPTH_SMALL` | `ClassVar[DeviceModelZoo]` | `...` | L8264 |
| `__entries` | `ClassVar[dict]` | `...` | L8265 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L8266 | __init__(self: depthai.DeviceModelZoo, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L8268 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L8270 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L8272 | __index__(self: depthai.DeviceModelZoo) -> int |
| `def __int__(self) -> int` | `(self)` | L8274 | __int__(self: depthai.DeviceModelZoo) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L8276 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L8279 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L8285 | (arg0: depthai.DeviceModelZoo) -> int |

<a id="class-devicenode"></a>
### class `DeviceNode(ThreadedNode)`  — L8288

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L8289 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-devicenodegroup"></a>
### class `DeviceNodeGroup(DeviceNode)`  — L8292

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L8293 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-dynamiccalibrationcontrol"></a>
### class `DynamicCalibrationControl(Buffer)`  — L8296

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `DEFAULT` | `ClassVar[DynamicCalibrationControl.PerformanceMode]` | `...` | L8394 |
| `OPTIMIZE_PERFORMANCE` | `ClassVar[DynamicCalibrationControl.PerformanceMode]` | `...` | L8395 |
| `OPTIMIZE_SPEED` | `ClassVar[DynamicCalibrationControl.PerformanceMode]` | `...` | L8396 |
| `SKIP_CHECKS` | `ClassVar[DynamicCalibrationControl.PerformanceMode]` | `...` | L8397 |
| `STATIC_SCENERY` | `ClassVar[DynamicCalibrationControl.PerformanceMode]` | `...` | L8398 |

**🔧 Dunder Methods (9):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L8400 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: DynamicCalibrationControl.Commands.Calibrate) -> None` | `(self, arg0: DynamicCalibrationControl.Commands.Calibrate)` | L8423 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: DynamicCalibrationControl.Commands.CalibrationQuality) -> None` | `(self, arg0: DynamicCalibrationControl.Commands.CalibrationQuality)` | L8446 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: DynamicCalibrationControl.Commands.StartCalibration) -> None` | `(self, arg0: DynamicCalibrationControl.Commands.StartCalibration)` | L8469 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: DynamicCalibrationControl.Commands.StopCalibration) -> None` | `(self, arg0: DynamicCalibrationControl.Commands.StopCalibration)` | L8492 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: DynamicCalibrationControl.Commands.LoadImage) -> None` | `(self, arg0: DynamicCalibrationControl.Commands.LoadImage)` | L8515 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: DynamicCalibrationControl.Commands.ApplyCalibration) -> None` | `(self, arg0: DynamicCalibrationControl.Commands.ApplyCalibration)` | L8538 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: DynamicCalibrationControl.Commands.ResetData) -> None` | `(self, arg0: DynamicCalibrationControl.Commands.ResetData)` | L8561 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: DynamicCalibrationControl.Commands.SetPerformanceMode) -> None` | `(self, arg0: DynamicCalibrationControl.Commands.SetPerformanceMode)` | L8584 | __init__(*args, **kwargs) |

**⚡ Static Methods (8):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@staticmethod` `def applyCalibration(calibration) -> DynamicCalibrationControl` | `(calibration)` | L8607 | applyCalibration(calibration: dai::CalibrationHandler) -> depthai.DynamicCalibrationControl |
| `@staticmethod` `def calibrate(force: bool = ...) -> DynamicCalibrationControl` | `(force: bool = ...)` | L8613 | calibrate(force: bool = False) -> depthai.DynamicCalibrationControl |
| `@staticmethod` `def calibrationQuality(force: bool = ...) -> DynamicCalibrationControl` | `(force: bool = ...)` | L8619 | calibrationQuality(force: bool = False) -> depthai.DynamicCalibrationControl |
| `@staticmethod` `def loadImage() -> DynamicCalibrationControl` | `()` | L8625 | loadImage() -> depthai.DynamicCalibrationControl |
| `@staticmethod` `def resetData() -> DynamicCalibrationControl` | `()` | L8631 | resetData() -> depthai.DynamicCalibrationControl |
| `@staticmethod` `def setPerformanceMode(mode: DynamicCalibrationControl.PerformanceMode = ...) -> DynamicCalibrationControl` | `(mode: DynamicCalibrationControl.PerformanceMode = ...)` | L8637 | setPerformanceMode(mode: depthai.DynamicCalibrationControl.PerformanceMode = <PerformanceMode.DEFAULT: 0>) -> depthai.DynamicCalibrationControl |
| `@staticmethod` `def startCalibration(loadImagePeriod: float = ..., calibrationPeriod: float = ...) -> DynamicCalibrationControl` | `(loadImagePeriod: float = ..., calibrationPeriod: float = ...)` | L8643 | startCalibration(loadImagePeriod: float = 0.5, calibrationPeriod: float = 5.0) -> depthai.DynamicCalibrationControl |
| `@staticmethod` `def stopCalibration() -> DynamicCalibrationControl` | `()` | L8649 | stopCalibration() -> depthai.DynamicCalibrationControl |

**Nested Class:**

<a id="class-commands"></a>
#### class `Commands`  — L8297

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L8351 | Initialize self.  See help(type(self)) for accurate signature. |

**Nested Class:**

<a id="class-applycalibration"></a>
##### class `ApplyCalibration`  — L8298

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `calibration` | `Incomplete` | — | L8299 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L8301 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, calibration) -> None` | `(self, calibration)` | L8310 | __init__(*args, **kwargs) |

**Nested Class:**

<a id="class-calibrate"></a>
##### class `Calibrate`  — L8319

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `force` | `bool` | — | L8320 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, force: bool = ...) -> None` | `(self, force: bool = ...)` | L8321 | __init__(self: depthai.DynamicCalibrationControl.Commands.Calibrate, force: bool = False) -> None |

**Nested Class:**

<a id="class-calibrationquality"></a>
##### class `CalibrationQuality`  — L8324

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `force` | `bool` | — | L8325 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, force: bool = ...) -> None` | `(self, force: bool = ...)` | L8326 | __init__(self: depthai.DynamicCalibrationControl.Commands.CalibrationQuality, force: bool = False) -> None |

**Nested Class:**

<a id="class-loadimage"></a>
##### class `LoadImage`  — L8329

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L8330 | __init__(self: depthai.DynamicCalibrationControl.Commands.LoadImage) -> None |

**Nested Class:**

<a id="class-resetdata"></a>
##### class `ResetData`  — L8333

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L8334 | __init__(self: depthai.DynamicCalibrationControl.Commands.ResetData) -> None |

**Nested Class:**

<a id="class-setperformancemode"></a>
##### class `SetPerformanceMode`  — L8337

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `performanceMode` | `DynamicCalibrationControl.PerformanceMode` | — | L8338 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, performanceMode: DynamicCalibrationControl.PerformanceMode) -> None` | `(self, performanceMode: DynamicCalibrationControl.PerformanceMode)` | L8339 | __init__(self: depthai.DynamicCalibrationControl.Commands.SetPerformanceMode, performanceMode: depthai.DynamicCalibrationControl.PerformanceMode) -> None |

**Nested Class:**

<a id="class-startcalibration"></a>
##### class `StartCalibration`  — L8342

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `calibrationPeriod` | `float` | — | L8343 |
| `loadImagePeriod` | `float` | — | L8344 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, loadImagePeriod: float = ..., calibrationPeriod: float = ...) -> None` | `(self, loadImagePeriod: float = ..., calibrationPeriod: float = ...)` | L8345 | __init__(self: depthai.DynamicCalibrationControl.Commands.StartCalibration, loadImagePeriod: float = 0.5, calibrationPeriod: float = 5.0) -> None |

**Nested Class:**

<a id="class-stopcalibration"></a>
##### class `StopCalibration`  — L8348

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L8349 | __init__(self: depthai.DynamicCalibrationControl.Commands.StopCalibration) -> None |

**Nested Class:**

<a id="class-performancemode"></a>
#### class `PerformanceMode`  — L8354

> Members:

DEFAULT

STATIC_SCENERY

OPTIMIZE_SPEED

OPTIMIZE_PERFORMANCE

SKIP_CHECKS

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L8366 |
| `DEFAULT` | `ClassVar[DynamicCalibrationControl.PerformanceMode]` | `...` | L8367 |
| `OPTIMIZE_PERFORMANCE` | `ClassVar[DynamicCalibrationControl.PerformanceMode]` | `...` | L8368 |
| `OPTIMIZE_SPEED` | `ClassVar[DynamicCalibrationControl.PerformanceMode]` | `...` | L8369 |
| `SKIP_CHECKS` | `ClassVar[DynamicCalibrationControl.PerformanceMode]` | `...` | L8370 |
| `STATIC_SCENERY` | `ClassVar[DynamicCalibrationControl.PerformanceMode]` | `...` | L8371 |
| `__entries` | `ClassVar[dict]` | `...` | L8372 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L8373 | __init__(self: depthai.DynamicCalibrationControl.PerformanceMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L8375 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L8377 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L8379 | __index__(self: depthai.DynamicCalibrationControl.PerformanceMode) -> int |
| `def __int__(self) -> int` | `(self)` | L8381 | __int__(self: depthai.DynamicCalibrationControl.PerformanceMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L8383 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L8386 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L8392 | (arg0: depthai.DynamicCalibrationControl.PerformanceMode) -> int |

<a id="class-dynamiccalibrationproperties"></a>
### class `DynamicCalibrationProperties`  — L8655

> Specify properties for Dynamic calibration.

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L8657 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-dynamiccalibrationresult"></a>
### class `DynamicCalibrationResult(Buffer)`  — L8660

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `calibrationData` | `DynamicCalibrationResultData | None` | — | L8661 |
| `info` | `str` | — | L8662 |

**🔧 Dunder Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L8664 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, data: DynamicCalibrationResultData, info: str) -> None` | `(self, data: DynamicCalibrationResultData, info: str)` | L8675 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, info: str) -> None` | `(self, info: str)` | L8686 | __init__(*args, **kwargs) |

<a id="class-dynamiccalibrationresultdata"></a>
### class `DynamicCalibrationResultData`  — L8697

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `calibrationDifference` | `CalibrationQualityData` | — | L8698 |
| `currentCalibration` | `Incomplete` | — | L8699 |
| `newCalibration` | `Incomplete` | — | L8700 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L8701 | __init__(self: depthai.DynamicCalibrationResultData) -> None |

<a id="class-edgedetectorconfig"></a>
### class `EdgeDetectorConfig(Buffer)`  — L8704

> EdgeDetectorConfig message. Carries sobel edge filter config.

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L8706 | __init__(self: depthai.EdgeDetectorConfig) -> None |

**🔹 Public Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getConfigData(self) -> EdgeDetectorConfigData` | `(self)` | L8708 | getConfigData(self: depthai.EdgeDetectorConfig) -> depthai.EdgeDetectorConfigData |
| `def setSobelFilterKernels(self, horizontalKernel: list[list[int]], verticalKernel: list[list[int]]) -> None` | `(self, horizontalKernel: list[list[int]], verticalKernel: list[list[int]])` | L8716 | setSobelFilterKernels(self: depthai.EdgeDetectorConfig, horizontalKernel: list[list[int]], verticalKernel: list[list[int]]) -> None |

<a id="class-edgedetectorconfigdata"></a>
### class `EdgeDetectorConfigData`  — L8728

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `sobelFilterHorizontalKernel` | `list[list[int]]` | — | L8729 |
| `sobelFilterVerticalKernel` | `list[list[int]]` | — | L8730 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L8731 | __init__(self: depthai.EdgeDetectorConfigData) -> None |

<a id="class-edgedetectorproperties"></a>
### class `EdgeDetectorProperties`  — L8734

> Specify properties for EdgeDetector

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `initialConfig` | `EdgeDetectorConfig` | — | L8736 |
| `numFramesPool` | `int` | — | L8737 |
| `outputFrameSize` | `int` | — | L8738 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L8739 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-eepromdata"></a>
### class `EepromData`  — L8742

> EepromData structure

Contains the Calibration and Board data stored on device

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `batchName` | `str` | — | L8746 |
| `batchTime` | `int` | — | L8747 |
| `boardConf` | `str` | — | L8748 |
| `boardCustom` | `str` | — | L8749 |
| `boardName` | `str` | — | L8750 |
| `boardOptions` | `int` | — | L8751 |
| `boardRev` | `str` | — | L8752 |
| `cameraData` | `dict[CameraBoardSocket, CameraInfo]` | — | L8753 |
| `deviceName` | `str` | — | L8754 |
| `hardwareConf` | `str` | — | L8755 |
| `housingExtrinsics` | `Extrinsics` | — | L8756 |
| `imuExtrinsics` | `Extrinsics` | — | L8757 |
| `miscellaneousData` | `Incomplete` | — | L8758 |
| `productName` | `str` | — | L8759 |
| `stereoEnableDistortionCorrection` | `bool` | — | L8760 |
| `stereoRectificationData` | `StereoRectification` | — | L8761 |
| `stereoUseSpecTranslation` | `bool` | — | L8762 |
| `version` | `int` | — | L8763 |
| `verticalCameraSocket` | `CameraBoardSocket` | — | L8764 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L8765 | __init__(self: depthai.EepromData) -> None |

<a id="class-eepromerror"></a>
### class `EepromError(RuntimeError)`  — L8768

<a id="class-encodedframe"></a>
### class `EncodedFrame(Buffer)`  — L8770

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L8845 | __init__(self: depthai.EncodedFrame) -> None |

**🔹 Public Methods (27):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getBitrate(self) -> int` | `(self)` | L8847 | getBitrate(self: depthai.EncodedFrame) -> int |
| `def getColorTemperature(self) -> int` | `(self)` | L8852 | getColorTemperature(self: depthai.EncodedFrame) -> int |
| `def getExposureTime(self) -> datetime.timedelta` | `(self)` | L8857 | getExposureTime(self: depthai.EncodedFrame) -> datetime.timedelta |
| `def getFrameType(self) -> EncodedFrame.FrameType` | `(self)` | L8862 | getFrameType(self: depthai.EncodedFrame) -> depthai.EncodedFrame.FrameType |
| `def getHeight(self) -> int` | `(self)` | L8867 | getHeight(self: depthai.EncodedFrame) -> int |
| `def getInstanceNum(self) -> int` | `(self)` | L8872 | getInstanceNum(self: depthai.EncodedFrame) -> int |
| `def getLensPosition(self) -> int` | `(self)` | L8877 | getLensPosition(self: depthai.EncodedFrame) -> int |
| `def getLensPositionRaw(self) -> float` | `(self)` | L8882 | getLensPositionRaw(self: depthai.EncodedFrame) -> float |
| `def getLossless(self) -> bool` | `(self)` | L8887 | getLossless(self: depthai.EncodedFrame) -> bool |
| `def getProfile(self) -> EncodedFrame.Profile` | `(self)` | L8892 | getProfile(self: depthai.EncodedFrame) -> depthai.EncodedFrame.Profile |
| `def getQuality(self) -> int` | `(self)` | L8897 | getQuality(self: depthai.EncodedFrame) -> int |
| `def getSensitivity(self) -> int` | `(self)` | L8902 | getSensitivity(self: depthai.EncodedFrame) -> int |
| `def getSequenceNum(self) -> int` | `(self)` | L8907 | getSequenceNum(self: depthai.EncodedFrame) -> int |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L8912 | getTimestamp(self: depthai.EncodedFrame) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L8917 | getTimestampDevice(self: depthai.EncodedFrame) -> datetime.timedelta |
| `def getTransformation(self) -> ImgTransformation` | `(self)` | L8923 | getTransformation(self: depthai.EncodedFrame) -> depthai.ImgTransformation |
| `def getWidth(self) -> int` | `(self)` | L8925 | getWidth(self: depthai.EncodedFrame) -> int |
| `def setBitrate(self, arg0: int) -> EncodedFrame` | `(self, arg0: int)` | L8930 | setBitrate(self: depthai.EncodedFrame, arg0: int) -> depthai.EncodedFrame |
| `def setFrameType(self, arg0: EncodedFrame.FrameType) -> EncodedFrame` | `(self, arg0: EncodedFrame.FrameType)` | L8935 | setFrameType(self: depthai.EncodedFrame, arg0: depthai.EncodedFrame.FrameType) -> depthai.EncodedFrame |
| `def setHeight(self, height: int) -> EncodedFrame` | `(self, height: int)` | L8940 | setHeight(self: depthai.EncodedFrame, height: int) -> depthai.EncodedFrame |
| `def setLossless(self, arg0: bool) -> EncodedFrame` | `(self, arg0: bool)` | L8948 | setLossless(self: depthai.EncodedFrame, arg0: bool) -> depthai.EncodedFrame |
| `def setProfile(self, arg0: EncodedFrame.Profile) -> EncodedFrame` | `(self, arg0: EncodedFrame.Profile)` | L8953 | setProfile(self: depthai.EncodedFrame, arg0: depthai.EncodedFrame.Profile) -> depthai.EncodedFrame |
| `def setQuality(self, arg0: int) -> EncodedFrame` | `(self, arg0: int)` | L8958 | setQuality(self: depthai.EncodedFrame, arg0: int) -> depthai.EncodedFrame |
| `@overload` `def setSize(self, width: int, height: int) -> EncodedFrame` | `(self, width: int, height: int)` | L8964 | setSize(*args, **kwargs) |
| `@overload` `def setSize(self, sizer: tuple[int, int]) -> EncodedFrame` | `(self, sizer: tuple[int, int])` | L8986 | setSize(*args, **kwargs) |
| `def setTransformation(self, arg0: ImgTransformation) -> None` | `(self, arg0: ImgTransformation)` | L9007 | setTransformation(self: depthai.EncodedFrame, arg0: depthai.ImgTransformation) -> None |
| `def setWidth(self, width: int) -> EncodedFrame` | `(self, width: int)` | L9009 | setWidth(self: depthai.EncodedFrame, width: int) -> depthai.EncodedFrame |

**Nested Class:**

<a id="class-frametype"></a>
#### class `FrameType`  — L8771

> Members:

  I

  P

  B

  Unknown

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L8783 |
| `B` | `ClassVar[EncodedFrame.FrameType]` | `...` | L8784 |
| `I` | `ClassVar[EncodedFrame.FrameType]` | `...` | L8785 |
| `P` | `ClassVar[EncodedFrame.FrameType]` | `...` | L8786 |
| `Unknown` | `ClassVar[EncodedFrame.FrameType]` | `...` | L8787 |
| `__entries` | `ClassVar[dict]` | `...` | L8788 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L8789 | __init__(self: depthai.EncodedFrame.FrameType, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L8791 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L8793 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L8795 | __index__(self: depthai.EncodedFrame.FrameType) -> int |
| `def __int__(self) -> int` | `(self)` | L8797 | __int__(self: depthai.EncodedFrame.FrameType) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L8799 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L8802 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L8808 | (arg0: depthai.EncodedFrame.FrameType) -> int |

**Nested Class:**

<a id="class-profile"></a>
#### class `Profile`  — L8811

> Members:

JPEG

AVC

HEVC

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L8819 |
| `AVC` | `ClassVar[EncodedFrame.Profile]` | `...` | L8820 |
| `HEVC` | `ClassVar[EncodedFrame.Profile]` | `...` | L8821 |
| `JPEG` | `ClassVar[EncodedFrame.Profile]` | `...` | L8822 |
| `__entries` | `ClassVar[dict]` | `...` | L8823 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L8824 | __init__(self: depthai.EncodedFrame.Profile, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L8826 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L8828 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L8830 | __index__(self: depthai.EncodedFrame.Profile) -> int |
| `def __int__(self) -> int` | `(self)` | L8832 | __int__(self: depthai.EncodedFrame.Profile) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L8834 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L8837 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L8843 | (arg0: depthai.EncodedFrame.Profile) -> int |

<a id="class-eventsmanager"></a>
### class `EventsManager`  — L9018

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L9020 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, uploadCachedOnStart: bool = ...) -> None` | `(self, uploadCachedOnStart: bool = ...)` | L9029 | __init__(*args, **kwargs) |

**🔹 Public Methods (8):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def sendEvent(self, name: str, tags: list[str] = ..., extras: dict[str, str] = ..., deviceSerialNo: str = ..., associateFiles: list[str] = ...) -> bool` | `(self, name: str, tags: list[str] = ..., extras: dict[str, str] = ..., deviceSerialNo: str = ..., associateFiles: list[str] = ...)` | L9037 | sendEvent(self: depthai.EventsManager, name: str, tags: list[str] = [], extras: dict[str, str] = {}, deviceSerialNo: str = '', associateFiles: list[str] = []) -> bool |
| `@overload` `def sendSnap(self, name: str, fileGroup: FileGroup = ..., tags: list[str] = ..., extras: dict[str, str] = ..., deviceSerialNo: str = ...) -> bool` | `(self, name: str, fileGroup: FileGroup = ..., tags: list[str] = ..., extras: dict[str, str] = ..., deviceSerialNo: str = ...)` | L9061 | sendSnap(*args, **kwargs) |
| `@overload` `def sendSnap(self, name: str, fileName: str | None, imgFrame: ImgFrame, imgDetections: ImgDetections | None, tags: list[str] = ..., extras: dict[str, str] = ..., deviceSerialNo: str = ...) -> bool` | `(self, name: str, fileName: str | None, imgFrame: ImgFrame, imgDetections: ImgDetections | None, tags: list[str] = ..., extras: dict[str, str] = ..., deviceSerialNo: str = ...)` | L9112 | sendSnap(*args, **kwargs) |
| `def setCacheDir(self, cacheDir: str) -> None` | `(self, cacheDir: str)` | L9162 | setCacheDir(self: depthai.EventsManager, cacheDir: str) -> None |
| `def setCacheIfCannotSend(self, cacheIfCannotUpload: bool) -> None` | `(self, cacheIfCannotUpload: bool)` | L9174 | setCacheIfCannotSend(self: depthai.EventsManager, cacheIfCannotUpload: bool) -> None |
| `def setLogResponse(self, logResponse: bool) -> None` | `(self, logResponse: bool)` | L9186 | setLogResponse(self: depthai.EventsManager, logResponse: bool) -> None |
| `def setToken(self, token: str) -> None` | `(self, token: str)` | L9198 | setToken(self: depthai.EventsManager, token: str) -> None |
| `def setVerifySsl(self, verifySsl: bool) -> None` | `(self, verifySsl: bool)` | L9210 | setVerifySsl(self: depthai.EventsManager, verifySsl: bool) -> None |

<a id="class-extrinsics"></a>
### class `Extrinsics`  — L9222

> Extrinsics structure

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `rotationMatrix` | `list[list[float]]` | — | L9224 |
| `specTranslation` | `Point3f` | — | L9225 |
| `toCameraSocket` | `CameraBoardSocket` | — | L9226 |
| `translation` | `Point3f` | — | L9227 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9228 | __init__(self: depthai.Extrinsics) -> None |

<a id="class-featuretrackerconfig"></a>
### class `FeatureTrackerConfig(Buffer)`  — L9231

> FeatureTrackerConfig message. Carries config for feature tracking algorithm

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9350 | __init__(self: depthai.FeatureTrackerConfig) -> None |

**🔹 Public Methods (10):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def setCornerDetector(self, cornerDetector: FeatureTrackerConfig.CornerDetector.Type) -> FeatureTrackerConfig` | `(self, cornerDetector: FeatureTrackerConfig.CornerDetector.Type)` | L9353 | setCornerDetector(*args, **kwargs) |
| `@overload` `def setCornerDetector(self, config: FeatureTrackerConfig.CornerDetector) -> FeatureTrackerConfig` | `(self, config: FeatureTrackerConfig.CornerDetector)` | L9372 | setCornerDetector(*args, **kwargs) |
| `@overload` `def setFeatureMaintainer(self, enable: bool) -> FeatureTrackerConfig` | `(self, enable: bool)` | L9391 | setFeatureMaintainer(*args, **kwargs) |
| `@overload` `def setFeatureMaintainer(self, config: FeatureTrackerConfig.FeatureMaintainer) -> FeatureTrackerConfig` | `(self, config: FeatureTrackerConfig.FeatureMaintainer)` | L9409 | setFeatureMaintainer(*args, **kwargs) |
| `def setHwMotionEstimation(self) -> FeatureTrackerConfig` | `(self)` | L9426 | setHwMotionEstimation(self: depthai.FeatureTrackerConfig) -> depthai.FeatureTrackerConfig |
| `@overload` `def setMotionEstimator(self, enable: bool) -> FeatureTrackerConfig` | `(self, enable: bool)` | L9433 | setMotionEstimator(*args, **kwargs) |
| `@overload` `def setMotionEstimator(self, config: FeatureTrackerConfig.MotionEstimator) -> FeatureTrackerConfig` | `(self, config: FeatureTrackerConfig.MotionEstimator)` | L9451 | setMotionEstimator(*args, **kwargs) |
| `def setNumTargetFeatures(self, numTargetFeatures: int) -> FeatureTrackerConfig` | `(self, numTargetFeatures: int)` | L9468 | setNumTargetFeatures(self: depthai.FeatureTrackerConfig, numTargetFeatures: int) -> depthai.FeatureTrackerConfig |
| `@overload` `def setOpticalFlow(self) -> FeatureTrackerConfig` | `(self)` | L9477 | setOpticalFlow(*args, **kwargs) |
| `@overload` `def setOpticalFlow(self, config: FeatureTrackerConfig.MotionEstimator.OpticalFlow) -> FeatureTrackerConfig` | `(self, config: FeatureTrackerConfig.MotionEstimator.OpticalFlow)` | L9493 | setOpticalFlow(*args, **kwargs) |

**Nested Class:**

<a id="class-cornerdetector"></a>
#### class `CornerDetector`  — L9234

> Corner detector configuration structure.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `cellGridDimension` | `int` | — | L9280 |
| `enableSobel` | `bool` | — | L9281 |
| `enableSorting` | `bool` | — | L9282 |
| `numMaxFeatures` | `int` | — | L9283 |
| `numTargetFeatures` | `int` | — | L9284 |
| `thresholds` | `FeatureTrackerConfig.CornerDetector.Thresholds` | — | L9285 |
| `type` | `FeatureTrackerConfig.CornerDetector.Type` | — | L9286 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9287 | __init__(self: depthai.FeatureTrackerConfig.CornerDetector) -> None |

**Nested Class:**

<a id="class-thresholds"></a>
##### class `Thresholds`  — L9237

> Threshold settings structure for corner detector.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `decreaseFactor` | `float` | — | L9239 |
| `increaseFactor` | `float` | — | L9240 |
| `initialValue` | `float` | — | L9241 |
| `max` | `float` | — | L9242 |
| `min` | `float` | — | L9243 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9244 | __init__(self: depthai.FeatureTrackerConfig.CornerDetector.Thresholds) -> None |

**Nested Class:**

<a id="class-type"></a>
##### class `Type`  — L9247

> Members:

  HARRIS

  SHI_THOMASI

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L9255 |
| `HARRIS` | `ClassVar[FeatureTrackerConfig.CornerDetector.Type]` | `...` | L9256 |
| `SHI_THOMASI` | `ClassVar[FeatureTrackerConfig.CornerDetector.Type]` | `...` | L9257 |
| `__entries` | `ClassVar[dict]` | `...` | L9258 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L9259 | __init__(self: depthai.FeatureTrackerConfig.CornerDetector.Type, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L9261 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L9263 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L9265 | __index__(self: depthai.FeatureTrackerConfig.CornerDetector.Type) -> int |
| `def __int__(self) -> int` | `(self)` | L9267 | __int__(self: depthai.FeatureTrackerConfig.CornerDetector.Type) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L9269 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L9272 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L9278 | (arg0: depthai.FeatureTrackerConfig.CornerDetector.Type) -> int |

**Nested Class:**

<a id="class-featuremaintainer"></a>
#### class `FeatureMaintainer`  — L9290

> FeatureMaintainer configuration structure.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `enable` | `bool` | — | L9292 |
| `lostFeatureErrorThreshold` | `float` | — | L9293 |
| `minimumDistanceBetweenFeatures` | `float` | — | L9294 |
| `trackedFeatureThreshold` | `float` | — | L9295 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9296 | __init__(self: depthai.FeatureTrackerConfig.FeatureMaintainer) -> None |

**Nested Class:**

<a id="class-motionestimator"></a>
#### class `MotionEstimator`  — L9299

> Used for feature reidentification between current and previous features.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `enable` | `bool` | — | L9345 |
| `opticalFlow` | `FeatureTrackerConfig.MotionEstimator.OpticalFlow` | — | L9346 |
| `type` | `FeatureTrackerConfig.MotionEstimator.Type` | — | L9347 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9348 | __init__(self: depthai.FeatureTrackerConfig.MotionEstimator) -> None |

**Nested Class:**

<a id="class-opticalflow"></a>
##### class `OpticalFlow`  — L9302

> Optical flow configuration structure.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `epsilon` | `float` | — | L9304 |
| `maxIterations` | `int` | — | L9305 |
| `pyramidLevels` | `int` | — | L9306 |
| `searchWindowHeight` | `int` | — | L9307 |
| `searchWindowWidth` | `int` | — | L9308 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9309 | __init__(self: depthai.FeatureTrackerConfig.MotionEstimator.OpticalFlow) -> None |

**Nested Class:**

<a id="class-type"></a>
##### class `Type`  — L9312

> Members:

  LUCAS_KANADE_OPTICAL_FLOW

  HW_MOTION_ESTIMATION

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L9320 |
| `HW_MOTION_ESTIMATION` | `ClassVar[FeatureTrackerConfig.MotionEstimator.Type]` | `...` | L9321 |
| `LUCAS_KANADE_OPTICAL_FLOW` | `ClassVar[FeatureTrackerConfig.MotionEstimator.Type]` | `...` | L9322 |
| `__entries` | `ClassVar[dict]` | `...` | L9323 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L9324 | __init__(self: depthai.FeatureTrackerConfig.MotionEstimator.Type, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L9326 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L9328 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L9330 | __index__(self: depthai.FeatureTrackerConfig.MotionEstimator.Type) -> int |
| `def __int__(self) -> int` | `(self)` | L9332 | __int__(self: depthai.FeatureTrackerConfig.MotionEstimator.Type) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L9334 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L9337 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L9343 | (arg0: depthai.FeatureTrackerConfig.MotionEstimator.Type) -> int |

<a id="class-featuretrackerproperties"></a>
### class `FeatureTrackerProperties`  — L9509

> Specify properties for FeatureTracker

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `initialConfig` | `FeatureTrackerConfig` | — | L9511 |
| `numMemorySlices` | `int` | — | L9512 |
| `numShaves` | `int` | — | L9513 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L9514 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-filegroup"></a>
### class `FileGroup`  — L9517

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9518 | __init__(self: depthai.FileGroup) -> None |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def addFile(self, fileName: str, data: str, mimeType: str) -> None` | `(self, fileName: str, data: str, mimeType: str)` | L9521 | addFile(*args, **kwargs) |
| `@overload` `def addFile(self, fileName: str, filePath: os.PathLike) -> None` | `(self, fileName: str, filePath: os.PathLike)` | L9536 | addFile(*args, **kwargs) |
| `@overload` `def addFile(self, fileName: str | None, imgFrame: ImgFrame) -> None` | `(self, fileName: str | None, imgFrame: ImgFrame)` | L9551 | addFile(*args, **kwargs) |
| `@overload` `def addFile(self, fileName: str | None, encodedFrame: EncodedFrame) -> None` | `(self, fileName: str | None, encodedFrame: EncodedFrame)` | L9566 | addFile(*args, **kwargs) |
| `@overload` `def addFile(self, fileName: str | None, imgDetections: ImgDetections) -> None` | `(self, fileName: str | None, imgDetections: ImgDetections)` | L9581 | addFile(*args, **kwargs) |
| `@overload` `def addImageDetectionsPair(self, fileName: str | None, imgFrame: ImgFrame, imgDetections: ImgDetections) -> None` | `(self, fileName: str | None, imgFrame: ImgFrame, imgDetections: ImgDetections)` | L9596 | addImageDetectionsPair(*args, **kwargs) |
| `@overload` `def addImageDetectionsPair(self, fileName: str | None, encodedFrame: EncodedFrame, imgDetections: ImgDetections) -> None` | `(self, fileName: str | None, encodedFrame: EncodedFrame, imgDetections: ImgDetections)` | L9605 | addImageDetectionsPair(*args, **kwargs) |

<a id="class-frameevent"></a>
### class `FrameEvent`  — L9614

> Members:

  NONE

  READOUT_START

  READOUT_END

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L9624 |
| `NONE` | `ClassVar[FrameEvent]` | `...` | L9625 |
| `READOUT_END` | `ClassVar[FrameEvent]` | `...` | L9626 |
| `READOUT_START` | `ClassVar[FrameEvent]` | `...` | L9627 |
| `__entries` | `ClassVar[dict]` | `...` | L9628 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L9629 | __init__(self: depthai.FrameEvent, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L9631 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L9633 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L9635 | __index__(self: depthai.FrameEvent) -> int |
| `def __int__(self) -> int` | `(self)` | L9637 | __int__(self: depthai.FrameEvent) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L9639 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L9642 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L9648 | (arg0: depthai.FrameEvent) -> int |

<a id="class-globalproperties"></a>
### class `GlobalProperties`  — L9651

> Specify properties which apply for whole pipeline

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `cameraTuningBlobSize` | `int | None` | — | L9653 |
| `cameraTuningBlobUri` | `str` | — | L9654 |
| `leonOsFrequencyHz` | `float` | — | L9655 |
| `leonRtFrequencyHz` | `float` | — | L9656 |
| `pipelineName` | `str | None` | — | L9657 |
| `pipelineVersion` | `str | None` | — | L9658 |
| `sippBufferSize` | `int` | — | L9659 |
| `sippDmaBufferSize` | `int` | — | L9660 |
| `xlinkChunkSize` | `int` | — | L9661 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L9662 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-housingcoordinatesystem"></a>
### class `HousingCoordinateSystem`  — L9665

> Which Housing to use.

AUTO denotes that the decision will be made by device

Members:

  CAM_A

  CAM_B

  CAM_C

  CAM_D

  CAM_E

  CAM_F

  CAM_G

  CAM_H

  CAM_I

  CAM_J

  FRONT_CAM_A

  FRONT_CAM_B

  FRONT_CAM_C

  FRONT_CAM_D

  FRONT_CAM_E

  FRONT_CAM_F

  FRONT_CAM_G

  FRONT_CAM_H

  FRONT_CAM_I

  FRONT_CAM_J

  VESA_A

  VESA_B

  VESA_C

  VESA_D

  VESA_E

  VESA_F

  VESA_G

  VESA_H

  VESA_I

  VESA_J

  IMU

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L9733 |
| `CAM_A` | `ClassVar[HousingCoordinateSystem]` | `...` | L9734 |
| `CAM_B` | `ClassVar[HousingCoordinateSystem]` | `...` | L9735 |
| `CAM_C` | `ClassVar[HousingCoordinateSystem]` | `...` | L9736 |
| `CAM_D` | `ClassVar[HousingCoordinateSystem]` | `...` | L9737 |
| `CAM_E` | `ClassVar[HousingCoordinateSystem]` | `...` | L9738 |
| `CAM_F` | `ClassVar[HousingCoordinateSystem]` | `...` | L9739 |
| `CAM_G` | `ClassVar[HousingCoordinateSystem]` | `...` | L9740 |
| `CAM_H` | `ClassVar[HousingCoordinateSystem]` | `...` | L9741 |
| `CAM_I` | `ClassVar[HousingCoordinateSystem]` | `...` | L9742 |
| `CAM_J` | `ClassVar[HousingCoordinateSystem]` | `...` | L9743 |
| `FRONT_CAM_A` | `ClassVar[HousingCoordinateSystem]` | `...` | L9744 |
| `FRONT_CAM_B` | `ClassVar[HousingCoordinateSystem]` | `...` | L9745 |
| `FRONT_CAM_C` | `ClassVar[HousingCoordinateSystem]` | `...` | L9746 |
| `FRONT_CAM_D` | `ClassVar[HousingCoordinateSystem]` | `...` | L9747 |
| `FRONT_CAM_E` | `ClassVar[HousingCoordinateSystem]` | `...` | L9748 |
| `FRONT_CAM_F` | `ClassVar[HousingCoordinateSystem]` | `...` | L9749 |
| `FRONT_CAM_G` | `ClassVar[HousingCoordinateSystem]` | `...` | L9750 |
| `FRONT_CAM_H` | `ClassVar[HousingCoordinateSystem]` | `...` | L9751 |
| `FRONT_CAM_I` | `ClassVar[HousingCoordinateSystem]` | `...` | L9752 |
| `FRONT_CAM_J` | `ClassVar[HousingCoordinateSystem]` | `...` | L9753 |
| `IMU` | `ClassVar[HousingCoordinateSystem]` | `...` | L9754 |
| `VESA_A` | `ClassVar[HousingCoordinateSystem]` | `...` | L9755 |
| `VESA_B` | `ClassVar[HousingCoordinateSystem]` | `...` | L9756 |
| `VESA_C` | `ClassVar[HousingCoordinateSystem]` | `...` | L9757 |
| `VESA_D` | `ClassVar[HousingCoordinateSystem]` | `...` | L9758 |
| `VESA_E` | `ClassVar[HousingCoordinateSystem]` | `...` | L9759 |
| `VESA_F` | `ClassVar[HousingCoordinateSystem]` | `...` | L9760 |
| `VESA_G` | `ClassVar[HousingCoordinateSystem]` | `...` | L9761 |
| `VESA_H` | `ClassVar[HousingCoordinateSystem]` | `...` | L9762 |
| `VESA_I` | `ClassVar[HousingCoordinateSystem]` | `...` | L9763 |
| `VESA_J` | `ClassVar[HousingCoordinateSystem]` | `...` | L9764 |
| `__entries` | `ClassVar[dict]` | `...` | L9765 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L9766 | __init__(self: depthai.HousingCoordinateSystem, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L9768 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L9770 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L9772 | __index__(self: depthai.HousingCoordinateSystem) -> int |
| `def __int__(self) -> int` | `(self)` | L9774 | __int__(self: depthai.HousingCoordinateSystem) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L9776 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L9779 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L9785 | (arg0: depthai.HousingCoordinateSystem) -> int |

<a id="class-imudata"></a>
### class `IMUData(Buffer)`  — L9788

> IMUData message. Carries normalized detection results

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `packets` | `list[IMUPacket]` | — | L9790 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9791 | __init__(self: depthai.IMUData) -> None |

<a id="class-imupacket"></a>
### class `IMUPacket`  — L9794

> IMU output

Contains combined output for all possible modes. Only the enabled outputs are
populated.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `acceleroMeter` | `IMUReportAccelerometer` | — | L9799 |
| `gyroscope` | `IMUReportGyroscope` | — | L9800 |
| `magneticField` | `IMUReportMagneticField` | — | L9801 |
| `rotationVector` | `IMUReportRotationVectorWAcc` | — | L9802 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9803 | __init__(self: depthai.IMUPacket) -> None |

<a id="class-imuproperties"></a>
### class `IMUProperties`  — L9806

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `batchReportThreshold` | `int` | — | L9807 |
| `enableFirmwareUpdate` | `bool | None` | — | L9808 |
| `imuSensors` | `list[IMUSensorConfig]` | — | L9809 |
| `maxBatchReports` | `int` | — | L9810 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L9811 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-imureport"></a>
### class `IMUReport`  — L9814

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `accuracy` | `IMUReport.Accuracy` | — | L9852 |
| `sequence` | `int` | — | L9853 |
| `timestamp` | `Timestamp` | — | L9854 |
| `tsDevice` | `Timestamp` | — | L9855 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9856 | __init__(self: depthai.IMUReport) -> None |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getSequenceNum(self) -> int` | `(self)` | L9858 | getSequenceNum(self: depthai.IMUReport) -> int |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L9863 | getTimestamp(self: depthai.IMUReport) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L9868 | getTimestampDevice(self: depthai.IMUReport) -> datetime.timedelta |

**Nested Class:**

<a id="class-accuracy"></a>
#### class `Accuracy`  — L9815

> Members:

UNRELIABLE

LOW

MEDIUM

HIGH

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L9825 |
| `HIGH` | `ClassVar[IMUReport.Accuracy]` | `...` | L9826 |
| `LOW` | `ClassVar[IMUReport.Accuracy]` | `...` | L9827 |
| `MEDIUM` | `ClassVar[IMUReport.Accuracy]` | `...` | L9828 |
| `UNRELIABLE` | `ClassVar[IMUReport.Accuracy]` | `...` | L9829 |
| `__entries` | `ClassVar[dict]` | `...` | L9830 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L9831 | __init__(self: depthai.IMUReport.Accuracy, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L9833 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L9835 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L9837 | __index__(self: depthai.IMUReport.Accuracy) -> int |
| `def __int__(self) -> int` | `(self)` | L9839 | __int__(self: depthai.IMUReport.Accuracy) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L9841 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L9844 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L9850 | (arg0: depthai.IMUReport.Accuracy) -> int |

<a id="class-imureportaccelerometer"></a>
### class `IMUReportAccelerometer(IMUReport)`  — L9875

> Accelerometer

Units are [m/s^2]

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `x` | `float` | — | L9879 |
| `y` | `float` | — | L9880 |
| `z` | `float` | — | L9881 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9882 | __init__(self: depthai.IMUReportAccelerometer) -> None |

<a id="class-imureportgyroscope"></a>
### class `IMUReportGyroscope(IMUReport)`  — L9885

> Gyroscope

Units are [rad/s]

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `x` | `float` | — | L9889 |
| `y` | `float` | — | L9890 |
| `z` | `float` | — | L9891 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9892 | __init__(self: depthai.IMUReportGyroscope) -> None |

<a id="class-imureportmagneticfield"></a>
### class `IMUReportMagneticField(IMUReport)`  — L9895

> Magnetic field

Units are [uTesla]

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `x` | `float` | — | L9899 |
| `y` | `float` | — | L9900 |
| `z` | `float` | — | L9901 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9902 | __init__(self: depthai.IMUReportMagneticField) -> None |

<a id="class-imureportrotationvectorwacc"></a>
### class `IMUReportRotationVectorWAcc(IMUReport)`  — L9905

> Rotation Vector with Accuracy

Contains quaternion components: i,j,k,real

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `i` | `float` | — | L9909 |
| `j` | `float` | — | L9910 |
| `k` | `float` | — | L9911 |
| `real` | `float` | — | L9912 |
| `rotationVectorAccuracy` | `float` | — | L9913 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L9914 | __init__(self: depthai.IMUReportRotationVectorWAcc) -> None |

<a id="class-imusensor"></a>
### class `IMUSensor`  — L9917

> Available IMU sensors. More details about each sensor can be found in the
datasheet:

https://www.ceva-dsp.com/wp-content/uploads/2019/10/BNO080_085-Datasheet.pdf

Members:

  ACCELEROMETER_RAW : Section 2.1.1

Acceleration of the device without any postprocessing, straight from the sensor.
Units are [m/s^2]

  ACCELEROMETER : Section 2.1.1

Acceleration of the device including gravity. Units are [m/s^2]

  LINEAR_ACCELERATION : Section 2.1.1

Acceleration of the device with gravity removed. Units are [m/s^2]

  GRAVITY : Section 2.1.1

Gravity. Units are [m/s^2]

  GYROSCOPE_RAW : Section 2.1.2

The angular velocity of the device without any postprocessing, straight from the
sensor. Units are [rad/s]

  GYROSCOPE_CALIBRATED : Section 2.1.2

The angular velocity of the device. Units are [rad/s]

  GYROSCOPE_UNCALIBRATED : Section 2.1.2

Angular velocity without bias compensation. Units are [rad/s]

  MAGNETOMETER_RAW : Section 2.1.3

Magnetic field measurement without any postprocessing, straight from the sensor.
Units are [uTesla]

  MAGNETOMETER_CALIBRATED : Section 2.1.3

The fully calibrated magnetic field measurement. Units are [uTesla]

  MAGNETOMETER_UNCALIBRATED : Section 2.1.3

The magnetic field measurement without hard-iron offset applied. Units are
[uTesla]

  ROTATION_VECTOR : Section 2.2

The rotation vector provides an orientation output that is expressed as a
quaternion referenced to magnetic north and gravity. It is produced by fusing
the outputs of the accelerometer, gyroscope and magnetometer. The rotation
vector is the most accurate orientation estimate available. The magnetometer
provides correction in yaw to reduce drift and the gyroscope enables the most
responsive performance.

  GAME_ROTATION_VECTOR : Section 2.2

The game rotation vector is an orientation output that is expressed as a
quaternion with no specific reference for heading, while roll and pitch are
referenced against gravity. It is produced by fusing the outputs of the
accelerometer and the gyroscope (i.e. no magnetometer). The game rotation vector
does not use the magnetometer to correct the gyroscopes drift in yaw. This is a
deliberate omission (as specified by Google) to allow gaming applications to use
a smoother representation of the orientation without the jumps that an
instantaneous correction provided by a magnetic field update could provide. Long
term the output will likely drift in yaw due to the characteristics of
gyroscopes, but this is seen as preferable for this output versus a corrected
output.

  GEOMAGNETIC_ROTATION_VECTOR : Section 2.2

The geomagnetic rotation vector is an orientation output that is expressed as a
quaternion referenced to magnetic north and gravity. It is produced by fusing
the outputs of the accelerometer and magnetometer. The gyroscope is specifically
excluded in order to produce a rotation vector output using less power than is
required to produce the rotation vector of section 2.2.4. The consequences of
removing the gyroscope are: Less responsive output since the highly dynamic
outputs of the gyroscope are not used More errors in the presence of varying
magnetic fields.

  ARVR_STABILIZED_ROTATION_VECTOR : Section 2.2

Estimates of the magnetic field and the roll/pitch of the device can create a
potential correction in the rotation vector produced. For applications
(typically augmented or virtual reality applications) where a sudden jump can be
disturbing, the output is adjusted to prevent these jumps in a manner that takes
account of the velocity of the sensor system.

  ARVR_STABILIZED_GAME_ROTATION_VECTOR : Section 2.2

While the magnetometer is removed from the calculation of the game rotation
vector, the accelerometer itself can create a potential correction in the
rotation vector produced (i.e. the estimate of gravity changes). For
applications (typically augmented or virtual reality applications) where a
sudden jump can be disturbing, the output is adjusted to prevent these jumps in
a manner that takes account of the velocity of the sensor system. This process
is called AR/VR stabilization.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L10020 |
| `ACCELEROMETER` | `ClassVar[IMUSensor]` | `...` | L10021 |
| `ACCELEROMETER_RAW` | `ClassVar[IMUSensor]` | `...` | L10022 |
| `ARVR_STABILIZED_GAME_ROTATION_VECTOR` | `ClassVar[IMUSensor]` | `...` | L10023 |
| `ARVR_STABILIZED_ROTATION_VECTOR` | `ClassVar[IMUSensor]` | `...` | L10024 |
| `GAME_ROTATION_VECTOR` | `ClassVar[IMUSensor]` | `...` | L10025 |
| `GEOMAGNETIC_ROTATION_VECTOR` | `ClassVar[IMUSensor]` | `...` | L10026 |
| `GRAVITY` | `ClassVar[IMUSensor]` | `...` | L10027 |
| `GYROSCOPE_CALIBRATED` | `ClassVar[IMUSensor]` | `...` | L10028 |
| `GYROSCOPE_RAW` | `ClassVar[IMUSensor]` | `...` | L10029 |
| `GYROSCOPE_UNCALIBRATED` | `ClassVar[IMUSensor]` | `...` | L10030 |
| `LINEAR_ACCELERATION` | `ClassVar[IMUSensor]` | `...` | L10031 |
| `MAGNETOMETER_CALIBRATED` | `ClassVar[IMUSensor]` | `...` | L10032 |
| `MAGNETOMETER_RAW` | `ClassVar[IMUSensor]` | `...` | L10033 |
| `MAGNETOMETER_UNCALIBRATED` | `ClassVar[IMUSensor]` | `...` | L10034 |
| `ROTATION_VECTOR` | `ClassVar[IMUSensor]` | `...` | L10035 |
| `__entries` | `ClassVar[dict]` | `...` | L10036 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L10037 | __init__(self: depthai.IMUSensor, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L10039 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L10041 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L10043 | __index__(self: depthai.IMUSensor) -> int |
| `def __int__(self) -> int` | `(self)` | L10045 | __int__(self: depthai.IMUSensor) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L10047 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L10050 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L10056 | (arg0: depthai.IMUSensor) -> int |

<a id="class-imusensorconfig"></a>
### class `IMUSensorConfig`  — L10059

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `changeSensitivity` | `int` | — | L10060 |
| `reportRate` | `int` | — | L10061 |
| `sensitivityEnabled` | `bool` | — | L10062 |
| `sensitivityRelative` | `bool` | — | L10063 |
| `sensorId` | `IMUSensor` | — | L10064 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L10065 | __init__(self: depthai.IMUSensorConfig) -> None |

<a id="class-imagealignconfig"></a>
### class `ImageAlignConfig(Buffer)`  — L10068

> ImageAlignConfig configuration structure

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `staticDepthPlane` | `int` | — | L10070 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L10071 | __init__(self: depthai.ImageAlignConfig) -> None |

<a id="class-imagealignproperties"></a>
### class `ImageAlignProperties`  — L10074

> Specify properties for ImageAlign

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `alignHeight` | `int` | — | L10076 |
| `alignWidth` | `int` | — | L10077 |
| `initialConfig` | `ImageAlignConfig` | — | L10078 |
| `interpolation` | `Interpolation` | — | L10079 |
| `numFramesPool` | `int` | — | L10080 |
| `numShaves` | `int` | — | L10081 |
| `outKeepAspectRatio` | `bool` | — | L10082 |
| `warpHwIds` | `list[int]` | — | L10083 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L10084 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-imagefiltersconfig"></a>
### class `ImageFiltersConfig(Buffer)`  — L10087

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `filterIndices` | `list[int]` | — | L10088 |
| `filterParams` | `Incomplete` | — | L10089 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L10090 | __init__(self: depthai.ImageFiltersConfig) -> None |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def insertFilter(self, params) -> ImageFiltersConfig` | `(self, params)` | L10092 | insertFilter(self: depthai.ImageFiltersConfig, params: Union[dai::filters::params::MedianFilter, dai::filters::params::SpatialFilter, dai::filters::params::SpeckleFilter, dai::filters::params::TemporalFilter]) -> depthai.ImageFiltersConfig |
| `def setProfilePreset(self, arg0) -> None` | `(self, arg0)` | L10100 | setProfilePreset(self: depthai.ImageFiltersConfig, arg0: dai::ImageFiltersPresetMode) -> None |
| `def updateFilterAtIndex(self, index: int, params) -> ImageFiltersConfig` | `(self, index: int, params)` | L10108 | updateFilterAtIndex(self: depthai.ImageFiltersConfig, index: int, params: Union[dai::filters::params::MedianFilter, dai::filters::params::SpatialFilter, dai::filters::params::SpeckleFilter, dai::filters::params::TemporalFilter]) -> depthai.ImageFiltersConfig |

<a id="class-imagefilterspresetmode"></a>
### class `ImageFiltersPresetMode`  — L10121

> Members:

TOF_LOW_RANGE

TOF_MID_RANGE

TOF_HIGH_RANGE

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L10129 |
| `TOF_HIGH_RANGE` | `ClassVar[ImageFiltersPresetMode]` | `...` | L10130 |
| `TOF_LOW_RANGE` | `ClassVar[ImageFiltersPresetMode]` | `...` | L10131 |
| `TOF_MID_RANGE` | `ClassVar[ImageFiltersPresetMode]` | `...` | L10132 |
| `__entries` | `ClassVar[dict]` | `...` | L10133 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L10134 | __init__(self: depthai.ImageFiltersPresetMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L10136 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L10138 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L10140 | __index__(self: depthai.ImageFiltersPresetMode) -> int |
| `def __int__(self) -> int` | `(self)` | L10142 | __int__(self: depthai.ImageFiltersPresetMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L10144 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L10147 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L10153 | (arg0: depthai.ImageFiltersPresetMode) -> int |

<a id="class-imagefiltersproperties"></a>
### class `ImageFiltersProperties`  — L10156

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L10157 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-imagemanipconfig"></a>
### class `ImageManipConfig(Buffer)`  — L10160

> ImageManipConfig message. Specifies image manipulation options like:

- Crop

- Resize

- Warp

- ...

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L10208 | __init__(self: depthai.ImageManipConfig) -> None |

**🔹 Public Methods (24):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def addCrop(self, x: int, y: int, w: int, h: int) -> ImageManipConfig` | `(self, x: int, y: int, w: int, h: int)` | L10211 | addCrop(*args, **kwargs) |
| `@overload` `def addCrop(self, rect: Rect, normalizedCoords: bool) -> ImageManipConfig` | `(self, rect: Rect, normalizedCoords: bool)` | L10248 | addCrop(*args, **kwargs) |
| `def addCropRotatedRect(self, rect: RotatedRect, normalizedCoords: bool) -> ImageManipConfig` | `(self, rect: RotatedRect, normalizedCoords: bool)` | L10284 | addCropRotatedRect(self: depthai.ImageManipConfig, rect: depthai.RotatedRect, normalizedCoords: bool) -> depthai.ImageManipConfig |
| `def addFlipHorizontal(self) -> ImageManipConfig` | `(self)` | L10296 | addFlipHorizontal(self: depthai.ImageManipConfig) -> depthai.ImageManipConfig |
| `def addFlipVertical(self) -> ImageManipConfig` | `(self)` | L10301 | addFlipVertical(self: depthai.ImageManipConfig) -> depthai.ImageManipConfig |
| `@overload` `def addRotateDeg(self, angle: float) -> ImageManipConfig` | `(self, angle: float)` | L10307 | addRotateDeg(*args, **kwargs) |
| `@overload` `def addRotateDeg(self, angle: float, center: Point2f) -> ImageManipConfig` | `(self, angle: float, center: Point2f)` | L10326 | addRotateDeg(*args, **kwargs) |
| `@overload` `def addScale(self, scale: float) -> ImageManipConfig` | `(self, scale: float)` | L10345 | addScale(*args, **kwargs) |
| `@overload` `def addScale(self, scaleX: float, scaleY: float) -> ImageManipConfig` | `(self, scaleX: float, scaleY: float)` | L10372 | addScale(*args, **kwargs) |
| `def addTransformAffine(self, mat) -> ImageManipConfig` | `(self, mat)` | L10398 | addTransformAffine(self: depthai.ImageManipConfig, mat: Annotated[list[float], FixedSize(4)]) -> depthai.ImageManipConfig |
| `def addTransformFourPoints(self, src, dst, normalizedCoords: bool) -> ImageManipConfig` | `(self, src, dst, normalizedCoords: bool)` | L10406 | addTransformFourPoints(self: depthai.ImageManipConfig, src: Annotated[list[depthai.Point2f], FixedSize(4)], dst: Annotated[list[depthai.Point2f], FixedSize(4)], normalizedCoords: bool) -> depthai.ImageManipConfig |
| `def addTransformPerspective(self, mat) -> ImageManipConfig` | `(self, mat)` | L10421 | addTransformPerspective(self: depthai.ImageManipConfig, mat: Annotated[list[float], FixedSize(9)]) -> depthai.ImageManipConfig |
| `def clearOps(self) -> ImageManipConfig` | `(self)` | L10429 | clearOps(self: depthai.ImageManipConfig) -> depthai.ImageManipConfig |
| `def getUndistort(self) -> bool` | `(self)` | L10434 | getUndistort(self: depthai.ImageManipConfig) -> bool |
| `@overload` `def setBackgroundColor(self, r: int, g: int, b: int) -> ImageManipConfig` | `(self, r: int, g: int, b: int)` | L10443 | setBackgroundColor(*args, **kwargs) |
| `@overload` `def setBackgroundColor(self, val: int) -> ImageManipConfig` | `(self, val: int)` | L10474 | setBackgroundColor(*args, **kwargs) |
| `@overload` `def setColormap(self, colormap: Colormap) -> ImageManipConfig` | `(self, colormap: Colormap)` | L10505 | setColormap(*args, **kwargs) |
| `@overload` `def setColormap(self, colormap: Colormap) -> ImageManipConfig` | `(self, colormap: Colormap)` | L10524 | setColormap(*args, **kwargs) |
| `def setFrameType(self, type: ImgFrame.Type) -> ImageManipConfig` | `(self, type: ImgFrame.Type)` | L10542 | setFrameType(self: depthai.ImageManipConfig, type: depthai.ImgFrame.Type) -> depthai.ImageManipConfig |
| `def setOutputCenter(self, c: bool) -> ImageManipConfig` | `(self, c: bool)` | L10550 | setOutputCenter(self: depthai.ImageManipConfig, c: bool) -> depthai.ImageManipConfig |
| `def setOutputSize(self, w: int, h: int, mode: ImageManipConfig.ResizeMode = ...) -> ImageManipConfig` | `(self, w: int, h: int, mode: ImageManipConfig.ResizeMode = ...)` | L10558 | setOutputSize(self: depthai.ImageManipConfig, w: int, h: int, mode: depthai.ImageManipConfig.ResizeMode = <ResizeMode.STRETCH: 1>) -> depthai.ImageManipConfig |
| `def setReusePreviousImage(self, reuse: bool) -> ImageManipConfig` | `(self, reuse: bool)` | L10574 | setReusePreviousImage(self: depthai.ImageManipConfig, reuse: bool) -> depthai.ImageManipConfig |
| `def setSkipCurrentImage(self, skip: bool) -> ImageManipConfig` | `(self, skip: bool)` | L10583 | setSkipCurrentImage(self: depthai.ImageManipConfig, skip: bool) -> depthai.ImageManipConfig |
| `def setUndistort(self, undistort: bool) -> ImageManipConfig` | `(self, undistort: bool)` | L10591 | setUndistort(self: depthai.ImageManipConfig, undistort: bool) -> depthai.ImageManipConfig |

**Nested Class:**

<a id="class-resizemode"></a>
#### class `ResizeMode`  — L10171

> Members:

NONE

LETTERBOX

CENTER_CROP

STRETCH

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L10181 |
| `CENTER_CROP` | `ClassVar[ImageManipConfig.ResizeMode]` | `...` | L10182 |
| `LETTERBOX` | `ClassVar[ImageManipConfig.ResizeMode]` | `...` | L10183 |
| `NONE` | `ClassVar[ImageManipConfig.ResizeMode]` | `...` | L10184 |
| `STRETCH` | `ClassVar[ImageManipConfig.ResizeMode]` | `...` | L10185 |
| `__entries` | `ClassVar[dict]` | `...` | L10186 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L10187 | __init__(self: depthai.ImageManipConfig.ResizeMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L10189 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L10191 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L10193 | __index__(self: depthai.ImageManipConfig.ResizeMode) -> int |
| `def __int__(self) -> int` | `(self)` | L10195 | __int__(self: depthai.ImageManipConfig.ResizeMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L10197 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L10200 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L10206 | (arg0: depthai.ImageManipConfig.ResizeMode) -> int |

<a id="class-imgannotation"></a>
### class `ImgAnnotation`  — L10597

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `circles` | `VectorCircleAnnotation` | — | L10598 |
| `points` | `VectorPointsAnnotation` | — | L10599 |
| `texts` | `VectorTextAnnotation` | — | L10600 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L10601 | __init__(self: depthai.ImgAnnotation) -> None |

<a id="class-imgannotations"></a>
### class `ImgAnnotations(Buffer)`  — L10604

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `annotations` | `VectorImgAnnotation` | — | L10605 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L10607 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: VectorImgAnnotation) -> None` | `(self, arg0: VectorImgAnnotation)` | L10618 | __init__(*args, **kwargs) |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getSequenceNum(self) -> int` | `(self)` | L10628 | getSequenceNum(self: depthai.ImgAnnotations) -> int |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L10633 | getTimestamp(self: depthai.ImgAnnotations) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L10638 | getTimestampDevice(self: depthai.ImgAnnotations) -> datetime.timedelta |

<a id="class-imgdetection"></a>
### class `ImgDetection`  — L10645

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `confidence` | `float` | — | L10646 |
| `label` | `int` | — | L10647 |
| `labelName` | `str` | — | L10648 |
| `xmax` | `float` | — | L10649 |
| `xmin` | `float` | — | L10650 |
| `ymax` | `float` | — | L10651 |
| `ymin` | `float` | — | L10652 |

**🔧 Dunder Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L10654 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, boundingBox: RotatedRect, confidence: float, label: int) -> None` | `(self, boundingBox: RotatedRect, confidence: float, label: int)` | L10669 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, boundingBox: RotatedRect, labelName: str, confidence: float, label: int) -> None` | `(self, boundingBox: RotatedRect, labelName: str, confidence: float, label: int)` | L10684 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, boundingBox: RotatedRect, keypoints: KeypointsList, confidence: float, label: int) -> None` | `(self, boundingBox: RotatedRect, keypoints: KeypointsList, confidence: float, label: int)` | L10699 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, boundingBox: RotatedRect, keypoints: KeypointsList, labelName: str, confidence: float, label: int) -> None` | `(self, boundingBox: RotatedRect, keypoints: KeypointsList, labelName: str, confidence: float, label: int)` | L10714 | __init__(*args, **kwargs) |

**🔹 Public Methods (18):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getAngle(self) -> float` | `(self)` | L10728 | getAngle(self: depthai.ImgDetection) -> float |
| `def getBoundingBox(self) -> RotatedRect` | `(self)` | L10730 | getBoundingBox(self: depthai.ImgDetection) -> depthai.RotatedRect |
| `def getCenterX(self) -> float` | `(self)` | L10732 | getCenterX(self: depthai.ImgDetection) -> float |
| `def getCenterY(self) -> float` | `(self)` | L10734 | getCenterY(self: depthai.ImgDetection) -> float |
| `def getEdges(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L10736 | getEdges(self: depthai.ImgDetection) -> list[Annotated[list[int], FixedSize(2)]] |
| `def getHeight(self) -> float` | `(self)` | L10742 | getHeight(self: depthai.ImgDetection) -> float |
| `def getKeypoints(self) -> list[Keypoint]` | `(self)` | L10744 | getKeypoints(self: depthai.ImgDetection) -> list[depthai.Keypoint] |
| `def getKeypoints2f(self) -> VectorPoint2f` | `(self)` | L10749 | getKeypoints2f(self: depthai.ImgDetection) -> depthai.VectorPoint2f |
| `def getKeypoints3f(self) -> list[Point3f]` | `(self)` | L10755 | getKeypoints3f(self: depthai.ImgDetection) -> list[depthai.Point3f] |
| `def getWidth(self) -> float` | `(self)` | L10761 | getWidth(self: depthai.ImgDetection) -> float |
| `def setBoundingBox(self, boundingBox: RotatedRect) -> None` | `(self, boundingBox: RotatedRect)` | L10763 | setBoundingBox(self: depthai.ImgDetection, boundingBox: depthai.RotatedRect) -> None |
| `def setEdges(self, edges) -> None` | `(self, edges)` | L10765 | setEdges(self: depthai.ImgDetection, edges: list[Annotated[list[int], FixedSize(2)]]) -> None |
| `@overload` `def setKeypoints(self, keypoints: KeypointsList) -> None` | `(self, keypoints: KeypointsList)` | L10768 | setKeypoints(*args, **kwargs) |
| `@overload` `def setKeypoints(self, keypoints: list[Keypoint]) -> None` | `(self, keypoints: list[Keypoint])` | L10783 | setKeypoints(*args, **kwargs) |
| `@overload` `def setKeypoints(self, keypoints: list[Keypoint], edges) -> None` | `(self, keypoints: list[Keypoint], edges)` | L10798 | setKeypoints(*args, **kwargs) |
| `@overload` `def setKeypoints(self, keypoints: list[Point3f]) -> None` | `(self, keypoints: list[Point3f])` | L10813 | setKeypoints(*args, **kwargs) |
| `@overload` `def setKeypoints(self, keypoints: VectorPoint2f) -> None` | `(self, keypoints: VectorPoint2f)` | L10828 | setKeypoints(*args, **kwargs) |
| `def setOuterBoundingBox(self, xmin: float, ymin: float, xmax: float, ymax: float) -> None` | `(self, xmin: float, ymin: float, xmax: float, ymax: float)` | L10842 | setOuterBoundingBox(self: depthai.ImgDetection, xmin: float, ymin: float, xmax: float, ymax: float) -> None |

<a id="class-imgdetections"></a>
### class `ImgDetections(Buffer)`  — L10845

> ImgDetections message. Carries normalized detections and optional segmentation
mask. The segmentation mask is stored as a single-channel INT8 2-d array, where
the value represents the instance index in the list of detections. The value 255
is treated as a background pixel (no instance).

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `detections` | `list[ImgDetection]` | — | L10850 |
| `segmentationMaskHeight` | `int` | — | L10851 |
| `segmentationMaskWidth` | `int` | — | L10852 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L10853 | __init__(self: depthai.ImgDetections) -> None |

**🔹 Public Methods (14):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getCvSegmentationMask(self) -> numpy.ndarray | None` | `(self)` | L10855 | getCvSegmentationMask(self: depthai.ImgDetections) -> Optional[numpy.ndarray] |
| `def getCvSegmentationMaskByClass(self, semantic_class: int) -> numpy.ndarray | None` | `(self, semantic_class: int)` | L10865 | getCvSegmentationMaskByClass(self: depthai.ImgDetections, semantic_class: int) -> Optional[numpy.ndarray] |
| `def getCvSegmentationMaskByIndex(self, index: int) -> numpy.ndarray | None` | `(self, index: int)` | L10878 | getCvSegmentationMaskByIndex(self: depthai.ImgDetections, index: int) -> Optional[numpy.ndarray] |
| `def getMaskData(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L10891 | getMaskData(self: depthai.ImgDetections) -> Optional[std::vector<unsigned char,std::allocator<unsigned char> >] |
| `def getSegmentationMask(self) -> ImgFrame | None` | `(self)` | L10893 | getSegmentationMask(self: depthai.ImgDetections) -> Optional[depthai.ImgFrame] |
| `def getSegmentationMaskHeight(self) -> int` | `(self)` | L10895 | getSegmentationMaskHeight(self: depthai.ImgDetections) -> int |
| `def getSegmentationMaskWidth(self) -> int` | `(self)` | L10897 | getSegmentationMaskWidth(self: depthai.ImgDetections) -> int |
| `def getSequenceNum(self) -> int` | `(self)` | L10899 | getSequenceNum(self: depthai.ImgDetections) -> int |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L10904 | getTimestamp(self: depthai.ImgDetections) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L10909 | getTimestampDevice(self: depthai.ImgDetections) -> datetime.timedelta |
| `def getTransformation(self) -> ImgTransformation | None` | `(self)` | L10915 | getTransformation(self: depthai.ImgDetections) -> Optional[depthai.ImgTransformation] |
| `def setCvSegmentationMask(self, mask: numpy.ndarray) -> None` | `(self, mask: numpy.ndarray)` | L10917 | setCvSegmentationMask(self: depthai.ImgDetections, mask: numpy.ndarray) -> None |
| `def setSegmentationMask(self, frame: ImgFrame) -> None` | `(self, frame: ImgFrame)` | L10926 | setSegmentationMask(self: depthai.ImgDetections, frame: depthai.ImgFrame) -> None |
| `def setTransformation(self, arg0: ImgTransformation | None) -> None` | `(self, arg0: ImgTransformation | None)` | L10928 | setTransformation(self: depthai.ImgDetections, arg0: Optional[depthai.ImgTransformation]) -> None |

<a id="class-imgframe"></a>
### class `ImgFrame(Buffer)`  — L10931

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L11072 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: int) -> None` | `(self, arg0: int)` | L11081 | __init__(*args, **kwargs) |

**🔹 Public Methods (38):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getBytesPerPixel(self) -> float` | `(self)` | L11089 | getBytesPerPixel(self: depthai.ImgFrame) -> float |
| `def getCategory(self) -> int` | `(self)` | L11094 | getCategory(self: depthai.ImgFrame) -> int |
| `def getColorTemperature(self) -> int` | `(self)` | L11099 | getColorTemperature(self: depthai.ImgFrame) -> int |
| `def getCvFrame(self) -> numpy.ndarray` | `(self)` | L11104 | getCvFrame(self: depthai.ImgFrame) -> numpy.ndarray |
| `def getExposureTime(self) -> datetime.timedelta` | `(self)` | L11117 | getExposureTime(self: depthai.ImgFrame) -> datetime.timedelta |
| `def getFrame(self) -> numpy.ndarray` | `(self)` | L11122 | getFrame(self: depthai.ImgFrame) -> numpy.ndarray |
| `def getHeight(self) -> int` | `(self)` | L11135 | getHeight(self: depthai.ImgFrame) -> int |
| `def getInstanceNum(self) -> int` | `(self)` | L11140 | getInstanceNum(self: depthai.ImgFrame) -> int |
| `def getLensPosition(self) -> int` | `(self)` | L11145 | getLensPosition(self: depthai.ImgFrame) -> int |
| `def getLensPositionRaw(self) -> float` | `(self)` | L11150 | getLensPositionRaw(self: depthai.ImgFrame) -> float |
| `def getPlaneHeight(self) -> int` | `(self)` | L11155 | getPlaneHeight(self: depthai.ImgFrame) -> int |
| `def getPlaneStride(self, arg0: int) -> int` | `(self, arg0: int)` | L11160 | getPlaneStride(self: depthai.ImgFrame, arg0: int) -> int |
| `def getSensitivity(self) -> int` | `(self)` | L11168 | getSensitivity(self: depthai.ImgFrame) -> int |
| `def getSequenceNum(self) -> int` | `(self)` | L11173 | getSequenceNum(self: depthai.ImgFrame) -> int |
| `def getSourceDFov(self) -> float` | `(self)` | L11178 | getSourceDFov(self: depthai.ImgFrame) -> float |
| `def getSourceHFov(self) -> float` | `(self)` | L11187 | getSourceHFov(self: depthai.ImgFrame) -> float |
| `def getSourceHeight(self) -> int` | `(self)` | L11196 | getSourceHeight(self: depthai.ImgFrame) -> int |
| `def getSourceVFov(self) -> float` | `(self)` | L11201 | getSourceVFov(self: depthai.ImgFrame) -> float |
| `def getSourceWidth(self) -> int` | `(self)` | L11210 | getSourceWidth(self: depthai.ImgFrame) -> int |
| `def getStride(self) -> int` | `(self)` | L11215 | getStride(self: depthai.ImgFrame) -> int |
| `@overload` `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L11221 | getTimestamp(*args, **kwargs) |
| `@overload` `def getTimestamp(self, offset: CameraExposureOffset) -> datetime.timedelta` | `(self, offset: CameraExposureOffset)` | L11235 | getTimestamp(*args, **kwargs) |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L11248 | getTimestampDevice(*args, **kwargs) |
| `def getTransformation(self) -> ImgTransformation` | `(self)` | L11263 | getTransformation(self: depthai.ImgFrame) -> depthai.ImgTransformation |
| `def getType(self) -> ImgFrame.Type` | `(self)` | L11265 | getType(self: depthai.ImgFrame) -> depthai.ImgFrame.Type |
| `def getWidth(self) -> int` | `(self)` | L11270 | getWidth(self: depthai.ImgFrame) -> int |
| `def setCategory(self, category: int) -> ImgFrame` | `(self, category: int)` | L11275 | setCategory(self: depthai.ImgFrame, category: int) -> depthai.ImgFrame |
| `def setCvFrame(self, arg0: numpy.ndarray, arg1: ImgFrame.Type) -> ImgFrame` | `(self, arg0: numpy.ndarray, arg1: ImgFrame.Type)` | L11281 | setCvFrame(self: depthai.ImgFrame, arg0: numpy.ndarray, arg1: depthai.ImgFrame.Type) -> depthai.ImgFrame |
| `def setFrame(self, arg0: numpy.ndarray) -> ImgFrame` | `(self, arg0: numpy.ndarray)` | L11296 | setFrame(self: depthai.ImgFrame, arg0: numpy.ndarray) -> depthai.ImgFrame |
| `def setHeight(self, height: int) -> ImgFrame` | `(self, height: int)` | L11306 | setHeight(self: depthai.ImgFrame, height: int) -> depthai.ImgFrame |
| `def setInstanceNum(self, instance: int) -> ImgFrame` | `(self, instance: int)` | L11314 | setInstanceNum(self: depthai.ImgFrame, instance: int) -> depthai.ImgFrame |
| `@overload` `def setSize(self, width: int, height: int) -> ImgFrame` | `(self, width: int, height: int)` | L11323 | setSize(*args, **kwargs) |
| `@overload` `def setSize(self, sizer: tuple[int, int]) -> ImgFrame` | `(self, sizer: tuple[int, int])` | L11345 | setSize(*args, **kwargs) |
| `def setStride(self, stride: int) -> ImgFrame` | `(self, stride: int)` | L11366 | setStride(self: depthai.ImgFrame, stride: int) -> depthai.ImgFrame |
| `def setTransformation(self, arg0: ImgTransformation) -> None` | `(self, arg0: ImgTransformation)` | L11374 | setTransformation(self: depthai.ImgFrame, arg0: depthai.ImgTransformation) -> None |
| `def setType(self, type: ImgFrame.Type) -> ImgFrame` | `(self, type: ImgFrame.Type)` | L11376 | setType(self: depthai.ImgFrame, type: depthai.ImgFrame.Type) -> depthai.ImgFrame |
| `def setWidth(self, width: int) -> ImgFrame` | `(self, width: int)` | L11384 | setWidth(self: depthai.ImgFrame, width: int) -> depthai.ImgFrame |
| `def validateTransformations(self) -> bool` | `(self)` | L11392 | validateTransformations(self: depthai.ImgFrame) -> bool |

**Nested Class:**

<a id="class-specs"></a>
#### class `Specs`  — L10932

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `bytesPP` | `int` | — | L10933 |
| `height` | `int` | — | L10934 |
| `p1Offset` | `int` | — | L10935 |
| `p2Offset` | `int` | — | L10936 |
| `p3Offset` | `int` | — | L10937 |
| `stride` | `int` | — | L10938 |
| `type` | `ImgFrame.Type` | — | L10939 |
| `width` | `int` | — | L10940 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L10941 | __init__(self: depthai.ImgFrame.Specs) -> None |

**Nested Class:**

<a id="class-type"></a>
#### class `Type`  — L10944

> Members:

YUV422i

YUV444p

YUV420p

YUV422p

YUV400p

RGBA8888

RGB161616

RGB888p

BGR888p

RGB888i

BGR888i

RGBF16F16F16p

BGRF16F16F16p

RGBF16F16F16i

BGRF16F16F16i

GRAY8

GRAYF16

LUT2

LUT4

LUT16

RAW16

RAW14

RAW12

RAW10

RAW8

PACK10

PACK12

YUV444i

NV12

NV21

BITSTREAM

HDR

RAW32

NONE

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L11014 |
| `BGR888i` | `ClassVar[ImgFrame.Type]` | `...` | L11015 |
| `BGR888p` | `ClassVar[ImgFrame.Type]` | `...` | L11016 |
| `BGRF16F16F16i` | `ClassVar[ImgFrame.Type]` | `...` | L11017 |
| `BGRF16F16F16p` | `ClassVar[ImgFrame.Type]` | `...` | L11018 |
| `BITSTREAM` | `ClassVar[ImgFrame.Type]` | `...` | L11019 |
| `GRAY8` | `ClassVar[ImgFrame.Type]` | `...` | L11020 |
| `GRAYF16` | `ClassVar[ImgFrame.Type]` | `...` | L11021 |
| `HDR` | `ClassVar[ImgFrame.Type]` | `...` | L11022 |
| `LUT16` | `ClassVar[ImgFrame.Type]` | `...` | L11023 |
| `LUT2` | `ClassVar[ImgFrame.Type]` | `...` | L11024 |
| `LUT4` | `ClassVar[ImgFrame.Type]` | `...` | L11025 |
| `NONE` | `ClassVar[ImgFrame.Type]` | `...` | L11026 |
| `NV12` | `ClassVar[ImgFrame.Type]` | `...` | L11027 |
| `NV21` | `ClassVar[ImgFrame.Type]` | `...` | L11028 |
| `PACK10` | `ClassVar[ImgFrame.Type]` | `...` | L11029 |
| `PACK12` | `ClassVar[ImgFrame.Type]` | `...` | L11030 |
| `RAW10` | `ClassVar[ImgFrame.Type]` | `...` | L11031 |
| `RAW12` | `ClassVar[ImgFrame.Type]` | `...` | L11032 |
| `RAW14` | `ClassVar[ImgFrame.Type]` | `...` | L11033 |
| `RAW16` | `ClassVar[ImgFrame.Type]` | `...` | L11034 |
| `RAW32` | `ClassVar[ImgFrame.Type]` | `...` | L11035 |
| `RAW8` | `ClassVar[ImgFrame.Type]` | `...` | L11036 |
| `RGB161616` | `ClassVar[ImgFrame.Type]` | `...` | L11037 |
| `RGB888i` | `ClassVar[ImgFrame.Type]` | `...` | L11038 |
| `RGB888p` | `ClassVar[ImgFrame.Type]` | `...` | L11039 |
| `RGBA8888` | `ClassVar[ImgFrame.Type]` | `...` | L11040 |
| `RGBF16F16F16i` | `ClassVar[ImgFrame.Type]` | `...` | L11041 |
| `RGBF16F16F16p` | `ClassVar[ImgFrame.Type]` | `...` | L11042 |
| `YUV400p` | `ClassVar[ImgFrame.Type]` | `...` | L11043 |
| `YUV420p` | `ClassVar[ImgFrame.Type]` | `...` | L11044 |
| `YUV422i` | `ClassVar[ImgFrame.Type]` | `...` | L11045 |
| `YUV422p` | `ClassVar[ImgFrame.Type]` | `...` | L11046 |
| `YUV444i` | `ClassVar[ImgFrame.Type]` | `...` | L11047 |
| `YUV444p` | `ClassVar[ImgFrame.Type]` | `...` | L11048 |
| `__entries` | `ClassVar[dict]` | `...` | L11049 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L11050 | __init__(self: depthai.ImgFrame.Type, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L11052 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L11054 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L11056 | __index__(self: depthai.ImgFrame.Type) -> int |
| `def __int__(self) -> int` | `(self)` | L11058 | __int__(self: depthai.ImgFrame.Type) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L11060 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L11063 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L11069 | (arg0: depthai.ImgFrame.Type) -> int |

<a id="class-imgframecapability"></a>
### class `ImgFrameCapability(Capability)`  — L11401

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `enableUndistortion` | `bool | None` | — | L11402 |
| `fps` | `CapabilityRangeFloat` | — | L11403 |
| `resizeMode` | `ImgResizeMode` | — | L11404 |
| `size` | `CapabilityRangeUintPair` | — | L11405 |
| `type` | `ImgFrame.Type | None` | — | L11406 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L11407 | __init__(self: depthai.ImgFrameCapability) -> None |

<a id="class-imgresizemode"></a>
### class `ImgResizeMode`  — L11410

> Members:

  CROP

  STRETCH

  LETTERBOX

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L11420 |
| `CROP` | `ClassVar[ImgResizeMode]` | `...` | L11421 |
| `LETTERBOX` | `ClassVar[ImgResizeMode]` | `...` | L11422 |
| `STRETCH` | `ClassVar[ImgResizeMode]` | `...` | L11423 |
| `__entries` | `ClassVar[dict]` | `...` | L11424 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L11425 | __init__(self: depthai.ImgResizeMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L11427 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L11429 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L11431 | __index__(self: depthai.ImgResizeMode) -> int |
| `def __int__(self) -> int` | `(self)` | L11433 | __int__(self: depthai.ImgResizeMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L11435 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L11438 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L11444 | (arg0: depthai.ImgResizeMode) -> int |

<a id="class-imgtransformation"></a>
### class `ImgTransformation`  — L11447

> ImgTransformation struct. Holds information of how a ImgFrame or related message
was transformed from their source. Useful for remapping from one ImgFrame to
another.

**🔧 Dunder Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L11452 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, width: int, height: int) -> None` | `(self, width: int, height: int)` | L11467 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, srcWidth: int, srcHeight: int, width: int, height: int) -> None` | `(self, srcWidth: int, srcHeight: int, width: int, height: int)` | L11482 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, width: int, height: int, sourceIntrinsicMatrix) -> None` | `(self, width: int, height: int, sourceIntrinsicMatrix)` | L11497 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, width: int, height: int, sourceIntrinsicMatrix, distortionModel: CameraModel, distortionCoefficients: list[float]) -> None` | `(self, width: int, height: int, sourceIntrinsicMatrix, distortionModel: CameraModel, distortionCoefficients: list[float])` | L11512 | __init__(*args, **kwargs) |

**🔹 Public Methods (35):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def addCrop(self, x: int, y: int, width: int, height: int) -> ImgTransformation` | `(self, x: int, y: int, width: int, height: int)` | L11526 | addCrop(self: depthai.ImgTransformation, x: int, y: int, width: int, height: int) -> depthai.ImgTransformation |
| `def addFlipHorizontal(self) -> ImgTransformation` | `(self)` | L11543 | addFlipHorizontal(self: depthai.ImgTransformation) -> depthai.ImgTransformation |
| `def addFlipVertical(self) -> ImgTransformation` | `(self)` | L11548 | addFlipVertical(self: depthai.ImgTransformation) -> depthai.ImgTransformation |
| `def addPadding(self, x: int, y: int, width: int, height: int) -> ImgTransformation` | `(self, x: int, y: int, width: int, height: int)` | L11553 | addPadding(self: depthai.ImgTransformation, x: int, y: int, width: int, height: int) -> depthai.ImgTransformation |
| `def addRotation(self, angle: float, rotationPoint: Point2f) -> ImgTransformation` | `(self, angle: float, rotationPoint: Point2f)` | L11570 | addRotation(self: depthai.ImgTransformation, angle: float, rotationPoint: depthai.Point2f) -> depthai.ImgTransformation |
| `def addScale(self, scaleX: float, scaleY: float) -> ImgTransformation` | `(self, scaleX: float, scaleY: float)` | L11581 | addScale(self: depthai.ImgTransformation, scaleX: float, scaleY: float) -> depthai.ImgTransformation |
| `def addTransformation(self, matrix) -> ImgTransformation` | `(self, matrix)` | L11592 | addTransformation(self: depthai.ImgTransformation, matrix: Annotated[list[Annotated[list[float], FixedSize(3)]], FixedSize(3)]) -> depthai.ImgTransformation |
| `def getDFov(self, source: bool = ...) -> float` | `(self, source: bool = ...)` | L11600 | getDFov(self: depthai.ImgTransformation, source: bool = False) -> float |
| `def getDistortionCoefficients(self) -> list[float]` | `(self)` | L11602 | getDistortionCoefficients(self: depthai.ImgTransformation) -> list[float] |
| `def getDistortionModel(self) -> CameraModel` | `(self)` | L11610 | getDistortionModel(self: depthai.ImgTransformation) -> depthai.CameraModel |
| `def getDstMaskPt(self, x: int, y: int) -> bool` | `(self, x: int, y: int)` | L11618 | getDstMaskPt(self: depthai.ImgTransformation, x: int, y: int) -> bool |
| `def getHFov(self, source: bool = ...) -> float` | `(self, source: bool = ...)` | L11624 | getHFov(self: depthai.ImgTransformation, source: bool = False) -> float |
| `def getIntrinsicMatrix(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L11626 | getIntrinsicMatrix(self: depthai.ImgTransformation) -> Annotated[list[Annotated[list[float], FixedSize(3)]], FixedSize(3)] |
| `def getIntrinsicMatrixInv(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L11628 | getIntrinsicMatrixInv(self: depthai.ImgTransformation) -> Annotated[list[Annotated[list[float], FixedSize(3)]], FixedSize(3)] |
| `def getMatrix(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L11630 | getMatrix(self: depthai.ImgTransformation) -> Annotated[list[Annotated[list[float], FixedSize(3)]], FixedSize(3)] |
| `def getMatrixInv(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L11632 | getMatrixInv(self: depthai.ImgTransformation) -> Annotated[list[Annotated[list[float], FixedSize(3)]], FixedSize(3)] |
| `def getSize(self) -> tuple[int, int]` | `(self)` | L11634 | getSize(self: depthai.ImgTransformation) -> tuple[int, int] |
| `def getSourceIntrinsicMatrix(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L11643 | getSourceIntrinsicMatrix(self: depthai.ImgTransformation) -> Annotated[list[Annotated[list[float], FixedSize(3)]], FixedSize(3)] |
| `def getSourceIntrinsicMatrixInv(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L11645 | getSourceIntrinsicMatrixInv(self: depthai.ImgTransformation) -> Annotated[list[Annotated[list[float], FixedSize(3)]], FixedSize(3)] |
| `def getSourceSize(self) -> tuple[int, int]` | `(self)` | L11647 | getSourceSize(self: depthai.ImgTransformation) -> tuple[int, int] |
| `def getSrcCrops(self) -> list[RotatedRect]` | `(self)` | L11655 | getSrcCrops(self: depthai.ImgTransformation) -> list[depthai.RotatedRect] |
| `def getSrcMaskPt(self, x: int, y: int) -> bool` | `(self, x: int, y: int)` | L11657 | getSrcMaskPt(self: depthai.ImgTransformation, x: int, y: int) -> bool |
| `def getVFov(self, source: bool = ...) -> float` | `(self, source: bool = ...)` | L11663 | getVFov(self: depthai.ImgTransformation, source: bool = False) -> float |
| `def invTransformPoint(self, point: Point2f) -> Point2f` | `(self, point: Point2f)` | L11665 | invTransformPoint(self: depthai.ImgTransformation, point: depthai.Point2f) -> depthai.Point2f |
| `def invTransformRect(self, rect: RotatedRect) -> RotatedRect` | `(self, rect: RotatedRect)` | L11676 | invTransformRect(self: depthai.ImgTransformation, rect: depthai.RotatedRect) -> depthai.RotatedRect |
| `def isValid(self) -> bool` | `(self)` | L11687 | isValid(self: depthai.ImgTransformation) -> bool |
| `def remapPointFrom(self, to: ImgTransformation, point: Point2f) -> Point2f` | `(self, to: ImgTransformation, point: Point2f)` | L11693 | remapPointFrom(self: depthai.ImgTransformation, to: depthai.ImgTransformation, point: depthai.Point2f) -> depthai.Point2f |
| `def remapPointTo(self, to: ImgTransformation, point: Point2f) -> Point2f` | `(self, to: ImgTransformation, point: Point2f)` | L11706 | remapPointTo(self: depthai.ImgTransformation, to: depthai.ImgTransformation, point: depthai.Point2f) -> depthai.Point2f |
| `def remapRectFrom(self, to: ImgTransformation, rect: RotatedRect) -> RotatedRect` | `(self, to: ImgTransformation, rect: RotatedRect)` | L11719 | remapRectFrom(self: depthai.ImgTransformation, to: depthai.ImgTransformation, rect: depthai.RotatedRect) -> depthai.RotatedRect |
| `def remapRectTo(self, to: ImgTransformation, rect: RotatedRect) -> RotatedRect` | `(self, to: ImgTransformation, rect: RotatedRect)` | L11732 | remapRectTo(self: depthai.ImgTransformation, to: depthai.ImgTransformation, rect: depthai.RotatedRect) -> depthai.RotatedRect |
| `def setDistortionCoefficients(self, coefficients: list[float]) -> ImgTransformation` | `(self, coefficients: list[float])` | L11745 | setDistortionCoefficients(self: depthai.ImgTransformation, coefficients: list[float]) -> depthai.ImgTransformation |
| `def setDistortionModel(self, model: CameraModel) -> ImgTransformation` | `(self, model: CameraModel)` | L11747 | setDistortionModel(self: depthai.ImgTransformation, model: depthai.CameraModel) -> depthai.ImgTransformation |
| `def setIntrinsicMatrix(self, intrinsicMatrix) -> ImgTransformation` | `(self, intrinsicMatrix)` | L11749 | setIntrinsicMatrix(self: depthai.ImgTransformation, intrinsicMatrix: Annotated[list[Annotated[list[float], FixedSize(3)]], FixedSize(3)]) -> depthai.ImgTransformation |
| `def transformPoint(self, point: Point2f) -> Point2f` | `(self, point: Point2f)` | L11751 | transformPoint(self: depthai.ImgTransformation, point: depthai.Point2f) -> depthai.Point2f |
| `def transformRect(self, rect: RotatedRect) -> RotatedRect` | `(self, rect: RotatedRect)` | L11762 | transformRect(self: depthai.ImgTransformation, rect: depthai.RotatedRect) -> depthai.RotatedRect |

<a id="class-inputqueue"></a>
### class `InputQueue`  — L11774

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L11775 | Initialize self.  See help(type(self)) for accurate signature. |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def send(self, msg: ADatatype) -> None` | `(self, msg: ADatatype)` | L11777 | send(self: depthai.InputQueue, msg: depthai.ADatatype) -> None |

<a id="class-interpolation"></a>
### class `Interpolation`  — L11786

> Interpolation type

Members:

  BILINEAR

  BICUBIC

  NEAREST_NEIGHBOR

  BYPASS

  DEFAULT

  DEFAULT_DISPARITY_DEPTH

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L11802 |
| `BICUBIC` | `ClassVar[Interpolation]` | `...` | L11803 |
| `BILINEAR` | `ClassVar[Interpolation]` | `...` | L11804 |
| `BYPASS` | `ClassVar[Interpolation]` | `...` | L11805 |
| `DEFAULT` | `ClassVar[Interpolation]` | `...` | L11806 |
| `DEFAULT_DISPARITY_DEPTH` | `ClassVar[Interpolation]` | `...` | L11807 |
| `NEAREST_NEIGHBOR` | `ClassVar[Interpolation]` | `...` | L11808 |
| `__entries` | `ClassVar[dict]` | `...` | L11809 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L11810 | __init__(self: depthai.Interpolation, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L11812 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L11814 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L11816 | __index__(self: depthai.Interpolation) -> int |
| `def __int__(self) -> int` | `(self)` | L11818 | __int__(self: depthai.Interpolation) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L11820 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L11823 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L11829 | (arg0: depthai.Interpolation) -> int |

<a id="class-keypoint"></a>
### class `Keypoint`  — L11832

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `confidence` | `float` | — | L11833 |
| `imageCoordinates` | `Point3f` | — | L11834 |
| `label` | `int` | — | L11835 |
| `labelName` | `str` | — | L11836 |

**🔧 Dunder Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L11838 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, coordinates: Point3f, confidence: float = ..., label: int = ..., labelName: str = ...) -> None` | `(self, coordinates: Point3f, confidence: float = ..., label: int = ..., labelName: str = ...)` | L11851 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, coordinates: Point2f, confidence: float = ..., label: int = ..., labelName: str = ...) -> None` | `(self, coordinates: Point2f, confidence: float = ..., label: int = ..., labelName: str = ...)` | L11864 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, x: float, y: float, z: float, confidence: float = ..., label: int = ..., labelName: str = ...) -> None` | `(self, x: float, y: float, z: float, confidence: float = ..., label: int = ..., labelName: str = ...)` | L11877 | __init__(*args, **kwargs) |

<a id="class-keypointslist"></a>
### class `KeypointsList`  — L11890

**🔧 Dunder Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L11892 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, keypoints: list[Keypoint], edges) -> None` | `(self, keypoints: list[Keypoint], edges)` | L11903 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, keypoints: list[Keypoint]) -> None` | `(self, keypoints: list[Keypoint])` | L11914 | __init__(*args, **kwargs) |

**🔹 Public Methods (9):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getEdges(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L11924 | getEdges(self: depthai.KeypointsList) -> list[Annotated[list[int], FixedSize(2)]] |
| `def getKeypoints(self) -> list[Keypoint]` | `(self)` | L11932 | getKeypoints(self: depthai.KeypointsList) -> list[depthai.Keypoint] |
| `def getPoints2f(self) -> VectorPoint2f` | `(self)` | L11940 | getPoints2f(self: depthai.KeypointsList) -> depthai.VectorPoint2f |
| `def getPoints3f(self) -> list[Point3f]` | `(self)` | L11948 | getPoints3f(self: depthai.KeypointsList) -> list[depthai.Point3f] |
| `def setEdges(self, edges) -> None` | `(self, edges)` | L11956 | setEdges(self: depthai.KeypointsList, edges: list[Annotated[list[int], FixedSize(2)]]) -> None |
| `@overload` `def setKeypoints(self, keypoints: list[Keypoint]) -> None` | `(self, keypoints: list[Keypoint])` | L11959 | setKeypoints(*args, **kwargs) |
| `@overload` `def setKeypoints(self, keypoints: list[Point3f]) -> None` | `(self, keypoints: list[Point3f])` | L11996 | setKeypoints(*args, **kwargs) |
| `@overload` `def setKeypoints(self, keypoints: VectorPoint2f) -> None` | `(self, keypoints: VectorPoint2f)` | L12033 | setKeypoints(*args, **kwargs) |
| `@overload` `def setKeypoints(self, keypoints: list[Keypoint], edges) -> None` | `(self, keypoints: list[Keypoint], edges)` | L12070 | setKeypoints(*args, **kwargs) |

<a id="class-loglevel"></a>
### class `LogLevel`  — L12107

> Members:

TRACE

DEBUG

INFO

WARN

ERR

CRITICAL

OFF

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L12123 |
| `CRITICAL` | `ClassVar[LogLevel]` | `...` | L12124 |
| `DEBUG` | `ClassVar[LogLevel]` | `...` | L12125 |
| `ERR` | `ClassVar[LogLevel]` | `...` | L12126 |
| `INFO` | `ClassVar[LogLevel]` | `...` | L12127 |
| `OFF` | `ClassVar[LogLevel]` | `...` | L12128 |
| `TRACE` | `ClassVar[LogLevel]` | `...` | L12129 |
| `WARN` | `ClassVar[LogLevel]` | `...` | L12130 |
| `__entries` | `ClassVar[dict]` | `...` | L12131 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L12132 | __init__(self: depthai.LogLevel, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L12134 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L12136 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L12138 | __index__(self: depthai.LogLevel) -> int |
| `def __int__(self) -> int` | `(self)` | L12140 | __int__(self: depthai.LogLevel) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L12142 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L12145 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L12151 | (arg0: depthai.LogLevel) -> int |

<a id="class-logmessage"></a>
### class `LogMessage`  — L12154

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `colorRangeEnd` | `int` | — | L12155 |
| `colorRangeStart` | `int` | — | L12156 |
| `level` | `LogLevel` | — | L12157 |
| `nodeIdName` | `str` | — | L12158 |
| `payload` | `str` | — | L12159 |
| `time` | `Timestamp` | — | L12160 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L12161 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-memoryinfo"></a>
### class `MemoryInfo`  — L12164

> MemoryInfo structure

Free, remaining and total memory stats

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `remaining` | `int` | — | L12168 |
| `total` | `int` | — | L12169 |
| `used` | `int` | — | L12170 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L12171 | __init__(self: depthai.MemoryInfo) -> None |

<a id="class-messagedemuxproperties"></a>
### class `MessageDemuxProperties`  — L12174

> MessageDemux does not have any properties to set

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L12176 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-messagegroup"></a>
### class `MessageGroup(Buffer)`  — L12179

> MessageGroup message. Carries multiple messages in one.

**🔧 Dunder Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L12181 | __init__(self: depthai.MessageGroup) -> None |
| `def __getitem__(self, arg0: str) -> ADatatype` | `(self, arg0: str)` | L12219 | __getitem__(self: depthai.MessageGroup, arg0: str) -> depthai.ADatatype |
| `def __iter__(self) -> Iterator[tuple[str, ADatatype]]` | `(self)` | L12221 | __iter__(self: depthai.MessageGroup) -> Iterator[tuple[str, depthai.ADatatype]] |
| `def __setitem__(self, arg0: str, arg1: ADatatype) -> None` | `(self, arg0: str, arg1: ADatatype)` | L12223 | __setitem__(self: depthai.MessageGroup, arg0: str, arg1: depthai.ADatatype) -> None |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getIntervalNs(self) -> int` | `(self)` | L12183 | getIntervalNs(self: depthai.MessageGroup) -> int |
| `def getMessageNames(self) -> list[str]` | `(self)` | L12188 | getMessageNames(self: depthai.MessageGroup) -> list[str] |
| `def getNumMessages(self) -> int` | `(self)` | L12193 | getNumMessages(self: depthai.MessageGroup) -> int |
| `def getSequenceNum(self) -> int` | `(self)` | L12195 | getSequenceNum(self: depthai.MessageGroup) -> int |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L12200 | getTimestamp(self: depthai.MessageGroup) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L12205 | getTimestampDevice(self: depthai.MessageGroup) -> datetime.timedelta |
| `def isSynced(self, arg0: int) -> bool` | `(self, arg0: int)` | L12211 | isSynced(self: depthai.MessageGroup, arg0: int) -> bool |

<a id="class-messagequeue"></a>
### class `MessageQueue`  — L12226

> Thread safe queue to send messages between nodes

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `QueueException` | `ClassVar[type[MessageQueue.QueueException]]` | `...` | L12228 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self, name: str) -> None` | `(self, name: str)` | L12230 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, name: str = ..., maxSize: int = ..., blocking: bool = ...) -> None` | `(self, name: str = ..., maxSize: int = ..., blocking: bool = ...)` | L12239 | __init__(*args, **kwargs) |

**🔹 Public Methods (23):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def addCallback(self, callback: Callable) -> int` | `(self, callback: Callable)` | L12247 | addCallback(self: depthai.MessageQueue, callback: Callable) -> int |
| `def close(self) -> None` | `(self)` | L12258 | close(self: depthai.MessageQueue) -> None |
| `def front(self) -> ADatatype` | `(self)` | L12263 | front(self: depthai.MessageQueue) -> depthai.ADatatype |
| `@overload` `def get(self) -> ADatatype` | `(self)` | L12272 | get(*args, **kwargs) |
| `@overload` `def get(self, timeout: datetime.timedelta) -> ADatatype` | `(self, timeout: datetime.timedelta)` | L12291 | get(*args, **kwargs) |
| `def getAll(self) -> list[ADatatype]` | `(self)` | L12309 | getAll(self: depthai.MessageQueue) -> list[depthai.ADatatype] |
| `def getBlocking(self) -> bool` | `(self)` | L12318 | getBlocking(self: depthai.MessageQueue) -> bool |
| `def getMaxSize(self) -> int` | `(self)` | L12326 | getMaxSize(self: depthai.MessageQueue) -> int |
| `@overload` `def getName(self) -> str` | `(self)` | L12335 | getName(*args, **kwargs) |
| `@overload` `def getName(self) -> str` | `(self)` | L12348 | getName(*args, **kwargs) |
| `def getSize(self) -> int` | `(self)` | L12360 | getSize(self: depthai.MessageQueue) -> int |
| `def has(self) -> bool` | `(self)` | L12368 | has(self: depthai.MessageQueue) -> bool |
| `def isClosed(self) -> bool` | `(self)` | L12377 | isClosed(self: depthai.MessageQueue) -> bool |
| `def isFull(self) -> int` | `(self)` | L12382 | isFull(self: depthai.MessageQueue) -> int |
| `def removeCallback(self, callbackId: int) -> bool` | `(self, callbackId: int)` | L12390 | removeCallback(self: depthai.MessageQueue, callbackId: int) -> bool |
| `@overload` `def send(self, msg: ADatatype) -> None` | `(self, msg: ADatatype)` | L12402 | send(*args, **kwargs) |
| `@overload` `def send(self, msg: ADatatype, timeout: datetime.timedelta) -> bool` | `(self, msg: ADatatype, timeout: datetime.timedelta)` | L12423 | send(*args, **kwargs) |
| `def setBlocking(self, blocking: bool) -> None` | `(self, blocking: bool)` | L12443 | setBlocking(self: depthai.MessageQueue, blocking: bool) -> None |
| `def setMaxSize(self, maxSize: int) -> None` | `(self, maxSize: int)` | L12451 | setMaxSize(self: depthai.MessageQueue, maxSize: int) -> None |
| `def setName(self, name: str) -> None` | `(self, name: str)` | L12461 | setName(self: depthai.MessageQueue, name: str) -> None |
| `def tryGet(self) -> ADatatype` | `(self)` | L12466 | tryGet(self: depthai.MessageQueue) -> depthai.ADatatype |
| `def tryGetAll(self) -> list[ADatatype]` | `(self)` | L12475 | tryGetAll(self: depthai.MessageQueue) -> list[depthai.ADatatype] |
| `def trySend(self, msg: ADatatype) -> bool` | `(self, msg: ADatatype)` | L12483 | trySend(self: depthai.MessageQueue, msg: depthai.ADatatype) -> bool |

<a id="class-modeltype"></a>
### class `ModelType`  — L12492

> Neural network model type

Members:

  BLOB

  SUPERBLOB

  DLC

  NNARCHIVE

  OTHER

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L12506 |
| `BLOB` | `ClassVar[ModelType]` | `...` | L12507 |
| `DLC` | `ClassVar[ModelType]` | `...` | L12508 |
| `NNARCHIVE` | `ClassVar[ModelType]` | `...` | L12509 |
| `OTHER` | `ClassVar[ModelType]` | `...` | L12510 |
| `SUPERBLOB` | `ClassVar[ModelType]` | `...` | L12511 |
| `__entries` | `ClassVar[dict]` | `...` | L12512 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L12513 | __init__(self: depthai.ModelType, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L12515 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L12517 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L12519 | __index__(self: depthai.ModelType) -> int |
| `def __int__(self) -> int` | `(self)` | L12521 | __int__(self: depthai.ModelType) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L12523 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L12526 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L12532 | (arg0: depthai.ModelType) -> int |

<a id="class-monocameraproperties"></a>
### class `MonoCameraProperties`  — L12535

> Specify properties for MonoCamera such as camera ID, ...

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `boardSocket` | `CameraBoardSocket` | — | L12587 |
| `eventFilter` | `list[FrameEvent]` | — | L12588 |
| `fps` | `float` | — | L12589 |
| `initialControl` | `CameraControl` | — | L12590 |
| `isp3aFps` | `int` | — | L12591 |
| `numFramesPool` | `int` | — | L12592 |
| `numFramesPoolRaw` | `int` | — | L12593 |
| `resolution` | `MonoCameraProperties.SensorResolution` | — | L12594 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L12595 | Initialize self.  See help(type(self)) for accurate signature. |

**Nested Class:**

<a id="class-sensorresolution"></a>
#### class `SensorResolution`  — L12538

> Select the camera sensor resolution: 1280×720, 1280×800, 640×400, 640×480,
1920×1200, ...

Members:

  THE_720_P

  THE_800_P

  THE_400_P

  THE_480_P

  THE_1200_P

  THE_4000X3000

  THE_4224X3136

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L12557 |
| `THE_1200_P` | `ClassVar[MonoCameraProperties.SensorResolution]` | `...` | L12558 |
| `THE_4000X3000` | `ClassVar[MonoCameraProperties.SensorResolution]` | `...` | L12559 |
| `THE_400_P` | `ClassVar[MonoCameraProperties.SensorResolution]` | `...` | L12560 |
| `THE_4224X3136` | `ClassVar[MonoCameraProperties.SensorResolution]` | `...` | L12561 |
| `THE_480_P` | `ClassVar[MonoCameraProperties.SensorResolution]` | `...` | L12562 |
| `THE_720_P` | `ClassVar[MonoCameraProperties.SensorResolution]` | `...` | L12563 |
| `THE_800_P` | `ClassVar[MonoCameraProperties.SensorResolution]` | `...` | L12564 |
| `__entries` | `ClassVar[dict]` | `...` | L12565 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L12566 | __init__(self: depthai.MonoCameraProperties.SensorResolution, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L12568 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L12570 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L12572 | __index__(self: depthai.MonoCameraProperties.SensorResolution) -> int |
| `def __int__(self) -> int` | `(self)` | L12574 | __int__(self: depthai.MonoCameraProperties.SensorResolution) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L12576 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L12579 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L12585 | (arg0: depthai.MonoCameraProperties.SensorResolution) -> int |

<a id="class-nnarchive"></a>
### class `NNArchive`  — L12598

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self, archivePath: os.PathLike, compression: NNArchiveEntry.Compression = ...) -> None` | `(self, archivePath: os.PathLike, compression: NNArchiveEntry.Compression = ...)` | L12600 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, archivePath: os.PathLike, options: NNArchiveOptions = ...) -> None` | `(self, archivePath: os.PathLike, options: NNArchiveOptions = ...)` | L12629 | __init__(*args, **kwargs) |

**🔹 Public Methods (10):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getBlob(self) -> OpenVINO.Blob | None` | `(self)` | L12657 | getBlob(self: depthai.NNArchive) -> Optional[depthai.OpenVINO.Blob] |
| `def getConfig(self) -> nn_archive.v1.Config` | `(self)` | L12666 | getConfig(self: depthai.NNArchive) -> Union[depthai.nn_archive.v1.Config] |
| `def getConfigV1(self) -> nn_archive.v1.Config` | `(self)` | L12677 | getConfigV1(self: depthai.NNArchive) -> depthai.nn_archive.v1.Config |
| `def getInputHeight(self, index: int = ...) -> int | None` | `(self, index: int = ...)` | L12688 | getInputHeight(self: depthai.NNArchive, index: int = 0) -> Optional[int] |
| `def getInputSize(self, index: int = ...) -> tuple[int, int] | None` | `(self, index: int = ...)` | L12699 | getInputSize(self: depthai.NNArchive, index: int = 0) -> Optional[tuple[int, int]] |
| `def getInputWidth(self, index: int = ...) -> int | None` | `(self, index: int = ...)` | L12711 | getInputWidth(self: depthai.NNArchive, index: int = 0) -> Optional[int] |
| `def getModelType(self) -> ModelType` | `(self)` | L12722 | getModelType(self: depthai.NNArchive) -> depthai.ModelType |
| `def getOtherModelFormat(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L12730 | getOtherModelFormat(self: depthai.NNArchive) -> Optional[std::vector<unsigned char,std::allocator<unsigned char> >] |
| `def getSuperBlob(self) -> OpenVINO.SuperBlob | None` | `(self)` | L12739 | getSuperBlob(self: depthai.NNArchive) -> Optional[depthai.OpenVINO.SuperBlob] |
| `def getSupportedPlatforms(self) -> list[Platform]` | `(self)` | L12748 | getSupportedPlatforms(self: depthai.NNArchive) -> list[depthai.Platform] |

<a id="class-nnarchiveconfigversion"></a>
### class `NNArchiveConfigVersion`  — L12757

> Members:

  V1

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L12763 |
| `V1` | `ClassVar[NNArchiveConfigVersion]` | `...` | L12764 |
| `__entries` | `ClassVar[dict]` | `...` | L12765 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L12766 | __init__(self: depthai.NNArchiveConfigVersion, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L12768 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L12770 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L12772 | __index__(self: depthai.NNArchiveConfigVersion) -> int |
| `def __int__(self) -> int` | `(self)` | L12774 | __int__(self: depthai.NNArchiveConfigVersion) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L12776 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L12779 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L12785 | (arg0: depthai.NNArchiveConfigVersion) -> int |

<a id="class-nnarchiveentry"></a>
### class `NNArchiveEntry`  — L12788

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L12864 | Initialize self.  See help(type(self)) for accurate signature. |

**Nested Class:**

<a id="class-compression"></a>
#### class `Compression`  — L12789

> Members:

AUTO

RAW_FS

TAR

TAR_GZ

TAR_XZ

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L12801 |
| `AUTO` | `ClassVar[NNArchiveEntry.Compression]` | `...` | L12802 |
| `RAW_FS` | `ClassVar[NNArchiveEntry.Compression]` | `...` | L12803 |
| `TAR` | `ClassVar[NNArchiveEntry.Compression]` | `...` | L12804 |
| `TAR_GZ` | `ClassVar[NNArchiveEntry.Compression]` | `...` | L12805 |
| `TAR_XZ` | `ClassVar[NNArchiveEntry.Compression]` | `...` | L12806 |
| `__entries` | `ClassVar[dict]` | `...` | L12807 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L12808 | __init__(self: depthai.NNArchiveEntry.Compression, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L12810 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L12812 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L12814 | __index__(self: depthai.NNArchiveEntry.Compression) -> int |
| `def __int__(self) -> int` | `(self)` | L12816 | __int__(self: depthai.NNArchiveEntry.Compression) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L12818 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L12821 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L12827 | (arg0: depthai.NNArchiveEntry.Compression) -> int |

**Nested Class:**

<a id="class-seek"></a>
#### class `Seek`  — L12830

> Members:

SET

CUR

END

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L12838 |
| `CUR` | `ClassVar[NNArchiveEntry.Seek]` | `...` | L12839 |
| `END` | `ClassVar[NNArchiveEntry.Seek]` | `...` | L12840 |
| `SET` | `ClassVar[NNArchiveEntry.Seek]` | `...` | L12841 |
| `__entries` | `ClassVar[dict]` | `...` | L12842 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L12843 | __init__(self: depthai.NNArchiveEntry.Seek, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L12845 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L12847 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L12849 | __index__(self: depthai.NNArchiveEntry.Seek) -> int |
| `def __int__(self) -> int` | `(self)` | L12851 | __int__(self: depthai.NNArchiveEntry.Seek) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L12853 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L12856 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L12862 | (arg0: depthai.NNArchiveEntry.Seek) -> int |

<a id="class-nnarchiveoptions"></a>
### class `NNArchiveOptions`  — L12867

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `compression` | `NNArchiveEntry.Compression` | — | L12868 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L12869 | __init__(self: depthai.NNArchiveOptions) -> None |

<a id="class-nnarchiveversionedconfig"></a>
### class `NNArchiveVersionedConfig`  — L12872

**🔧 Dunder Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self, path: os.PathLike, compression: NNArchiveEntry.Compression = ...) -> None` | `(self, path: os.PathLike, compression: NNArchiveEntry.Compression = ...)` | L12874 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, data, std, compression: NNArchiveEntry.Compression = ...) -> None` | `(self, data, std, compression: NNArchiveEntry.Compression = ...)` | L12893 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: Callable[[], int], arg1, arg2: Callable[[int, NNArchiveEntry.Seek], int], arg3: Callable[[int], int], arg4: Callable[[], int], arg5: NNArchiveEntry.Compression) -> None` | `(self, arg0: Callable[[], int], arg1, arg2: Callable[[int, NNArchiveEntry.Seek], int], arg3: Callable[[int], int], arg4: Callable[[], int], arg5: NNArchiveEntry.Compression)` | L12912 | __init__(*args, **kwargs) |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getConfig(self) -> nn_archive.v1.Config` | `(self)` | L12930 | getConfig(self: depthai.NNArchiveVersionedConfig) -> Union[depthai.nn_archive.v1.Config] |
| `def getConfigV1(self) -> nn_archive.v1.Config` | `(self)` | L12938 | getConfigV1(self: depthai.NNArchiveVersionedConfig) -> depthai.nn_archive.v1.Config |
| `def getVersion(self) -> NNArchiveConfigVersion` | `(self)` | L12946 | getVersion(self: depthai.NNArchiveVersionedConfig) -> depthai.NNArchiveConfigVersion |

<a id="class-nndata"></a>
### class `NNData(Buffer)`  — L12952

> NNData message. Carries tensors and their metadata

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L12955 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: int) -> None` | `(self, arg0: int)` | L12966 | __init__(*args, **kwargs) |

**🔹 Public Methods (23):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def addTensor(self, name: str, tensor: list[int], storageOrder: TensorInfo.StorageOrder) -> NNData` | `(self, name: str, tensor: list[int], storageOrder: TensorInfo.StorageOrder)` | L12977 | addTensor(*args, **kwargs) |
| `@overload` `def addTensor(self, name: str, tensor: list[float], storageOrder: TensorInfo.StorageOrder) -> NNData` | `(self, name: str, tensor: list[float], storageOrder: TensorInfo.StorageOrder)` | L13046 | addTensor(*args, **kwargs) |
| `@overload` `def addTensor(self, name: str, tensor: list[float], storageOrder: TensorInfo.StorageOrder) -> NNData` | `(self, name: str, tensor: list[float], storageOrder: TensorInfo.StorageOrder)` | L13115 | addTensor(*args, **kwargs) |
| `@overload` `def addTensor(self, name: str, tensor: numpy.ndarray[numpy.int32], storageOrder: TensorInfo.StorageOrder) -> NNData` | `(self, name: str, tensor: numpy.ndarray[numpy.int32], storageOrder: TensorInfo.StorageOrder)` | L13184 | addTensor(*args, **kwargs) |
| `@overload` `def addTensor(self, name: str, tensor: numpy.ndarray[numpy.float32], storageOrder: TensorInfo.StorageOrder) -> NNData` | `(self, name: str, tensor: numpy.ndarray[numpy.float32], storageOrder: TensorInfo.StorageOrder)` | L13253 | addTensor(*args, **kwargs) |
| `@overload` `def addTensor(self, name: str, tensor: numpy.ndarray[numpy.float64], storageOrder: TensorInfo.StorageOrder) -> NNData` | `(self, name: str, tensor: numpy.ndarray[numpy.float64], storageOrder: TensorInfo.StorageOrder)` | L13322 | addTensor(*args, **kwargs) |
| `@overload` `def addTensor(self, name: str, tensor: object, dataType: TensorInfo.DataType) -> None` | `(self, name: str, tensor: object, dataType: TensorInfo.DataType)` | L13391 | addTensor(*args, **kwargs) |
| `@overload` `def addTensor(self, name: str, tensor: object) -> None` | `(self, name: str, tensor: object)` | L13460 | addTensor(*args, **kwargs) |
| `def getAllLayerNames(self) -> list[str]` | `(self)` | L13528 | getAllLayerNames(self: depthai.NNData) -> list[str] |
| `def getAllLayers(self) -> list[TensorInfo]` | `(self)` | L13534 | getAllLayers(self: depthai.NNData) -> list[depthai.TensorInfo] |
| `@overload` `def getFirstTensor(self, dequantize: bool = ...) -> object` | `(self, dequantize: bool = ...)` | L13541 | getFirstTensor(*args, **kwargs) |
| `@overload` `def getFirstTensor(self, storageOrder: TensorInfo.StorageOrder, dequantize: bool = ...) -> object` | `(self, storageOrder: TensorInfo.StorageOrder, dequantize: bool = ...)` | L13560 | getFirstTensor(*args, **kwargs) |
| `def getLayerDatatype(self, name: str, datatype: TensorInfo.DataType) -> bool` | `(self, name: str, datatype: TensorInfo.DataType)` | L13578 | getLayerDatatype(self: depthai.NNData, name: str, datatype: depthai.TensorInfo.DataType) -> bool |
| `def getSequenceNum(self) -> int` | `(self)` | L13592 | getSequenceNum(self: depthai.NNData) -> int |
| `@overload` `def getTensor(self, name: str, dequantize: bool = ...) -> object` | `(self, name: str, dequantize: bool = ...)` | L13598 | getTensor(*args, **kwargs) |
| `@overload` `def getTensor(self, name: str, storageOrder: TensorInfo.StorageOrder, dequantize: bool = ...) -> object` | `(self, name: str, storageOrder: TensorInfo.StorageOrder, dequantize: bool = ...)` | L13617 | getTensor(*args, **kwargs) |
| `def getTensorDatatype(self, name: str) -> TensorInfo.DataType` | `(self, name: str)` | L13635 | getTensorDatatype(self: depthai.NNData, name: str) -> depthai.TensorInfo.DataType |
| `def getTensorInfo(self, name: str) -> TensorInfo | None` | `(self, name: str)` | L13643 | getTensorInfo(self: depthai.NNData, name: str) -> Optional[depthai.TensorInfo] |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L13654 | getTimestamp(self: depthai.NNData) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L13659 | getTimestampDevice(self: depthai.NNData) -> datetime.timedelta |
| `def getTransformation(self) -> ImgTransformation | None` | `(self)` | L13665 | getTransformation(self: depthai.NNData) -> Optional[depthai.ImgTransformation] |
| `def hasLayer(self, name: str) -> bool` | `(self, name: str)` | L13667 | hasLayer(self: depthai.NNData, name: str) -> bool |
| `def setTransformation(self, arg0: ImgTransformation | None) -> None` | `(self, arg0: ImgTransformation | None)` | L13678 | setTransformation(self: depthai.NNData, arg0: Optional[depthai.ImgTransformation]) -> None |

<a id="class-nnmodeldescription"></a>
### class `NNModelDescription`  — L13681

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `compressionLevel` | `str` | — | L13682 |
| `model` | `str` | — | L13683 |
| `modelPrecisionType` | `str` | — | L13684 |
| `optimizationLevel` | `str` | — | L13685 |
| `platform` | `str` | — | L13686 |
| `snpeVersion` | `str` | — | L13687 |

**🔧 Dunder Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L13689 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, model: str, platform: str = ..., optimizationLevel: str = ..., compressionLevel: str = ..., snpeVersion: str = ..., modelPrecisionType: str = ...) -> None` | `(self, model: str, platform: str = ..., optimizationLevel: str = ..., compressionLevel: str = ..., snpeVersion: str = ..., modelPrecisionType: str = ...)` | L13700 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, model: str) -> None` | `(self, model: str)` | L13711 | __init__(*args, **kwargs) |

**⚡ Static Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@staticmethod` `def fromYamlFile(yamlPath: os.PathLike, modelsPath: os.PathLike = ...) -> NNModelDescription` | `(yamlPath: os.PathLike, modelsPath: os.PathLike = ...)` | L13730 | fromYamlFile(yamlPath: os.PathLike, modelsPath: os.PathLike = '') -> depthai.NNModelDescription |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def check(self) -> bool` | `(self)` | L13721 | check(self: depthai.NNModelDescription) -> bool |
| `def saveToYamlFile(self, yamlPath: os.PathLike) -> None` | `(self, yamlPath: os.PathLike)` | L13752 | saveToYamlFile(self: depthai.NNModelDescription, yamlPath: os.PathLike) -> None |
| `def toString(self) -> str` | `(self)` | L13760 | toString(self: depthai.NNModelDescription) -> str |

<a id="class-neuraldepthconfig"></a>
### class `NeuralDepthConfig(Buffer)`  — L13770

> NeuralDepthConfig message.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `postProcessing` | `NeuralDepthConfig.PostProcessing` | — | L13779 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L13780 | __init__(self: depthai.NeuralDepthConfig) -> None |

**🔹 Public Methods (8):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getConfidenceThreshold(self) -> int` | `(self)` | L13782 | getConfidenceThreshold(self: depthai.NeuralDepthConfig) -> int |
| `def getCustomDepthUnitMultiplier(self) -> float` | `(self)` | L13787 | getCustomDepthUnitMultiplier(self: depthai.NeuralDepthConfig) -> float |
| `def getDepthUnit(self) -> DepthUnit` | `(self)` | L13792 | getDepthUnit(self: depthai.NeuralDepthConfig) -> depthai.DepthUnit |
| `def getEdgeThreshold(self) -> int` | `(self)` | L13797 | getEdgeThreshold(self: depthai.NeuralDepthConfig) -> int |
| `def setConfidenceThreshold(self, arg0: int) -> NeuralDepthConfig` | `(self, arg0: int)` | L13802 | setConfidenceThreshold(self: depthai.NeuralDepthConfig, arg0: int) -> depthai.NeuralDepthConfig |
| `def setCustomDepthUnitMultiplier(self, arg0: float) -> NeuralDepthConfig` | `(self, arg0: float)` | L13810 | setCustomDepthUnitMultiplier(self: depthai.NeuralDepthConfig, arg0: float) -> depthai.NeuralDepthConfig |
| `def setDepthUnit(self, arg0: DepthUnit) -> NeuralDepthConfig` | `(self, arg0: DepthUnit)` | L13815 | setDepthUnit(self: depthai.NeuralDepthConfig, arg0: depthai.DepthUnit) -> depthai.NeuralDepthConfig |
| `def setEdgeThreshold(self, arg0: int) -> NeuralDepthConfig` | `(self, arg0: int)` | L13820 | setEdgeThreshold(self: depthai.NeuralDepthConfig, arg0: int) -> depthai.NeuralDepthConfig |

**Nested Class:**

<a id="class-postprocessing"></a>
#### class `PostProcessing`  — L13773

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `confidenceThreshold` | `int` | — | L13774 |
| `edgeThreshold` | `int` | — | L13775 |
| `temporalFilter` | `filters.params.TemporalFilter` | — | L13776 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L13777 | __init__(self: depthai.NeuralDepthConfig.PostProcessing) -> None |

<a id="class-neuraldepthproperties"></a>
### class `NeuralDepthProperties`  — L13829

> Specify properties for NeuralDepth

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L13831 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-neuralnetworkproperties"></a>
### class `NeuralNetworkProperties`  — L13834

> Specify properties for NeuralNetwork such as blob path, ...

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `blobSize` | `int | None` | — | L13836 |
| `blobUri` | `str` | — | L13837 |
| `numFrames` | `int` | — | L13838 |
| `numNCEPerThread` | `int` | — | L13839 |
| `numThreads` | `int` | — | L13840 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L13841 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-node"></a>
### class `Node`  — L13844

> Abstract Node

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L14315 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def id(self) -> int` | `(self)` | L14446 | Id of node. Assigned after being placed on the pipeline |

**🔹 Public Methods (15):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def add(self, node: Node) -> None` | `(self, node: Node)` | L14317 | add(self: depthai.Node, node: depthai.Node) -> None |
| `@overload` `def getAssetManager(self) -> AssetManager` | `(self)` | L14323 | getAssetManager(*args, **kwargs) |
| `@overload` `def getAssetManager(self) -> AssetManager` | `(self)` | L14336 | getAssetManager(*args, **kwargs) |
| `def getInputMapRefs(self) -> list[Node.InputMap]` | `(self)` | L14348 | getInputMapRefs(self: depthai.Node) -> list[depthai.Node.InputMap] |
| `@overload` `def getInputRefs(self) -> list[Node.Input]` | `(self)` | L14354 | getInputRefs(*args, **kwargs) |
| `@overload` `def getInputRefs(self) -> list[Node.Input]` | `(self)` | L14367 | getInputRefs(*args, **kwargs) |
| `def getInputs(self) -> list[Node.Input]` | `(self)` | L14379 | getInputs(self: depthai.Node) -> list[depthai.Node.Input] |
| `def getName(self) -> str` | `(self)` | L14384 | getName(self: depthai.Node) -> str |
| `def getOutputMapRefs(self) -> list[Node.OutputMap]` | `(self)` | L14389 | getOutputMapRefs(self: depthai.Node) -> list[depthai.Node.OutputMap] |
| `@overload` `def getOutputRefs(self) -> list[Node.Output]` | `(self)` | L14395 | getOutputRefs(*args, **kwargs) |
| `@overload` `def getOutputRefs(self) -> list[Node.Output]` | `(self)` | L14408 | getOutputRefs(*args, **kwargs) |
| `def getOutputs(self) -> list[Node.Output]` | `(self)` | L14420 | getOutputs(self: depthai.Node) -> list[depthai.Node.Output] |
| `@overload` `def getParentPipeline(self) -> Pipeline` | `(self)` | L14426 | getParentPipeline(*args, **kwargs) |
| `@overload` `def getParentPipeline(self) -> Pipeline` | `(self)` | L14435 | getParentPipeline(*args, **kwargs) |
| `def stopPipeline(self) -> None` | `(self)` | L14443 | stopPipeline(self: depthai.Node) -> None |

**Nested Class:**

<a id="class-connection"></a>
#### class `Connection`  — L13847

> Connection between an Input and Output

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `inputGroup` | `str` | — | L13849 |
| `inputId` | `int` | — | L13850 |
| `inputName` | `str` | — | L13851 |
| `outputGroup` | `str` | — | L13852 |
| `outputId` | `int` | — | L13853 |
| `outputName` | `str` | — | L13854 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L13855 | Initialize self.  See help(type(self)) for accurate signature. |

**Nested Class:**

<a id="class-datatypehierarchy"></a>
#### class `DatatypeHierarchy`  — L13858

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `datatype` | `DatatypeEnum` | — | L13859 |
| `descendants` | `bool` | — | L13860 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, arg0: DatatypeEnum, arg1: bool) -> None` | `(self, arg0: DatatypeEnum, arg1: bool)` | L13861 | __init__(self: depthai.Node.DatatypeHierarchy, arg0: depthai.DatatypeEnum, arg1: bool) -> None |

**Nested Class:**

<a id="class-id"></a>
#### class `Id`  — L13864

> Node identificator. Unique for every node on a single Pipeline

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L13866 | Initialize self.  See help(type(self)) for accurate signature. |

**Nested Class:**

<a id="class-input"></a>
#### class `Input(MessageQueue)`  — L13869

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `possibleDatatypes` | `list[Node.DatatypeHierarchy]` | — | L13901 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, parent: Node, name: str = ..., group: str = ..., blocking: bool = ..., queueSize: int = ..., types: list[Node.DatatypeHierarchy] = ..., waitForMessage: bool = ...) -> None` | `(self, parent: Node, name: str = ..., group: str = ..., blocking: bool = ..., queueSize: int = ..., types: list[Node.DatatypeHierarchy] = ..., waitForMessage: bool = ...)` | L13902 | __init__(self: depthai.Node.Input, parent: depthai.Node, name: str = '', group: str = '', blocking: bool = True, queueSize: int = 3, types: list[depthai.Node.DatatypeHierarchy] = [<depthai.Node.DatatypeHierarchy object at 0x0000023408AF0C30>], waitForMessage: bool = False) -> None |

**🔹 Public Methods (11):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def createInputQueue(self, maxSize: int = ..., blocking: bool = ...) -> InputQueue` | `(self, maxSize: int = ..., blocking: bool = ...)` | L13904 | createInputQueue(self: depthai.Node.Input, maxSize: int = 16, blocking: bool = False) -> depthai.InputQueue |
| `@overload` `def getParent(self) -> Node` | `(self)` | L13920 | getParent(*args, **kwargs) |
| `@overload` `def getParent(self) -> Node` | `(self)` | L13933 | getParent(*args, **kwargs) |
| `def getPossibleDatatypes(self) -> list[Node.DatatypeHierarchy]` | `(self)` | L13945 | getPossibleDatatypes(self: depthai.Node.Input) -> list[depthai.Node.DatatypeHierarchy] |
| `def getReusePreviousMessage(self) -> bool` | `(self)` | L13950 | getReusePreviousMessage(self: depthai.Node.Input) -> bool |
| `def getWaitForMessage(self) -> bool` | `(self)` | L13955 | getWaitForMessage(self: depthai.Node.Input) -> bool |
| `def getXLinkBridge(self) -> node.internal.XLinkInBridge` | `(self)` | L13964 | getXLinkBridge(self: depthai.Node.Input) -> depthai.node.internal.XLinkInBridge |
| `@overload` `def setPossibleDatatypes(self, types: list[Node.DatatypeHierarchy]) -> None` | `(self, types: list[Node.DatatypeHierarchy])` | L13975 | setPossibleDatatypes(*args, **kwargs) |
| `@overload` `def setPossibleDatatypes(self, types: list[tuple[DatatypeEnum, bool]]) -> None` | `(self, types: list[tuple[DatatypeEnum, bool]])` | L13988 | setPossibleDatatypes(*args, **kwargs) |
| `def setReusePreviousMessage(self, reusePreviousMessage: bool) -> None` | `(self, reusePreviousMessage: bool)` | L14000 | setReusePreviousMessage(self: depthai.Node.Input, reusePreviousMessage: bool) -> None |
| `def setWaitForMessage(self, waitForMessage: bool) -> None` | `(self, waitForMessage: bool)` | L14005 | setWaitForMessage(self: depthai.Node.Input, waitForMessage: bool) -> None |

**Nested Class:**

<a id="class-type"></a>
##### class `Type`  — L13870

> Members:

SReceiver

MReceiver

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L13876 |
| `MReceiver` | `ClassVar[Node.Input.Type]` | `...` | L13877 |
| `SReceiver` | `ClassVar[Node.Input.Type]` | `...` | L13878 |
| `__entries` | `ClassVar[dict]` | `...` | L13879 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L13880 | __init__(self: depthai.Node.Input.Type, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L13882 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L13884 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L13886 | __index__(self: depthai.Node.Input.Type) -> int |
| `def __int__(self) -> int` | `(self)` | L13888 | __int__(self: depthai.Node.Input.Type) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L13890 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L13893 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L13899 | (arg0: depthai.Node.Input.Type) -> int |

**Nested Class:**

<a id="class-inputmap"></a>
#### class `InputMap`  — L14016

**🔧 Dunder Methods (11):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L14017 | Initialize self.  See help(type(self)) for accurate signature. |
| `def __bool__(self) -> bool` | `(self)` | L14021 | __bool__(self: depthai.Node.InputMap) -> bool |
| `@overload` `def __contains__(self, arg0: str) -> bool` | `(self, arg0: str)` | L14027 | __contains__(*args, **kwargs) |
| `@overload` `def __contains__(self, arg0: tuple[str, str]) -> bool` | `(self, arg0: tuple[str, str])` | L14036 | __contains__(*args, **kwargs) |
| `@overload` `def __delitem__(self, arg0: str) -> None` | `(self, arg0: str)` | L14045 | __delitem__(*args, **kwargs) |
| `@overload` `def __delitem__(self, arg0: tuple[str, str]) -> None` | `(self, arg0: tuple[str, str])` | L14054 | __delitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, arg0: str) -> Node.Input` | `(self, arg0: str)` | L14063 | __getitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, arg0: tuple[str, str]) -> Node.Input` | `(self, arg0: tuple[str, str])` | L14072 | __getitem__(*args, **kwargs) |
| `def __iter__(self) -> Iterator[tuple[str, str]]` | `(self)` | L14080 | __iter__(self: depthai.Node.InputMap) -> Iterator[tuple[str, str]] |
| `def __len__(self) -> int` | `(self)` | L14082 | __len__(self: depthai.Node.InputMap) -> int |
| `def __setitem__(self, arg0: tuple[str, str], arg1: Node.Input) -> None` | `(self, arg0: tuple[str, str], arg1: Node.Input)` | L14084 | __setitem__(self: depthai.Node.InputMap, arg0: tuple[str, str], arg1: depthai.Node.Input) -> None |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def items(self) -> Iterator[tuple[tuple[str, str], Node.Input]]` | `(self)` | L14019 | items(self: depthai.Node.InputMap) -> Iterator[tuple[tuple[str, str], depthai.Node.Input]] |

**Nested Class:**

<a id="class-output"></a>
#### class `Output`  — L14087

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, parent: Node, name: str = ..., group: str = ..., possibleDatatypes: list[Node.DatatypeHierarchy] = ...) -> None` | `(self, parent: Node, name: str = ..., group: str = ..., possibleDatatypes: list[Node.DatatypeHierarchy] = ...)` | L14119 | __init__(self: depthai.Node.Output, parent: depthai.Node, name: str = '', group: str = '', possibleDatatypes: list[depthai.Node.DatatypeHierarchy] = [<depthai.Node.DatatypeHierarchy object at 0x0000023406770870>]) -> None |

**🔹 Public Methods (14):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def canConnect(self, input: Node.Input) -> bool` | `(self, input: Node.Input)` | L14121 | canConnect(self: depthai.Node.Output, input: depthai.Node.Input) -> bool |
| `def createOutputQueue(self, maxSize: int = ..., blocking: bool = ...) -> MessageQueue` | `(self, maxSize: int = ..., blocking: bool = ...)` | L14132 | createOutputQueue(self: depthai.Node.Output, maxSize: int = 16, blocking: bool = False) -> depthai.MessageQueue |
| `def getName(self) -> str` | `(self)` | L14146 | getName(self: depthai.Node.Output) -> str |
| `@overload` `def getParent(self) -> Node` | `(self)` | L14152 | getParent(*args, **kwargs) |
| `@overload` `def getParent(self) -> Node` | `(self)` | L14161 | getParent(*args, **kwargs) |
| `def getPossibleDatatypes(self) -> list[Node.DatatypeHierarchy]` | `(self)` | L14169 | getPossibleDatatypes(self: depthai.Node.Output) -> list[depthai.Node.DatatypeHierarchy] |
| `def getXLinkBridge(self) -> node.internal.XLinkOutBridge` | `(self)` | L14174 | getXLinkBridge(self: depthai.Node.Output) -> depthai.node.internal.XLinkOutBridge |
| `def isSamePipeline(self, input: Node.Input) -> bool` | `(self, input: Node.Input)` | L14184 | isSamePipeline(self: depthai.Node.Output, input: depthai.Node.Input) -> bool |
| `def link(self, input: Node.Input) -> None` | `(self, input: Node.Input)` | L14195 | link(self: depthai.Node.Output, input: depthai.Node.Input) -> None |
| `def send(self, msg: ADatatype) -> None` | `(self, msg: ADatatype)` | L14197 | send(self: depthai.Node.Output, msg: depthai.ADatatype) -> None |
| `@overload` `def setPossibleDatatypes(self, types: list[Node.DatatypeHierarchy]) -> None` | `(self, types: list[Node.DatatypeHierarchy])` | L14206 | setPossibleDatatypes(*args, **kwargs) |
| `@overload` `def setPossibleDatatypes(self, types: list[tuple[DatatypeEnum, bool]]) -> None` | `(self, types: list[tuple[DatatypeEnum, bool]])` | L14219 | setPossibleDatatypes(*args, **kwargs) |
| `def trySend(self, msg: ADatatype) -> bool` | `(self, msg: ADatatype)` | L14231 | trySend(self: depthai.Node.Output, msg: depthai.ADatatype) -> bool |
| `def unlink(self, input: Node.Input) -> None` | `(self, input: Node.Input)` | L14242 | unlink(self: depthai.Node.Output, input: depthai.Node.Input) -> None |

**Nested Class:**

<a id="class-type"></a>
##### class `Type`  — L14088

> Members:

MSender

SSender

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L14094 |
| `MSender` | `ClassVar[Node.Output.Type]` | `...` | L14095 |
| `SSender` | `ClassVar[Node.Output.Type]` | `...` | L14096 |
| `__entries` | `ClassVar[dict]` | `...` | L14097 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L14098 | __init__(self: depthai.Node.Output.Type, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L14100 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L14102 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L14104 | __index__(self: depthai.Node.Output.Type) -> int |
| `def __int__(self) -> int` | `(self)` | L14106 | __int__(self: depthai.Node.Output.Type) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L14108 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L14111 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L14117 | (arg0: depthai.Node.Output.Type) -> int |

**Nested Class:**

<a id="class-outputmap"></a>
#### class `OutputMap`  — L14245

**🔧 Dunder Methods (11):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L14246 | Initialize self.  See help(type(self)) for accurate signature. |
| `def __bool__(self) -> bool` | `(self)` | L14250 | __bool__(self: depthai.Node.OutputMap) -> bool |
| `@overload` `def __contains__(self, arg0: str) -> bool` | `(self, arg0: str)` | L14256 | __contains__(*args, **kwargs) |
| `@overload` `def __contains__(self, arg0: tuple[str, str]) -> bool` | `(self, arg0: tuple[str, str])` | L14265 | __contains__(*args, **kwargs) |
| `@overload` `def __delitem__(self, arg0: str) -> None` | `(self, arg0: str)` | L14274 | __delitem__(*args, **kwargs) |
| `@overload` `def __delitem__(self, arg0: tuple[str, str]) -> None` | `(self, arg0: tuple[str, str])` | L14283 | __delitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, arg0: str) -> Node.Output` | `(self, arg0: str)` | L14292 | __getitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, arg0: tuple[str, str]) -> Node.Output` | `(self, arg0: tuple[str, str])` | L14301 | __getitem__(*args, **kwargs) |
| `def __iter__(self) -> Iterator[tuple[str, str]]` | `(self)` | L14309 | __iter__(self: depthai.Node.OutputMap) -> Iterator[tuple[str, str]] |
| `def __len__(self) -> int` | `(self)` | L14311 | __len__(self: depthai.Node.OutputMap) -> int |
| `def __setitem__(self, arg0: tuple[str, str], arg1: Node.Output) -> None` | `(self, arg0: tuple[str, str], arg1: Node.Output)` | L14313 | __setitem__(self: depthai.Node.OutputMap, arg0: tuple[str, str], arg1: depthai.Node.Output) -> None |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def items(self) -> Iterator[tuple[tuple[str, str], Node.Output]]` | `(self)` | L14248 | items(self: depthai.Node.OutputMap) -> Iterator[tuple[tuple[str, str], depthai.Node.Output]] |

<a id="class-nodegroup"></a>
### class `NodeGroup(Node)`  — L14451

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L14452 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-nodestate"></a>
### class `NodeState`  — L14455

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `events` | `list[NodeState.DurationEvent]` | — | L14615 |
| `inputStates` | `dict[str, NodeState.InputQueueState]` | — | L14616 |
| `inputsGetTiming` | `NodeState.Timing` | — | L14617 |
| `mainLoopTiming` | `NodeState.Timing` | — | L14618 |
| `otherTimings` | `dict[str, NodeState.Timing]` | — | L14619 |
| `outputStates` | `dict[str, NodeState.OutputQueueState]` | — | L14620 |
| `outputsSendTiming` | `NodeState.Timing` | — | L14621 |
| `state` | `NodeState.State` | — | L14622 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L14623 | __init__(self: depthai.NodeState) -> None |

**Nested Class:**

<a id="class-durationevent"></a>
#### class `DurationEvent`  — L14456

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `durationUs` | `int` | — | L14457 |
| `startEvent` | `PipelineEvent` | — | L14458 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L14459 | __init__(self: depthai.NodeState.DurationEvent) -> None |

**Nested Class:**

<a id="class-durationstats"></a>
#### class `DurationStats`  — L14462

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `averageMicrosRecent` | `int` | — | L14463 |
| `maxMicros` | `int` | — | L14464 |
| `maxMicrosRecent` | `int` | — | L14465 |
| `medianMicrosRecent` | `int` | — | L14466 |
| `minMicros` | `int` | — | L14467 |
| `minMicrosRecent` | `int` | — | L14468 |
| `stdDevMicrosRecent` | `int` | — | L14469 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L14470 | __init__(self: depthai.NodeState.DurationStats) -> None |

**Nested Class:**

<a id="class-inputqueuestate"></a>
#### class `InputQueueState`  — L14473

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `numQueued` | `int` | — | L14510 |
| `queueStats` | `NodeState.QueueStats` | — | L14511 |
| `state` | `NodeState.InputQueueState.State` | — | L14512 |
| `timing` | `NodeState.Timing` | — | L14513 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L14514 | __init__(self: depthai.NodeState.InputQueueState) -> None |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def isValid(self) -> bool` | `(self)` | L14516 | isValid(self: depthai.NodeState.InputQueueState) -> bool |

**Nested Class:**

<a id="class-state"></a>
##### class `State`  — L14474

> Members:

  IDLE

  WAITING

  BLOCKED

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L14484 |
| `BLOCKED` | `ClassVar[NodeState.InputQueueState.State]` | `...` | L14485 |
| `IDLE` | `ClassVar[NodeState.InputQueueState.State]` | `...` | L14486 |
| `WAITING` | `ClassVar[NodeState.InputQueueState.State]` | `...` | L14487 |
| `__entries` | `ClassVar[dict]` | `...` | L14488 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L14489 | __init__(self: depthai.NodeState.InputQueueState.State, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L14491 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L14493 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L14495 | __index__(self: depthai.NodeState.InputQueueState.State) -> int |
| `def __int__(self) -> int` | `(self)` | L14497 | __int__(self: depthai.NodeState.InputQueueState.State) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L14499 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L14502 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L14508 | (arg0: depthai.NodeState.InputQueueState.State) -> int |

**Nested Class:**

<a id="class-outputqueuestate"></a>
#### class `OutputQueueState`  — L14519

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `state` | `NodeState.OutputQueueState.State` | — | L14553 |
| `timing` | `NodeState.Timing` | — | L14554 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L14555 | __init__(self: depthai.NodeState.OutputQueueState) -> None |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def isValid(self) -> bool` | `(self)` | L14557 | isValid(self: depthai.NodeState.OutputQueueState) -> bool |

**Nested Class:**

<a id="class-state"></a>
##### class `State`  — L14520

> Members:

  IDLE

  SENDING

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L14528 |
| `IDLE` | `ClassVar[NodeState.OutputQueueState.State]` | `...` | L14529 |
| `SENDING` | `ClassVar[NodeState.OutputQueueState.State]` | `...` | L14530 |
| `__entries` | `ClassVar[dict]` | `...` | L14531 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L14532 | __init__(self: depthai.NodeState.OutputQueueState.State, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L14534 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L14536 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L14538 | __index__(self: depthai.NodeState.OutputQueueState.State) -> int |
| `def __int__(self) -> int` | `(self)` | L14540 | __int__(self: depthai.NodeState.OutputQueueState.State) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L14542 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L14545 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L14551 | (arg0: depthai.NodeState.OutputQueueState.State) -> int |

**Nested Class:**

<a id="class-queuestats"></a>
#### class `QueueStats`  — L14560

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `maxQueued` | `int` | — | L14561 |
| `maxQueuedRecent` | `int` | — | L14562 |
| `medianQueuedRecent` | `int` | — | L14563 |
| `minQueuedRecent` | `int` | — | L14564 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L14565 | __init__(self: depthai.NodeState.QueueStats) -> None |

**Nested Class:**

<a id="class-state"></a>
#### class `State`  — L14568

> Members:

  IDLE

  GETTING_INPUTS

  PROCESSING

  SENDING_OUTPUTS

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L14580 |
| `GETTING_INPUTS` | `ClassVar[NodeState.State]` | `...` | L14581 |
| `IDLE` | `ClassVar[NodeState.State]` | `...` | L14582 |
| `PROCESSING` | `ClassVar[NodeState.State]` | `...` | L14583 |
| `SENDING_OUTPUTS` | `ClassVar[NodeState.State]` | `...` | L14584 |
| `__entries` | `ClassVar[dict]` | `...` | L14585 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L14586 | __init__(self: depthai.NodeState.State, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L14588 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L14590 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L14592 | __index__(self: depthai.NodeState.State) -> int |
| `def __int__(self) -> int` | `(self)` | L14594 | __int__(self: depthai.NodeState.State) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L14596 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L14599 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L14605 | (arg0: depthai.NodeState.State) -> int |

**Nested Class:**

<a id="class-timing"></a>
#### class `Timing`  — L14608

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `durationStats` | `NodeState.DurationStats` | — | L14609 |
| `fps` | `float` | — | L14610 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L14611 | __init__(self: depthai.NodeState.Timing) -> None |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def isValid(self) -> bool` | `(self)` | L14613 | isValid(self: depthai.NodeState.Timing) -> bool |

<a id="class-nodestateapi"></a>
### class `NodeStateApi`  — L14626

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L14627 | Initialize self.  See help(type(self)) for accurate signature. |

**🔹 Public Methods (11):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def detailed(self) -> NodeState` | `(self)` | L14629 | detailed(self: depthai.NodeStateApi) -> depthai.NodeState |
| `@overload` `def inputs(self) -> dict[str, NodeState.InputQueueState]` | `(self)` | L14632 | inputs(*args, **kwargs) |
| `@overload` `def inputs(self, inputNames: list[str]) -> dict[str, NodeState.InputQueueState]` | `(self, inputNames: list[str])` | L14643 | inputs(*args, **kwargs) |
| `@overload` `def inputs(self, inputName: str) -> NodeState.InputQueueState` | `(self, inputName: str)` | L14654 | inputs(*args, **kwargs) |
| `@overload` `def otherTimings(self) -> dict[str, NodeState.Timing]` | `(self)` | L14665 | otherTimings(*args, **kwargs) |
| `@overload` `def otherTimings(self, timingNames: list[str]) -> dict[str, NodeState.Timing]` | `(self, timingNames: list[str])` | L14676 | otherTimings(*args, **kwargs) |
| `@overload` `def otherTimings(self, timingName: str) -> NodeState.Timing` | `(self, timingName: str)` | L14687 | otherTimings(*args, **kwargs) |
| `@overload` `def outputs(self) -> dict[str, NodeState.OutputQueueState]` | `(self)` | L14698 | outputs(*args, **kwargs) |
| `@overload` `def outputs(self, outputNames: list[str]) -> dict[str, NodeState.OutputQueueState]` | `(self, outputNames: list[str])` | L14709 | outputs(*args, **kwargs) |
| `@overload` `def outputs(self, outputName: str) -> NodeState.OutputQueueState` | `(self, outputName: str)` | L14720 | outputs(*args, **kwargs) |
| `def summary(self) -> NodeState` | `(self)` | L14730 | summary(self: depthai.NodeStateApi) -> depthai.NodeState |

<a id="class-nodesstateapi"></a>
### class `NodesStateApi`  — L14733

> pipeline.getState().nodes({nodeId1}).summary() ->
std::unordered_map<std::string, TimingStats>;
pipeline.getState().nodes({nodeId1}).detailed() ->
std::unordered_map<std::string, NodeState>;
pipeline.getState().nodes(nodeId1).detailed() -> NodeState;
pipeline.getState().nodes({nodeId1}).outputs() ->
std::unordered_map<std::string, TimingStats>;
pipeline.getState().nodes({nodeId1}).outputs({outputName1}) ->
std::unordered_map<std::string, TimingStats>;
pipeline.getState().nodes({nodeId1}).outputs(outputName) -> TimingStats;
pipeline.getState().nodes({nodeId1}).events();
pipeline.getState().nodes({nodeId1}).inputs() -> std::unordered_map<std::string,
QueueState>; pipeline.getState().nodes({nodeId1}).inputs({inputName1}) ->
std::unordered_map<std::string, QueueState>;
pipeline.getState().nodes({nodeId1}).inputs(inputName) -> QueueState;
pipeline.getState().nodes({nodeId1}).otherStats() ->
std::unordered_map<std::string, TimingStats>;
pipeline.getState().nodes({nodeId1}).otherStats({statName1}) ->
std::unordered_map<std::string, TimingStats>;
pipeline.getState().nodes({nodeId1}).outputs(statName) -> TimingStats;

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L14754 | Initialize self.  See help(type(self)) for accurate signature. |

**🔹 Public Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def detailed(self) -> PipelineState` | `(self)` | L14756 | detailed(self: depthai.NodesStateApi) -> depthai.PipelineState |
| `def inputs(self) -> dict[int, dict[str, NodeState.InputQueueState]]` | `(self)` | L14758 | inputs(self: depthai.NodesStateApi) -> dict[int, dict[str, depthai.NodeState.InputQueueState]] |
| `def otherTimings(self) -> dict[int, dict[str, NodeState.Timing]]` | `(self)` | L14760 | otherTimings(self: depthai.NodesStateApi) -> dict[int, dict[str, depthai.NodeState.Timing]] |
| `def outputs(self) -> dict[int, dict[str, NodeState.OutputQueueState]]` | `(self)` | L14762 | outputs(self: depthai.NodesStateApi) -> dict[int, dict[str, depthai.NodeState.OutputQueueState]] |
| `def summary(self) -> PipelineState` | `(self)` | L14764 | summary(self: depthai.NodesStateApi) -> depthai.PipelineState |

<a id="class-objecttrackerproperties"></a>
### class `ObjectTrackerProperties`  — L14767

> Specify properties for ObjectTracker

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `detectionLabelsToTrack` | `list[int]` | — | L14769 |
| `maxObjectsToTrack` | `int` | — | L14770 |
| `trackerIdAssignmentPolicy` | `TrackerIdAssignmentPolicy` | — | L14771 |
| `trackerThreshold` | `float` | — | L14772 |
| `trackerType` | `TrackerType` | — | L14773 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L14774 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-openvino"></a>
### class `OpenVINO`  — L14777

> Support for basic OpenVINO related actions like version identification of neural
network blobs,...

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `DEFAULT_VERSION` | `ClassVar[OpenVINO.Version]` | `...` | L14970 |
| `VERSION_2020_3` | `ClassVar[OpenVINO.Version]` | `...` | L14971 |
| `VERSION_2020_4` | `ClassVar[OpenVINO.Version]` | `...` | L14972 |
| `VERSION_2021_1` | `ClassVar[OpenVINO.Version]` | `...` | L14973 |
| `VERSION_2021_2` | `ClassVar[OpenVINO.Version]` | `...` | L14974 |
| `VERSION_2021_3` | `ClassVar[OpenVINO.Version]` | `...` | L14975 |
| `VERSION_2021_4` | `ClassVar[OpenVINO.Version]` | `...` | L14976 |
| `VERSION_2022_1` | `ClassVar[OpenVINO.Version]` | `...` | L14977 |
| `VERSION_UNIVERSAL` | `ClassVar[OpenVINO.Version]` | `...` | L14978 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L14979 | Initialize self.  See help(type(self)) for accurate signature. |

**⚡ Static Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@staticmethod` `def areVersionsBlobCompatible(v1: OpenVINO.Version, v2: OpenVINO.Version) -> bool` | `(v1: OpenVINO.Version, v2: OpenVINO.Version)` | L14982 | areVersionsBlobCompatible(v1: depthai.OpenVINO.Version, v2: depthai.OpenVINO.Version) -> bool |
| `@staticmethod` `def getBlobLatestSupportedVersion(*args, **kwargs)` | `(*args, **kwargs)` | L14988 | getBlobLatestSupportedVersion(majorVersion: int, majorVersion: int) -> depthai.OpenVINO.Version |
| `@staticmethod` `def getBlobSupportedVersions(*args, **kwargs)` | `(*args, **kwargs)` | L15003 | getBlobSupportedVersions(majorVersion: int, majorVersion: int) -> list[depthai.OpenVINO.Version] |
| `@staticmethod` `def getVersionName(version: OpenVINO.Version) -> str` | `(version: OpenVINO.Version)` | L15019 | getVersionName(version: depthai.OpenVINO.Version) -> str |
| `@staticmethod` `def getVersions() -> list[OpenVINO.Version]` | `()` | L15031 | getVersions() -> list[depthai.OpenVINO.Version] |
| `@staticmethod` `def parseVersionName(versionString: str) -> OpenVINO.Version` | `(versionString: str)` | L15038 | parseVersionName(versionString: str) -> depthai.OpenVINO.Version |

**Nested Class:**

<a id="class-blob"></a>
#### class `Blob`  — L14781

> OpenVINO Blob

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `data` | `Incomplete` | — | L14783 |
| `device` | `OpenVINO.Device` | — | L14784 |
| `networkInputs` | `dict[str, TensorInfo]` | — | L14785 |
| `networkOutputs` | `dict[str, TensorInfo]` | — | L14786 |
| `numShaves` | `int` | — | L14787 |
| `numSlices` | `int` | — | L14788 |
| `stageCount` | `int` | — | L14789 |
| `version` | `OpenVINO.Version` | — | L14790 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self, arg0, std) -> None` | `(self, arg0, std)` | L14792 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: os.PathLike) -> None` | `(self, arg0: os.PathLike)` | L14811 | __init__(*args, **kwargs) |

**Nested Class:**

<a id="class-device"></a>
#### class `Device`  — L14830

> Members:

  VPU

  VPUX

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L14838 |
| `VPU` | `ClassVar[OpenVINO.Device]` | `...` | L14839 |
| `VPUX` | `ClassVar[OpenVINO.Device]` | `...` | L14840 |
| `__entries` | `ClassVar[dict]` | `...` | L14841 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L14842 | __init__(self: depthai.OpenVINO.Device, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L14844 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L14846 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L14848 | __index__(self: depthai.OpenVINO.Device) -> int |
| `def __int__(self) -> int` | `(self)` | L14850 | __int__(self: depthai.OpenVINO.Device) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L14852 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L14855 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L14861 | (arg0: depthai.OpenVINO.Device) -> int |

**Nested Class:**

<a id="class-superblob"></a>
#### class `SuperBlob`  — L14864

> A superblob is an efficient way of storing generated blobs for all different
number of shaves.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `NUMBER_OF_PATCHES` | `ClassVar[int]` | `...` | L14867 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self, superblobBytes, std) -> None` | `(self, superblobBytes, std)` | L14869 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, pathToSuperBlobFile: str) -> None` | `(self, pathToSuperBlobFile: str)` | L14888 | __init__(*args, **kwargs) |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getBlobWithNumShaves(self, numShaves: int) -> OpenVINO.Blob` | `(self, numShaves: int)` | L14906 | getBlobWithNumShaves(self: depthai.OpenVINO.SuperBlob, numShaves: int) -> depthai.OpenVINO.Blob |

**Nested Class:**

<a id="class-version"></a>
#### class `Version`  — L14919

> OpenVINO Version supported version information

Members:

  VERSION_2020_3

  VERSION_2020_4

  VERSION_2021_1

  VERSION_2021_2

  VERSION_2021_3

  VERSION_2021_4

  VERSION_2022_1

  VERSION_UNIVERSAL

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L14939 |
| `VERSION_2020_3` | `ClassVar[OpenVINO.Version]` | `...` | L14940 |
| `VERSION_2020_4` | `ClassVar[OpenVINO.Version]` | `...` | L14941 |
| `VERSION_2021_1` | `ClassVar[OpenVINO.Version]` | `...` | L14942 |
| `VERSION_2021_2` | `ClassVar[OpenVINO.Version]` | `...` | L14943 |
| `VERSION_2021_3` | `ClassVar[OpenVINO.Version]` | `...` | L14944 |
| `VERSION_2021_4` | `ClassVar[OpenVINO.Version]` | `...` | L14945 |
| `VERSION_2022_1` | `ClassVar[OpenVINO.Version]` | `...` | L14946 |
| `VERSION_UNIVERSAL` | `ClassVar[OpenVINO.Version]` | `...` | L14947 |
| `__entries` | `ClassVar[dict]` | `...` | L14948 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L14949 | __init__(self: depthai.OpenVINO.Version, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L14951 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L14953 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L14955 | __index__(self: depthai.OpenVINO.Version) -> int |
| `def __int__(self) -> int` | `(self)` | L14957 | __int__(self: depthai.OpenVINO.Version) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L14959 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L14962 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L14968 | (arg0: depthai.OpenVINO.Version) -> int |

<a id="class-pipeline"></a>
### class `Pipeline`  — L15050

**🔧 Dunder Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self, createImplicitDevice: bool = ...) -> None` | `(self, createImplicitDevice: bool = ...)` | L15052 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, defaultDevice: Device) -> None` | `(self, defaultDevice: Device)` | L15071 | __init__(*args, **kwargs) |
| `def __enter__(self) -> Pipeline` | `(self)` | L15254 | __enter__(self: depthai.Pipeline) -> depthai.Pipeline |
| `def __exit__(self, arg0: object, arg1: object, arg2: object) -> None` | `(self, arg0: object, arg1: object, arg2: object)` | L15256 | __exit__(self: depthai.Pipeline, arg0: object, arg1: object, arg2: object) -> None |

**🔹 Public Methods (32):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def add(self, arg0: Node) -> Node` | `(self, arg0: Node)` | L15089 | add(self: depthai.Pipeline, arg0: depthai.Node) -> depthai.Node |
| `def build(self) -> None` | `(self)` | L15091 | build(self: depthai.Pipeline) -> None |
| `def create(self, arg0: Type[T], *args, **kwargs) -> T` | `(self, arg0: Type[T], *args, **kwargs)` | L15093 | create(self: depthai.Pipeline, arg0: object, *args, **kwargs) -> depthai.Node |
| `def enableHolisticRecord(self, recordConfig: RecordConfig) -> None` | `(self, recordConfig: RecordConfig)` | L15095 | enableHolisticRecord(self: depthai.Pipeline, recordConfig: depthai.RecordConfig) -> None |
| `def enableHolisticReplay(self, recordingPath: str) -> None` | `(self, recordingPath: str)` | L15100 | enableHolisticReplay(self: depthai.Pipeline, recordingPath: str) -> None |
| `def enablePipelineDebugging(self, enable: bool = ...) -> None` | `(self, enable: bool = ...)` | L15102 | enablePipelineDebugging(self: depthai.Pipeline, enable: bool = True) -> None |
| `def getAllNodes(self) -> list[Node]` | `(self)` | L15107 | getAllNodes(self: depthai.Pipeline) -> list[depthai.Node] |
| `@overload` `def getAssetManager(self) -> AssetManager` | `(self)` | L15113 | getAssetManager(*args, **kwargs) |
| `@overload` `def getAssetManager(self) -> AssetManager` | `(self)` | L15126 | getAssetManager(*args, **kwargs) |
| `def getBoardConfig(self) -> BoardConfig` | `(self)` | L15138 | getBoardConfig(self: depthai.Pipeline) -> depthai.BoardConfig |
| `def getCalibrationData(self) -> CalibrationHandler` | `(self)` | L15143 | getCalibrationData(self: depthai.Pipeline) -> depthai.CalibrationHandler |
| `@overload` `def getDefaultDevice(self) -> Device` | `(self)` | L15152 | getDefaultDevice(*args, **kwargs) |
| `@overload` `def getDefaultDevice(self) -> Device` | `(self)` | L15161 | getDefaultDevice(*args, **kwargs) |
| `def getDeviceConfig(self) -> Device.Config` | `(self)` | L15169 | getDeviceConfig(self: depthai.Pipeline) -> depthai.Device.Config |
| `def getGlobalProperties(self) -> GlobalProperties` | `(self)` | L15174 | getGlobalProperties(self: depthai.Pipeline) -> depthai.GlobalProperties |
| `def getNode(self, arg0: int) -> Node` | `(self, arg0: int)` | L15180 | getNode(self: depthai.Pipeline, arg0: int) -> depthai.Node |
| `def getPipelineState(self) -> PipelineStateApi` | `(self)` | L15185 | getPipelineState(self: depthai.Pipeline) -> depthai.PipelineStateApi |
| `def isBuilt(self) -> bool` | `(self)` | L15187 | isBuilt(self: depthai.Pipeline) -> bool |
| `def isRunning(self) -> bool` | `(self)` | L15189 | isRunning(self: depthai.Pipeline) -> bool |
| `def processTasks(self, waitForTasks: bool = ..., timeoutSeconds: float = ...) -> None` | `(self, waitForTasks: bool = ..., timeoutSeconds: float = ...)` | L15191 | processTasks(self: depthai.Pipeline, waitForTasks: bool = False, timeoutSeconds: float = -1.0) -> None |
| `def remove(self, node: Node) -> None` | `(self, node: Node)` | L15193 | remove(self: depthai.Pipeline, node: depthai.Node) -> None |
| `def run(self) -> None` | `(self)` | L15198 | run(self: depthai.Pipeline) -> None |
| `def serializeToJson(self, arg0: bool) -> json` | `(self, arg0: bool)` | L15200 | serializeToJson(self: depthai.Pipeline, arg0: bool) -> json |
| `def setBoardConfig(self, arg0: BoardConfig) -> None` | `(self, arg0: BoardConfig)` | L15205 | setBoardConfig(self: depthai.Pipeline, arg0: depthai.BoardConfig) -> None |
| `def setCalibrationData(self, calibrationDataHandler: CalibrationHandler) -> None` | `(self, calibrationDataHandler: CalibrationHandler)` | L15210 | setCalibrationData(self: depthai.Pipeline, calibrationDataHandler: depthai.CalibrationHandler) -> None |
| `def setCameraTuningBlobPath(self, path: os.PathLike) -> None` | `(self, path: os.PathLike)` | L15218 | setCameraTuningBlobPath(self: depthai.Pipeline, path: os.PathLike) -> None |
| `def setSippBufferSize(self, sizeBytes: int) -> None` | `(self, sizeBytes: int)` | L15223 | setSippBufferSize(self: depthai.Pipeline, sizeBytes: int) -> None |
| `def setSippDmaBufferSize(self, sizeBytes: int) -> None` | `(self, sizeBytes: int)` | L15232 | setSippDmaBufferSize(self: depthai.Pipeline, sizeBytes: int) -> None |
| `def setXLinkChunkSize(self, sizeBytes: int) -> None` | `(self, sizeBytes: int)` | L15240 | setXLinkChunkSize(self: depthai.Pipeline, sizeBytes: int) -> None |
| `def start(self) -> None` | `(self)` | L15248 | start(self: depthai.Pipeline) -> None |
| `def stop(self) -> None` | `(self)` | L15250 | stop(self: depthai.Pipeline) -> None |
| `def wait(self) -> None` | `(self)` | L15252 | wait(self: depthai.Pipeline) -> None |

<a id="class-pipelineevent"></a>
### class `PipelineEvent(Buffer)`  — L15259

> Pipeline event message.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `interval` | `PipelineEvent.Interval` | — | L15381 |
| `nodeId` | `int` | — | L15382 |
| `queueSize` | `int | None` | — | L15383 |
| `source` | `str` | — | L15384 |
| `status` | `PipelineEvent.Status` | — | L15385 |
| `type` | `PipelineEvent.Type` | — | L15386 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L15387 | __init__(self: depthai.PipelineEvent) -> None |

**🔹 Public Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getSequenceNum(self) -> int` | `(self)` | L15389 | getSequenceNum(self: depthai.PipelineEvent) -> int |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L15394 | getTimestamp(self: depthai.PipelineEvent) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L15399 | getTimestampDevice(self: depthai.PipelineEvent) -> datetime.timedelta |
| `def setSequenceNum(self, arg0: int) -> None` | `(self, arg0: int)` | L15405 | setSequenceNum(self: depthai.PipelineEvent, arg0: int) -> None |
| `def setTimestamp(self, arg0: datetime.timedelta) -> None` | `(self, arg0: datetime.timedelta)` | L15410 | setTimestamp(self: depthai.PipelineEvent, arg0: datetime.timedelta) -> None |
| `def setTimestampDevice(self, arg0: datetime.timedelta) -> None` | `(self, arg0: datetime.timedelta)` | L15415 | setTimestampDevice(self: depthai.PipelineEvent, arg0: datetime.timedelta) -> None |

**Nested Class:**

<a id="class-interval"></a>
#### class `Interval`  — L15262

> Members:

  NONE

  START

  END

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L15272 |
| `END` | `ClassVar[PipelineEvent.Interval]` | `...` | L15273 |
| `NONE` | `ClassVar[PipelineEvent.Interval]` | `...` | L15274 |
| `START` | `ClassVar[PipelineEvent.Interval]` | `...` | L15275 |
| `__entries` | `ClassVar[dict]` | `...` | L15276 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L15277 | __init__(self: depthai.PipelineEvent.Interval, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L15279 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L15281 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L15283 | __index__(self: depthai.PipelineEvent.Interval) -> int |
| `def __int__(self) -> int` | `(self)` | L15285 | __int__(self: depthai.PipelineEvent.Interval) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L15287 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L15290 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L15296 | (arg0: depthai.PipelineEvent.Interval) -> int |

**Nested Class:**

<a id="class-status"></a>
#### class `Status`  — L15299

> Members:

  SUCCESS

  BLOCKED

  CANCELLED

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L15309 |
| `BLOCKED` | `ClassVar[PipelineEvent.Status]` | `...` | L15310 |
| `CANCELLED` | `ClassVar[PipelineEvent.Status]` | `...` | L15311 |
| `SUCCESS` | `ClassVar[PipelineEvent.Status]` | `...` | L15312 |
| `__entries` | `ClassVar[dict]` | `...` | L15313 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L15314 | __init__(self: depthai.PipelineEvent.Status, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L15316 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L15318 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L15320 | __index__(self: depthai.PipelineEvent.Status) -> int |
| `def __int__(self) -> int` | `(self)` | L15322 | __int__(self: depthai.PipelineEvent.Status) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L15324 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L15327 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L15333 | (arg0: depthai.PipelineEvent.Status) -> int |

**Nested Class:**

<a id="class-type"></a>
#### class `Type`  — L15336

> Members:

  CUSTOM

  LOOP

  INPUT

  OUTPUT

  INPUT_BLOCK

  OUTPUT_BLOCK

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L15352 |
| `CUSTOM` | `ClassVar[PipelineEvent.Type]` | `...` | L15353 |
| `INPUT` | `ClassVar[PipelineEvent.Type]` | `...` | L15354 |
| `INPUT_BLOCK` | `ClassVar[PipelineEvent.Type]` | `...` | L15355 |
| `LOOP` | `ClassVar[PipelineEvent.Type]` | `...` | L15356 |
| `OUTPUT` | `ClassVar[PipelineEvent.Type]` | `...` | L15357 |
| `OUTPUT_BLOCK` | `ClassVar[PipelineEvent.Type]` | `...` | L15358 |
| `__entries` | `ClassVar[dict]` | `...` | L15359 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L15360 | __init__(self: depthai.PipelineEvent.Type, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L15362 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L15364 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L15366 | __index__(self: depthai.PipelineEvent.Type) -> int |
| `def __int__(self) -> int` | `(self)` | L15368 | __int__(self: depthai.PipelineEvent.Type) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L15370 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L15373 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L15379 | (arg0: depthai.PipelineEvent.Type) -> int |

<a id="class-pipelinestate"></a>
### class `PipelineState(Buffer)`  — L15421

> Pipeline event message.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `nodeStates` | `dict[int, NodeState]` | — | L15423 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L15424 | __init__(self: depthai.PipelineState) -> None |

**🔹 Public Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getSequenceNum(self) -> int` | `(self)` | L15426 | getSequenceNum(self: depthai.PipelineState) -> int |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L15431 | getTimestamp(self: depthai.PipelineState) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L15436 | getTimestampDevice(self: depthai.PipelineState) -> datetime.timedelta |
| `def setSequenceNum(self, arg0: int) -> None` | `(self, arg0: int)` | L15442 | setSequenceNum(self: depthai.PipelineState, arg0: int) -> None |
| `def setTimestamp(self, arg0: datetime.timedelta) -> None` | `(self, arg0: datetime.timedelta)` | L15447 | setTimestamp(self: depthai.PipelineState, arg0: datetime.timedelta) -> None |
| `def setTimestampDevice(self, arg0: datetime.timedelta) -> None` | `(self, arg0: datetime.timedelta)` | L15452 | setTimestampDevice(self: depthai.PipelineState, arg0: datetime.timedelta) -> None |

<a id="class-pipelinestateapi"></a>
### class `PipelineStateApi`  — L15458

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L15459 | Initialize self.  See help(type(self)) for accurate signature. |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def nodes(self) -> NodesStateApi` | `(self)` | L15462 | nodes(*args, **kwargs) |
| `@overload` `def nodes(self, nodeIds: list[int]) -> NodesStateApi` | `(self, nodeIds: list[int])` | L15473 | nodes(*args, **kwargs) |
| `@overload` `def nodes(self, nodeId: int) -> NodeStateApi` | `(self, nodeId: int)` | L15484 | nodes(*args, **kwargs) |

<a id="class-platform"></a>
### class `Platform`  — L15495

> Hardware platform type

Members:

  RVC2 : 

  RVC3 : 

  RVC4 : 

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L15505 |
| `RVC2` | `ClassVar[Platform]` | `...` | L15506 |
| `RVC3` | `ClassVar[Platform]` | `...` | L15507 |
| `RVC4` | `ClassVar[Platform]` | `...` | L15508 |
| `__entries` | `ClassVar[dict]` | `...` | L15509 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L15510 | __init__(self: depthai.Platform, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L15512 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L15514 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L15516 | __index__(self: depthai.Platform) -> int |
| `def __int__(self) -> int` | `(self)` | L15518 | __int__(self: depthai.Platform) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L15520 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L15523 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L15529 | (arg0: depthai.Platform) -> int |

<a id="class-point2f"></a>
### class `Point2f`  — L15532

> Point2f structure

x and y coordinates that define a 2D point.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `x` | `float` | — | L15536 |
| `y` | `float` | — | L15537 |

**🔧 Dunder Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L15539 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, x: float, y: float) -> None` | `(self, x: float, y: float)` | L15550 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, x: float, y: float, normalized: bool) -> None` | `(self, x: float, y: float, normalized: bool)` | L15561 | __init__(*args, **kwargs) |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def isNormalized(self) -> bool` | `(self)` | L15571 | isNormalized(self: depthai.Point2f) -> bool |

<a id="class-point3d"></a>
### class `Point3d`  — L15574

> Point3d structure

x,y,z coordinates that define a 3D point.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `x` | `float` | — | L15578 |
| `y` | `float` | — | L15579 |
| `z` | `float` | — | L15580 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L15582 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: float, arg1: float, arg2: float) -> None` | `(self, arg0: float, arg1: float, arg2: float)` | L15591 | __init__(*args, **kwargs) |

<a id="class-point3f"></a>
### class `Point3f`  — L15600

> Point3f structure

x,y,z coordinates that define a 3D point.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `x` | `float` | — | L15604 |
| `y` | `float` | — | L15605 |
| `z` | `float` | — | L15606 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L15608 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: float, arg1: float, arg2: float) -> None` | `(self, arg0: float, arg1: float, arg2: float)` | L15617 | __init__(*args, **kwargs) |

<a id="class-point3frgba"></a>
### class `Point3fRGBA`  — L15626

> Point3fRGBA structure

x,y,z coordinates and RGB color values that define a 3D point with color.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `a` | `int` | — | L15630 |
| `b` | `int` | — | L15631 |
| `g` | `int` | — | L15632 |
| `r` | `int` | — | L15633 |
| `x` | `float` | — | L15634 |
| `y` | `float` | — | L15635 |
| `z` | `float` | — | L15636 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L15638 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: float, arg1: float, arg2: float, arg3: int, arg4: int, arg5: int) -> None` | `(self, arg0: float, arg1: float, arg2: float, arg3: int, arg4: int, arg5: int)` | L15647 | __init__(*args, **kwargs) |

<a id="class-pointcloudconfig"></a>
### class `PointCloudConfig(Buffer)`  — L15656

> PointCloudConfig message. Carries ROI (region of interest) and threshold for
depth calculation

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L15659 | __init__(self: depthai.PointCloudConfig) -> None |

**🔹 Public Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getSparse(self) -> bool` | `(self)` | L15661 | getSparse(self: depthai.PointCloudConfig) -> bool |
| `def getTransformationMatrix(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L15669 | getTransformationMatrix(self: depthai.PointCloudConfig) -> Annotated[list[Annotated[list[float], FixedSize(4)]], FixedSize(4)] |
| `def setSparse(self, arg0: bool) -> PointCloudConfig` | `(self, arg0: bool)` | L15677 | setSparse(self: depthai.PointCloudConfig, arg0: bool) -> depthai.PointCloudConfig |
| `@overload` `def setTransformationMatrix(self, arg0) -> PointCloudConfig` | `(self, arg0)` | L15685 | setTransformationMatrix(*args, **kwargs) |
| `@overload` `def setTransformationMatrix(self, arg0) -> PointCloudConfig` | `(self, arg0)` | L15704 | setTransformationMatrix(*args, **kwargs) |

<a id="class-pointclouddata"></a>
### class `PointCloudData(Buffer)`  — L15723

> PointCloudData message. Carries point cloud data.

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L15725 | __init__(self: depthai.PointCloudData) -> None |

**🔹 Public Methods (29):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getHeight(self) -> int` | `(self)` | L15727 | getHeight(self: depthai.PointCloudData) -> int |
| `def getInstanceNum(self) -> int` | `(self)` | L15733 | getInstanceNum(self: depthai.PointCloudData) -> int |
| `def getMaxX(self) -> float` | `(self)` | L15738 | getMaxX(self: depthai.PointCloudData) -> float |
| `def getMaxY(self) -> float` | `(self)` | L15743 | getMaxY(self: depthai.PointCloudData) -> float |
| `def getMaxZ(self) -> float` | `(self)` | L15748 | getMaxZ(self: depthai.PointCloudData) -> float |
| `def getMinX(self) -> float` | `(self)` | L15753 | getMinX(self: depthai.PointCloudData) -> float |
| `def getMinY(self) -> float` | `(self)` | L15758 | getMinY(self: depthai.PointCloudData) -> float |
| `def getMinZ(self) -> float` | `(self)` | L15763 | getMinZ(self: depthai.PointCloudData) -> float |
| `def getPoints(self) -> numpy.ndarray[numpy.float32]` | `(self)` | L15768 | getPoints(self: object) -> numpy.ndarray[numpy.float32] |
| `def getPointsRGB(self) -> tuple` | `(self)` | L15770 | getPointsRGB(self: object) -> tuple |
| `def getSequenceNum(self) -> int` | `(self)` | L15772 | getSequenceNum(self: depthai.PointCloudData) -> int |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L15777 | getTimestamp(self: depthai.PointCloudData) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L15782 | getTimestampDevice(self: depthai.PointCloudData) -> datetime.timedelta |
| `def getWidth(self) -> int` | `(self)` | L15788 | getWidth(self: depthai.PointCloudData) -> int |
| `def isColor(self) -> bool` | `(self)` | L15794 | isColor(self: depthai.PointCloudData) -> bool |
| `def isSparse(self) -> bool` | `(self)` | L15799 | isSparse(self: depthai.PointCloudData) -> bool |
| `def setHeight(self, arg0: int) -> PointCloudData` | `(self, arg0: int)` | L15804 | setHeight(self: depthai.PointCloudData, arg0: int) -> depthai.PointCloudData |
| `def setInstanceNum(self, arg0: int) -> PointCloudData` | `(self, arg0: int)` | L15812 | setInstanceNum(self: depthai.PointCloudData, arg0: int) -> depthai.PointCloudData |
| `def setMaxX(self, arg0: float) -> PointCloudData` | `(self, arg0: float)` | L15820 | setMaxX(self: depthai.PointCloudData, arg0: float) -> depthai.PointCloudData |
| `def setMaxY(self, arg0: float) -> PointCloudData` | `(self, arg0: float)` | L15828 | setMaxY(self: depthai.PointCloudData, arg0: float) -> depthai.PointCloudData |
| `def setMaxZ(self, arg0: float) -> PointCloudData` | `(self, arg0: float)` | L15836 | setMaxZ(self: depthai.PointCloudData, arg0: float) -> depthai.PointCloudData |
| `def setMinX(self, arg0: float) -> PointCloudData` | `(self, arg0: float)` | L15844 | setMinX(self: depthai.PointCloudData, arg0: float) -> depthai.PointCloudData |
| `def setMinY(self, arg0: float) -> PointCloudData` | `(self, arg0: float)` | L15852 | setMinY(self: depthai.PointCloudData, arg0: float) -> depthai.PointCloudData |
| `def setMinZ(self, arg0: float) -> PointCloudData` | `(self, arg0: float)` | L15860 | setMinZ(self: depthai.PointCloudData, arg0: float) -> depthai.PointCloudData |
| `def setPoints(self, arg0: numpy.ndarray[numpy.float32]) -> None` | `(self, arg0: numpy.ndarray[numpy.float32])` | L15868 | setPoints(self: object, arg0: numpy.ndarray[numpy.float32]) -> None |
| `def setPointsRGB(self, arg0: numpy.ndarray[numpy.float32], arg1: numpy.ndarray[numpy.uint8]) -> None` | `(self, arg0: numpy.ndarray[numpy.float32], arg1: numpy.ndarray[numpy.uint8])` | L15870 | setPointsRGB(self: object, arg0: numpy.ndarray[numpy.float32], arg1: numpy.ndarray[numpy.uint8]) -> None |
| `@overload` `def setSize(self, width: int, height: int) -> PointCloudData` | `(self, width: int, height: int)` | L15873 | setSize(*args, **kwargs) |
| `@overload` `def setSize(self, size: tuple[int, int]) -> PointCloudData` | `(self, size: tuple[int, int])` | L15895 | setSize(*args, **kwargs) |
| `def setWidth(self, arg0: int) -> PointCloudData` | `(self, arg0: int)` | L15916 | setWidth(self: depthai.PointCloudData, arg0: int) -> depthai.PointCloudData |

<a id="class-pointcloudproperties"></a>
### class `PointCloudProperties`  — L15925

> Specify properties for PointCloud

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `initialConfig` | `PointCloudConfig` | — | L15927 |
| `numFramesPool` | `int` | — | L15928 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L15929 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-pointsannotation"></a>
### class `PointsAnnotation`  — L15932

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `fillColor` | `Color` | — | L15933 |
| `outlineColor` | `Color` | — | L15934 |
| `outlineColors` | `VectorColor` | — | L15935 |
| `points` | `VectorPoint2f` | — | L15936 |
| `thickness` | `float` | — | L15937 |
| `type` | `PointsAnnotationType` | — | L15938 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L15939 | __init__(self: depthai.PointsAnnotation) -> None |

<a id="class-pointsannotationtype"></a>
### class `PointsAnnotationType`  — L15942

> Members:

  UNKNOWN

  POINTS

  LINE_LOOP

  LINE_STRIP

  LINE_LIST

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L15956 |
| `LINE_LIST` | `ClassVar[PointsAnnotationType]` | `...` | L15957 |
| `LINE_LOOP` | `ClassVar[PointsAnnotationType]` | `...` | L15958 |
| `LINE_STRIP` | `ClassVar[PointsAnnotationType]` | `...` | L15959 |
| `POINTS` | `ClassVar[PointsAnnotationType]` | `...` | L15960 |
| `UNKNOWN` | `ClassVar[PointsAnnotationType]` | `...` | L15961 |
| `__entries` | `ClassVar[dict]` | `...` | L15962 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L15963 | __init__(self: depthai.PointsAnnotationType, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L15965 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L15967 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L15969 | __index__(self: depthai.PointsAnnotationType) -> int |
| `def __int__(self) -> int` | `(self)` | L15971 | __int__(self: depthai.PointsAnnotationType) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L15973 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L15976 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L15982 | (arg0: depthai.PointsAnnotationType) -> int |

<a id="class-processortype"></a>
### class `ProcessorType`  — L15985

> Members:

LEON_CSS

LEON_MSS

CPU

DSP

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L15995 |
| `CPU` | `ClassVar[ProcessorType]` | `...` | L15996 |
| `DSP` | `ClassVar[ProcessorType]` | `...` | L15997 |
| `LEON_CSS` | `ClassVar[ProcessorType]` | `...` | L15998 |
| `LEON_MSS` | `ClassVar[ProcessorType]` | `...` | L15999 |
| `__entries` | `ClassVar[dict]` | `...` | L16000 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L16001 | __init__(self: depthai.ProcessorType, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L16003 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L16005 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L16007 | __index__(self: depthai.ProcessorType) -> int |
| `def __int__(self) -> int` | `(self)` | L16009 | __int__(self: depthai.ProcessorType) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L16011 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L16014 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L16020 | (arg0: depthai.ProcessorType) -> int |

<a id="class-profilingdata"></a>
### class `ProfilingData`  — L16023

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `numBytesRead` | `int` | — | L16024 |
| `numBytesWritten` | `int` | — | L16025 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L16026 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-properties"></a>
### class `Properties`  — L16029

> Base Properties structure

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L16031 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-quaterniond"></a>
### class `Quaterniond`  — L16034

> Quaterniond structure

qx,qy,qz,qw coordinates that define a 3D point orientation.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `qw` | `float` | — | L16038 |
| `qx` | `float` | — | L16039 |
| `qy` | `float` | — | L16040 |
| `qz` | `float` | — | L16041 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L16043 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: float, arg1: float, arg2: float, arg3: float) -> None` | `(self, arg0: float, arg1: float, arg2: float, arg3: float)` | L16052 | __init__(*args, **kwargs) |

<a id="class-rgbddata"></a>
### class `RGBDData(Buffer)`  — L16061

> RGBD message. Carries RGB and Depth frames.

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L16063 | __init__(self: depthai.RGBDData) -> None |

**🔹 Public Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getDepthFrame(self) -> ImgFrame` | `(self)` | L16065 | getDepthFrame(self: depthai.RGBDData) -> depthai.ImgFrame |
| `def getRGBFrame(self) -> ImgFrame` | `(self)` | L16067 | getRGBFrame(self: depthai.RGBDData) -> depthai.ImgFrame |
| `def setDepthFrame(self, frame: ImgFrame) -> None` | `(self, frame: ImgFrame)` | L16069 | setDepthFrame(self: depthai.RGBDData, frame: depthai.ImgFrame) -> None |
| `def setRGBFrame(self, frame: ImgFrame) -> None` | `(self, frame: ImgFrame)` | L16071 | setRGBFrame(self: depthai.RGBDData, frame: depthai.ImgFrame) -> None |

<a id="class-recordconfig"></a>
### class `RecordConfig`  — L16074

> Configuration for recording and replaying messages

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `compressionLevel` | `Incomplete` | — | L16085 |
| `outputDir` | `os.PathLike` | — | L16086 |
| `videoEncoding` | `RecordConfig.VideoEncoding` | — | L16087 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L16088 | __init__(self: depthai.RecordConfig) -> None |

**Nested Class:**

<a id="class-videoencoding"></a>
#### class `VideoEncoding`  — L16077

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `bitrate` | `int` | — | L16078 |
| `enabled` | `bool` | — | L16079 |
| `lossless` | `bool` | — | L16080 |
| `profile` | `VideoEncoderProperties.Profile` | — | L16081 |
| `quality` | `int` | — | L16082 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L16083 | __init__(self: depthai.RecordConfig.VideoEncoding) -> None |

<a id="class-rect"></a>
### class `Rect`  — L16091

> Rect structure

x,y coordinates together with width and height that define a rectangle. Can be
either normalized [0,1] or absolute representation.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `height` | `float` | — | L16096 |
| `width` | `float` | — | L16097 |
| `x` | `float` | — | L16098 |
| `y` | `float` | — | L16099 |

**🔧 Dunder Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L16101 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: float, arg1: float, arg2: float, arg3: float) -> None` | `(self, arg0: float, arg1: float, arg2: float, arg3: float)` | L16120 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: float, arg1: float, arg2: float, arg3: float, arg4: bool) -> None` | `(self, arg0: float, arg1: float, arg2: float, arg3: float, arg4: bool)` | L16139 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: Point2f, arg1: Point2f) -> None` | `(self, arg0: Point2f, arg1: Point2f)` | L16158 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: Point2f, arg1: Point2f, arg2: bool) -> None` | `(self, arg0: Point2f, arg1: Point2f, arg2: bool)` | L16177 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: Point2f, arg1: Size2f) -> None` | `(self, arg0: Point2f, arg1: Size2f)` | L16196 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: Point2f, arg1: Size2f, arg2: bool) -> None` | `(self, arg0: Point2f, arg1: Size2f, arg2: bool)` | L16215 | __init__(*args, **kwargs) |

**🔹 Public Methods (9):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def area(self) -> float` | `(self)` | L16233 | area(self: depthai.Rect) -> float |
| `def bottomRight(self) -> Point2f` | `(self)` | L16238 | bottomRight(self: depthai.Rect) -> depthai.Point2f |
| `def contains(self, arg0: Point2f) -> bool` | `(self, arg0: Point2f)` | L16243 | contains(self: depthai.Rect, arg0: depthai.Point2f) -> bool |
| `def denormalize(self, width: int, height: int) -> Rect` | `(self, width: int, height: int)` | L16248 | denormalize(self: depthai.Rect, width: int, height: int) -> depthai.Rect |
| `def empty(self) -> bool` | `(self)` | L16259 | empty(self: depthai.Rect) -> bool |
| `def isNormalized(self) -> bool` | `(self)` | L16264 | isNormalized(self: depthai.Rect) -> bool |
| `def normalize(self, width: int, height: int) -> Rect` | `(self, width: int, height: int)` | L16269 | normalize(self: depthai.Rect, width: int, height: int) -> depthai.Rect |
| `def size(self) -> Size2f` | `(self)` | L16280 | size(self: depthai.Rect) -> depthai.Size2f |
| `def topLeft(self) -> Point2f` | `(self)` | L16285 | topLeft(self: depthai.Rect) -> depthai.Point2f |

<a id="class-rectificationproperties"></a>
### class `RectificationProperties`  — L16291

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `outputHeight` | `int | None` | — | L16292 |
| `outputWidth` | `int | None` | — | L16293 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L16294 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-remoteconnection"></a>
### class `RemoteConnection`  — L16297

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, address: str = ..., webSocketPort: int = ..., serveFrontend: bool = ..., httpPort: int = ...) -> None` | `(self, address: str = ..., webSocketPort: int = ..., serveFrontend: bool = ..., httpPort: int = ...)` | L16298 | __init__(self: depthai.RemoteConnection, address: str = '0.0.0.0', webSocketPort: int = 8765, serveFrontend: bool = True, httpPort: int = 8082) -> None |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def addTopic(self, topicName: str, output: Node.Output, group: str = ..., useVisualizationIfAvailable: bool = ...) -> None` | `(self, topicName: str, output: Node.Output, group: str = ..., useVisualizationIfAvailable: bool = ...)` | L16316 | addTopic(*args, **kwargs) |
| `@overload` `def addTopic(self, topicName: str, group: str = ..., maxSize: int = ..., blocking: bool = ..., useVisualizationIfAvailable: bool = ...) -> MessageQueue` | `(self, topicName: str, group: str = ..., maxSize: int = ..., blocking: bool = ..., useVisualizationIfAvailable: bool = ...)` | L16355 | addTopic(*args, **kwargs) |
| `def registerBinaryService(self, serviceName: str, callback: object) -> None` | `(self, serviceName: str, callback: object)` | L16393 | registerBinaryService(self: depthai.RemoteConnection, serviceName: str, callback: object) -> None |
| `def registerPipeline(self, pipeline: Pipeline) -> None` | `(self, pipeline: Pipeline)` | L16404 | registerPipeline(self: depthai.RemoteConnection, pipeline: depthai.Pipeline) -> None |
| `def registerService(self, serviceName: str, callback: Callable[[json], json]) -> None` | `(self, serviceName: str, callback: Callable[[json], json])` | L16412 | registerService(self: depthai.RemoteConnection, serviceName: str, callback: Callable[[json], json]) -> None |
| `def removeTopic(self, topicName: str) -> bool` | `(self, topicName: str)` | L16423 | removeTopic(self: depthai.RemoteConnection, topicName: str) -> bool |
| `def waitKey(self, delay: int) -> int` | `(self, delay: int)` | L16436 | waitKey(self: depthai.RemoteConnection, delay: int) -> int |

<a id="class-rotatedrect"></a>
### class `RotatedRect`  — L16448

> RotatedRect structure

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `angle` | `float` | — | L16450 |
| `center` | `Point2f` | — | L16451 |
| `size` | `Size2f` | — | L16452 |

**🔧 Dunder Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L16454 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: Point2f, arg1: Size2f, arg2: float) -> None` | `(self, arg0: Point2f, arg1: Size2f, arg2: float)` | L16465 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: Rect, arg1: float) -> None` | `(self, arg0: Rect, arg1: float)` | L16476 | __init__(*args, **kwargs) |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def denormalize(self, width: int, height: int, force: bool = ...) -> RotatedRect` | `(self, width: int, height: int, force: bool = ...)` | L16486 | denormalize(self: depthai.RotatedRect, width: int, height: int, force: bool = False) -> depthai.RotatedRect |
| `def getOuterCXCYWH(self) -> tuple[Point2f, Size2f]` | `(self)` | L16495 | getOuterCXCYWH(self: depthai.RotatedRect) -> tuple[depthai.Point2f, depthai.Size2f] |
| `def getOuterRect(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L16504 | getOuterRect(self: depthai.RotatedRect) -> Annotated[list[float], FixedSize(4)] |
| `def getOuterXYWH(self) -> tuple[Point2f, Size2f]` | `(self)` | L16512 | getOuterXYWH(self: depthai.RotatedRect) -> tuple[depthai.Point2f, depthai.Size2f] |
| `def getPoints(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L16521 | getPoints(self: depthai.RotatedRect) -> Annotated[list[depthai.Point2f], FixedSize(4)] |
| `def isNormalized(self) -> bool` | `(self)` | L16529 | isNormalized(self: depthai.RotatedRect) -> bool |
| `def normalize(self, width: int, height: int) -> RotatedRect` | `(self, width: int, height: int)` | L16531 | normalize(self: depthai.RotatedRect, width: int, height: int) -> depthai.RotatedRect |

<a id="class-spiinproperties"></a>
### class `SPIInProperties`  — L16541

> Properties for SPIIn node

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `busId` | `int` | — | L16543 |
| `maxDataSize` | `int` | — | L16544 |
| `numFrames` | `int` | — | L16545 |
| `streamName` | `str` | — | L16546 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L16547 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-spioutproperties"></a>
### class `SPIOutProperties`  — L16550

> Specify properties for SPIOut node

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `busId` | `int` | — | L16552 |
| `streamName` | `str` | — | L16553 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L16554 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-scriptproperties"></a>
### class `ScriptProperties`  — L16557

> Specify ScriptProperties options such as script uri, script name, ...

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `processor` | `ProcessorType` | — | L16559 |
| `scriptName` | `str` | — | L16560 |
| `scriptUri` | `str` | — | L16561 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L16562 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-serializationtype"></a>
### class `SerializationType`  — L16565

> Members:

LIBNOP

JSON

JSON_MSGPACK

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L16573 |
| `JSON` | `ClassVar[SerializationType]` | `...` | L16574 |
| `JSON_MSGPACK` | `ClassVar[SerializationType]` | `...` | L16575 |
| `LIBNOP` | `ClassVar[SerializationType]` | `...` | L16576 |
| `__entries` | `ClassVar[dict]` | `...` | L16577 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L16578 | __init__(self: depthai.SerializationType, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L16580 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L16582 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L16584 | __index__(self: depthai.SerializationType) -> int |
| `def __int__(self) -> int` | `(self)` | L16586 | __int__(self: depthai.SerializationType) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L16588 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L16591 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L16597 | (arg0: depthai.SerializationType) -> int |

<a id="class-size2f"></a>
### class `Size2f`  — L16600

> Size2f structure

width, height values define the size of the shape/frame

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `height` | `float` | — | L16604 |
| `width` | `float` | — | L16605 |

**🔧 Dunder Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L16607 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, width: float, height: float) -> None` | `(self, width: float, height: float)` | L16618 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, width: float, height: float, normalized: bool) -> None` | `(self, width: float, height: float, normalized: bool)` | L16629 | __init__(*args, **kwargs) |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def isNormalized(self) -> bool` | `(self)` | L16639 | isNormalized(self: depthai.Size2f) -> bool |

<a id="class-slugcomponents"></a>
### class `SlugComponents`  — L16642

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `modelRef` | `str` | — | L16643 |
| `modelSlug` | `str` | — | L16644 |
| `modelVariantSlug` | `str` | — | L16645 |
| `teamName` | `str` | — | L16646 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L16648 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, teamName: str = ..., modelSlug: str = ..., modelVariantSlug: str = ..., modelRef: str = ...) -> None` | `(self, teamName: str = ..., modelSlug: str = ..., modelVariantSlug: str = ..., modelRef: str = ...)` | L16657 | __init__(*args, **kwargs) |

**⚡ Static Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@staticmethod` `def split(slug: str) -> SlugComponents` | `(slug: str)` | L16668 | split(slug: str) -> depthai.SlugComponents |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def merge(self) -> str` | `(self)` | L16665 | merge(self: depthai.SlugComponents) -> str |

<a id="class-spatialdetectionnetworkproperties"></a>
### class `SpatialDetectionNetworkProperties`  — L16671

> Specify properties for SpatialDetectionNetwork

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `depthThresholds` | `SpatialLocationCalculatorConfigThresholds` | — | L16673 |
| `detectedBBScaleFactor` | `float` | — | L16674 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L16675 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-spatialimgdetection"></a>
### class `SpatialImgDetection(ImgDetection)`  — L16678

> SpatialImgDetection structure

Contains image detection results together with spatial location data.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `boundingBoxMapping` | `SpatialLocationCalculatorConfigData` | — | L16682 |
| `spatialCoordinates` | `Point3f` | — | L16683 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L16684 | __init__(self: depthai.SpatialImgDetection) -> None |

<a id="class-spatialimgdetections"></a>
### class `SpatialImgDetections(Buffer)`  — L16687

> SpatialImgDetections message. Carries detection results together with spatial
location data

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `detections` | `list[SpatialImgDetection]` | — | L16690 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L16691 | __init__(self: depthai.SpatialImgDetections) -> None |

**🔹 Public Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getSequenceNum(self) -> int` | `(self)` | L16693 | getSequenceNum(self: depthai.SpatialImgDetections) -> int |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L16698 | getTimestamp(self: depthai.SpatialImgDetections) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L16703 | getTimestampDevice(self: depthai.SpatialImgDetections) -> datetime.timedelta |
| `def getTransformation(self) -> ImgTransformation | None` | `(self)` | L16709 | getTransformation(self: depthai.SpatialImgDetections) -> Optional[depthai.ImgTransformation] |
| `def setTransformation(self, arg0: ImgTransformation | None) -> None` | `(self, arg0: ImgTransformation | None)` | L16711 | setTransformation(self: depthai.SpatialImgDetections, arg0: Optional[depthai.ImgTransformation]) -> None |

<a id="class-spatiallocationcalculatoralgorithm"></a>
### class `SpatialLocationCalculatorAlgorithm`  — L16714

> SpatialLocationCalculatorAlgorithm configuration modes

Contains calculation method used to obtain spatial locations.

Members:

  AVERAGE

  MEAN

  MIN

  MAX

  MODE

  MEDIAN

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L16732 |
| `AVERAGE` | `ClassVar[SpatialLocationCalculatorAlgorithm]` | `...` | L16733 |
| `MAX` | `ClassVar[SpatialLocationCalculatorAlgorithm]` | `...` | L16734 |
| `MEAN` | `ClassVar[SpatialLocationCalculatorAlgorithm]` | `...` | L16735 |
| `MEDIAN` | `ClassVar[SpatialLocationCalculatorAlgorithm]` | `...` | L16736 |
| `MIN` | `ClassVar[SpatialLocationCalculatorAlgorithm]` | `...` | L16737 |
| `MODE` | `ClassVar[SpatialLocationCalculatorAlgorithm]` | `...` | L16738 |
| `__entries` | `ClassVar[dict]` | `...` | L16739 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L16740 | __init__(self: depthai.SpatialLocationCalculatorAlgorithm, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L16742 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L16744 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L16746 | __index__(self: depthai.SpatialLocationCalculatorAlgorithm) -> int |
| `def __int__(self) -> int` | `(self)` | L16748 | __int__(self: depthai.SpatialLocationCalculatorAlgorithm) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L16750 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L16753 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L16759 | (arg0: depthai.SpatialLocationCalculatorAlgorithm) -> int |

<a id="class-spatiallocationcalculatorconfig"></a>
### class `SpatialLocationCalculatorConfig(Buffer)`  — L16762

> SpatialLocationCalculatorConfig message. Carries ROI (region of interest) and
threshold for depth calculation

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L16765 | __init__(self: depthai.SpatialLocationCalculatorConfig) -> None |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def addROI(self, ROI: SpatialLocationCalculatorConfigData) -> None` | `(self, ROI: SpatialLocationCalculatorConfigData)` | L16767 | addROI(self: depthai.SpatialLocationCalculatorConfig, ROI: depthai.SpatialLocationCalculatorConfigData) -> None |
| `def getConfigData(self) -> list[SpatialLocationCalculatorConfigData]` | `(self)` | L16775 | getConfigData(self: depthai.SpatialLocationCalculatorConfig) -> list[depthai.SpatialLocationCalculatorConfigData] |
| `def setROIs(self, ROIs: list[SpatialLocationCalculatorConfigData]) -> None` | `(self, ROIs: list[SpatialLocationCalculatorConfigData])` | L16783 | setROIs(self: depthai.SpatialLocationCalculatorConfig, ROIs: list[depthai.SpatialLocationCalculatorConfigData]) -> None |

<a id="class-spatiallocationcalculatorconfigdata"></a>
### class `SpatialLocationCalculatorConfigData`  — L16792

> SpatialLocation configuration data structure

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `calculationAlgorithm` | `SpatialLocationCalculatorAlgorithm` | — | L16794 |
| `depthThresholds` | `SpatialLocationCalculatorConfigThresholds` | — | L16795 |
| `roi` | `Rect` | — | L16796 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L16797 | __init__(self: depthai.SpatialLocationCalculatorConfigData) -> None |

<a id="class-spatiallocationcalculatorconfigthresholds"></a>
### class `SpatialLocationCalculatorConfigThresholds`  — L16800

> SpatialLocation configuration thresholds structure

Contains configuration data for lower and upper threshold in depth units
(millimeter by default) for ROI. Values outside of threshold range will be
ignored when calculating spatial coordinates from depth map.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `lowerThreshold` | `int` | — | L16806 |
| `upperThreshold` | `int` | — | L16807 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L16808 | __init__(self: depthai.SpatialLocationCalculatorConfigThresholds) -> None |

<a id="class-spatiallocationcalculatordata"></a>
### class `SpatialLocationCalculatorData(Buffer)`  — L16811

> SpatialLocationCalculatorData message. Carries spatial information (X,Y,Z) and
their configuration parameters

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `spatialLocations` | `list[SpatialLocations]` | — | L16814 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L16815 | __init__(self: depthai.SpatialLocationCalculatorData) -> None |

**🔹 Public Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getSequenceNum(self) -> int` | `(self)` | L16817 | getSequenceNum(self: depthai.SpatialLocationCalculatorData) -> int |
| `def getSpatialLocations(self) -> list[SpatialLocations]` | `(self)` | L16822 | getSpatialLocations(self: depthai.SpatialLocationCalculatorData) -> list[depthai.SpatialLocations] |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L16830 | getTimestamp(self: depthai.SpatialLocationCalculatorData) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L16835 | getTimestampDevice(self: depthai.SpatialLocationCalculatorData) -> datetime.timedelta |

<a id="class-spatiallocationcalculatorproperties"></a>
### class `SpatialLocationCalculatorProperties`  — L16842

> Specify properties for SpatialLocationCalculator

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `roiConfig` | `SpatialLocationCalculatorConfig` | — | L16844 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L16845 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-spatiallocations"></a>
### class `SpatialLocations`  — L16848

> SpatialLocations structure

Contains configuration data, average depth for the calculated ROI on depth map.
Together with spatial coordinates: x,y,z relative to the center of depth map.
Units are in depth units (millimeter by default).

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `config` | `SpatialLocationCalculatorConfigData` | — | L16854 |
| `depthAverage` | `float` | — | L16855 |
| `depthAveragePixelCount` | `int` | — | L16856 |
| `depthMax` | `int` | — | L16857 |
| `depthMedian` | `float` | — | L16858 |
| `depthMin` | `int` | — | L16859 |
| `depthMode` | `float` | — | L16860 |
| `spatialCoordinates` | `Point3f` | — | L16861 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L16862 | __init__(self: depthai.SpatialLocations) -> None |

<a id="class-stereodepthconfig"></a>
### class `StereoDepthConfig(Buffer)`  — L16865

> StereoDepthConfig message.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `MedianFilter` | `ClassVar[type[filters.params.MedianFilter]]` | `...` | L17283 |
| `algorithmControl` | `StereoDepthConfig.AlgorithmControl` | — | L17284 |
| `censusTransform` | `StereoDepthConfig.CensusTransform` | — | L17285 |
| `confidenceMetrics` | `StereoDepthConfig.ConfidenceMetrics` | — | L17286 |
| `costAggregation` | `StereoDepthConfig.CostAggregation` | — | L17287 |
| `costMatching` | `StereoDepthConfig.CostMatching` | — | L17288 |
| `postProcessing` | `StereoDepthConfig.PostProcessing` | — | L17289 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L17291 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self) -> None` | `(self)` | L17300 | __init__(*args, **kwargs) |

**🔹 Public Methods (26):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getBilateralFilterSigma(self) -> int` | `(self)` | L17308 | getBilateralFilterSigma(self: depthai.StereoDepthConfig) -> int |
| `def getConfidenceThreshold(self) -> int` | `(self)` | L17313 | getConfidenceThreshold(self: depthai.StereoDepthConfig) -> int |
| `def getCustomDepthUnitMultiplier(self) -> float` | `(self)` | L17318 | getCustomDepthUnitMultiplier(self: depthai.StereoDepthConfig) -> float |
| `def getDepthUnit(self) -> DepthUnit` | `(self)` | L17323 | getDepthUnit(self: depthai.StereoDepthConfig) -> depthai.DepthUnit |
| `def getExtendedDisparity(self) -> bool` | `(self)` | L17328 | getExtendedDisparity(self: depthai.StereoDepthConfig) -> bool |
| `def getFiltersComputeBackend(self) -> ProcessorType` | `(self)` | L17333 | getFiltersComputeBackend(self: depthai.StereoDepthConfig) -> depthai.ProcessorType |
| `def getLeftRightCheck(self) -> bool` | `(self)` | L17338 | getLeftRightCheck(self: depthai.StereoDepthConfig) -> bool |
| `def getLeftRightCheckThreshold(self) -> int` | `(self)` | L17343 | getLeftRightCheckThreshold(self: depthai.StereoDepthConfig) -> int |
| `def getMaxDisparity(self) -> float` | `(self)` | L17348 | getMaxDisparity(self: depthai.StereoDepthConfig) -> float |
| `def getMedianFilter(self) -> filters.params.MedianFilter` | `(self)` | L17356 | getMedianFilter(self: depthai.StereoDepthConfig) -> depthai.filters.params.MedianFilter |
| `def getSubpixel(self) -> bool` | `(self)` | L17361 | getSubpixel(self: depthai.StereoDepthConfig) -> bool |
| `def getSubpixelFractionalBits(self) -> int` | `(self)` | L17366 | getSubpixelFractionalBits(self: depthai.StereoDepthConfig) -> int |
| `def setBilateralFilterSigma(self, sigma: int) -> StereoDepthConfig` | `(self, sigma: int)` | L17371 | setBilateralFilterSigma(self: depthai.StereoDepthConfig, sigma: int) -> depthai.StereoDepthConfig |
| `def setConfidenceThreshold(self, confThr: int) -> StereoDepthConfig` | `(self, confThr: int)` | L17381 | setConfidenceThreshold(self: depthai.StereoDepthConfig, confThr: int) -> depthai.StereoDepthConfig |
| `def setCustomDepthUnitMultiplier(self, arg0: float) -> StereoDepthConfig` | `(self, arg0: float)` | L17389 | setCustomDepthUnitMultiplier(self: depthai.StereoDepthConfig, arg0: float) -> depthai.StereoDepthConfig |
| `def setDepthAlign(self, align: StereoDepthConfig.AlgorithmControl.DepthAlign) -> StereoDepthConfig` | `(self, align: StereoDepthConfig.AlgorithmControl.DepthAlign)` | L17394 | setDepthAlign(self: depthai.StereoDepthConfig, align: depthai.StereoDepthConfig.AlgorithmControl.DepthAlign) -> depthai.StereoDepthConfig |
| `def setDepthUnit(self, arg0: DepthUnit) -> StereoDepthConfig` | `(self, arg0: DepthUnit)` | L17401 | setDepthUnit(self: depthai.StereoDepthConfig, arg0: depthai.DepthUnit) -> depthai.StereoDepthConfig |
| `def setDisparityShift(self, arg0: int) -> StereoDepthConfig` | `(self, arg0: int)` | L17408 | setDisparityShift(self: depthai.StereoDepthConfig, arg0: int) -> depthai.StereoDepthConfig |
| `def setExtendedDisparity(self, enable: bool) -> StereoDepthConfig` | `(self, enable: bool)` | L17418 | setExtendedDisparity(self: depthai.StereoDepthConfig, enable: bool) -> depthai.StereoDepthConfig |
| `def setFiltersComputeBackend(self, filtersBackend: ProcessorType) -> StereoDepthConfig` | `(self, filtersBackend: ProcessorType)` | L17424 | setFiltersComputeBackend(self: depthai.StereoDepthConfig, filtersBackend: depthai.ProcessorType) -> depthai.StereoDepthConfig |
| `def setLeftRightCheck(self, enable: bool) -> StereoDepthConfig` | `(self, enable: bool)` | L17429 | setLeftRightCheck(self: depthai.StereoDepthConfig, enable: bool) -> depthai.StereoDepthConfig |
| `def setLeftRightCheckThreshold(self, sigma: int) -> StereoDepthConfig` | `(self, sigma: int)` | L17437 | setLeftRightCheckThreshold(self: depthai.StereoDepthConfig, sigma: int) -> depthai.StereoDepthConfig |
| `def setMedianFilter(self, median: filters.params.MedianFilter) -> StereoDepthConfig` | `(self, median: filters.params.MedianFilter)` | L17443 | setMedianFilter(self: depthai.StereoDepthConfig, median: depthai.filters.params.MedianFilter) -> depthai.StereoDepthConfig |
| `def setNumInvalidateEdgePixels(self, arg0: int) -> StereoDepthConfig` | `(self, arg0: int)` | L17449 | setNumInvalidateEdgePixels(self: depthai.StereoDepthConfig, arg0: int) -> depthai.StereoDepthConfig |
| `def setSubpixel(self, enable: bool) -> StereoDepthConfig` | `(self, enable: bool)` | L17456 | setSubpixel(self: depthai.StereoDepthConfig, enable: bool) -> depthai.StereoDepthConfig |
| `def setSubpixelFractionalBits(self, subpixelFractionalBits: int) -> StereoDepthConfig` | `(self, subpixelFractionalBits: int)` | L17463 | setSubpixelFractionalBits(self: depthai.StereoDepthConfig, subpixelFractionalBits: int) -> depthai.StereoDepthConfig |

**Nested Class:**

<a id="class-algorithmcontrol"></a>
#### class `AlgorithmControl`  — L16868

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `centerAlignmentShiftFactor` | `float | None` | — | L16951 |
| `customDepthUnitMultiplier` | `float` | — | L16952 |
| `depthAlign` | `StereoDepthConfig.AlgorithmControl.DepthAlign` | — | L16953 |
| `depthUnit` | `DepthUnit` | — | L16954 |
| `disparityShift` | `int` | — | L16955 |
| `enableExtended` | `bool` | — | L16956 |
| `enableLeftRightCheck` | `bool` | — | L16957 |
| `enableSubpixel` | `bool` | — | L16958 |
| `enableSwLeftRightCheck` | `bool` | — | L16959 |
| `leftRightCheckThreshold` | `int` | — | L16960 |
| `numInvalidateEdgePixels` | `int` | — | L16961 |
| `subpixelFractionalBits` | `int` | — | L16962 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L16963 | __init__(self: depthai.StereoDepthConfig.AlgorithmControl) -> None |

**Nested Class:**

<a id="class-depthalign"></a>
##### class `DepthAlign`  — L16869

> Align the disparity/depth to the perspective of a rectified output, or center it

Members:

  RECTIFIED_RIGHT : 

  RECTIFIED_LEFT : 

  CENTER : 

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L16879 |
| `CENTER` | `ClassVar[StereoDepthConfig.AlgorithmControl.DepthAlign]` | `...` | L16880 |
| `RECTIFIED_LEFT` | `ClassVar[StereoDepthConfig.AlgorithmControl.DepthAlign]` | `...` | L16881 |
| `RECTIFIED_RIGHT` | `ClassVar[StereoDepthConfig.AlgorithmControl.DepthAlign]` | `...` | L16882 |
| `__entries` | `ClassVar[dict]` | `...` | L16883 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L16884 | __init__(self: depthai.StereoDepthConfig.AlgorithmControl.DepthAlign, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L16886 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L16888 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L16890 | __index__(self: depthai.StereoDepthConfig.AlgorithmControl.DepthAlign) -> int |
| `def __int__(self) -> int` | `(self)` | L16892 | __int__(self: depthai.StereoDepthConfig.AlgorithmControl.DepthAlign) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L16894 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L16897 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L16903 | (arg0: depthai.StereoDepthConfig.AlgorithmControl.DepthAlign) -> int |

**Nested Class:**

<a id="class-depthunit"></a>
##### class `DepthUnit`  — L16906

> Measurement unit for depth data

Members:

  METER

  CENTIMETER

  MILLIMETER

  INCH

  FOOT

  CUSTOM

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L16922 |
| `CENTIMETER` | `ClassVar[DepthUnit]` | `...` | L16923 |
| `CUSTOM` | `ClassVar[DepthUnit]` | `...` | L16924 |
| `FOOT` | `ClassVar[DepthUnit]` | `...` | L16925 |
| `INCH` | `ClassVar[DepthUnit]` | `...` | L16926 |
| `METER` | `ClassVar[DepthUnit]` | `...` | L16927 |
| `MILLIMETER` | `ClassVar[DepthUnit]` | `...` | L16928 |
| `__entries` | `ClassVar[dict]` | `...` | L16929 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L16930 | __init__(self: depthai.DepthUnit, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L16932 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L16934 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L16936 | __index__(self: depthai.DepthUnit) -> int |
| `def __int__(self) -> int` | `(self)` | L16938 | __int__(self: depthai.DepthUnit) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L16940 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L16943 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L16949 | (arg0: depthai.DepthUnit) -> int |

**Nested Class:**

<a id="class-censustransform"></a>
#### class `CensusTransform`  — L16966

> The basic cost function used by the Stereo Accelerator for matching the left and
right images is the Census Transform. It works on a block of pixels and computes
a bit vector which represents the structure of the image in that block. There
are two types of Census Transform based on how the middle pixel is used: Classic
Approach and Modified Census. The comparisons that are made between pixels can
be or not thresholded. In some cases a mask can be applied to filter out only
specific bits from the entire bit stream. All these approaches are: Classic
Approach: Uses middle pixel to compare against all its neighbors over a defined
window. Each comparison results in a new bit, that is 0 if central pixel is
smaller, or 1 if is it bigger than its neighbor. Modified Census Transform: same
as classic Census Transform, but instead of comparing central pixel with its
neighbors, the window mean will be compared with each pixel over the window.
Thresholding Census Transform: same as classic Census Transform, but it is not
enough that a neighbor pixel to be bigger than the central pixel, it must be
significant bigger (based on a threshold). Census Transform with Mask: same as

classic Census Transform, but in this case not all of the pixel from the support
window are part of the binary descriptor. We use a ma sk “M” to define which
pixels are part of the binary descriptor (1), and which pixels should be skipped
(0).

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `enableMeanMode` | `bool` | — | L17027 |
| `kernelMask` | `int` | — | L17028 |
| `kernelSize` | `StereoDepthConfig.CensusTransform.KernelSize` | — | L17029 |
| `noiseThresholdOffset` | `int` | — | L17030 |
| `noiseThresholdScale` | `int` | — | L17031 |
| `threshold` | `int` | — | L17032 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17033 | __init__(self: depthai.StereoDepthConfig.CensusTransform) -> None |

**Nested Class:**

<a id="class-kernelsize"></a>
##### class `KernelSize`  — L16988

> Census transform kernel size possible values.

Members:

  AUTO : 

  KERNEL_5x5 : 

  KERNEL_7x7 : 

  KERNEL_7x9 : 

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L17000 |
| `AUTO` | `ClassVar[StereoDepthConfig.CensusTransform.KernelSize]` | `...` | L17001 |
| `KERNEL_5x5` | `ClassVar[StereoDepthConfig.CensusTransform.KernelSize]` | `...` | L17002 |
| `KERNEL_7x7` | `ClassVar[StereoDepthConfig.CensusTransform.KernelSize]` | `...` | L17003 |
| `KERNEL_7x9` | `ClassVar[StereoDepthConfig.CensusTransform.KernelSize]` | `...` | L17004 |
| `__entries` | `ClassVar[dict]` | `...` | L17005 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L17006 | __init__(self: depthai.StereoDepthConfig.CensusTransform.KernelSize, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L17008 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L17010 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L17012 | __index__(self: depthai.StereoDepthConfig.CensusTransform.KernelSize) -> int |
| `def __int__(self) -> int` | `(self)` | L17014 | __int__(self: depthai.StereoDepthConfig.CensusTransform.KernelSize) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L17016 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L17019 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L17025 | (arg0: depthai.StereoDepthConfig.CensusTransform.KernelSize) -> int |

**Nested Class:**

<a id="class-confidencemetrics"></a>
#### class `ConfidenceMetrics`  — L17036

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `flatnessConfidenceThreshold` | `int` | — | L17037 |
| `flatnessConfidenceWeight` | `int` | — | L17038 |
| `flatnessOverride` | `bool` | — | L17039 |
| `motionVectorConfidenceThreshold` | `int` | — | L17040 |
| `motionVectorConfidenceWeight` | `int` | — | L17041 |
| `occlusionConfidenceWeight` | `int` | — | L17042 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17043 | __init__(self: depthai.StereoDepthConfig.ConfidenceMetrics) -> None |

**Nested Class:**

<a id="class-costaggregation"></a>
#### class `CostAggregation`  — L17046

> Cost Aggregation is based on Semi Global Block Matching (SGBM). This algorithm
uses a semi global technique to aggregate the cost map. Ultimately the idea is
to build inertia into the stereo algorithm. If a pixel has very little texture
information, then odds are the correct disparity for this pixel is close to that
of the previous pixel considered. This means that we get improved results in
areas with low texture.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `divisionFactor` | `int` | — | L17073 |
| `horizontalPenaltyCostP1` | `int` | — | L17074 |
| `horizontalPenaltyCostP2` | `int` | — | L17075 |
| `p1Config` | `StereoDepthConfig.CostAggregation.P1Config` | — | L17076 |
| `p2Config` | `StereoDepthConfig.CostAggregation.P2Config` | — | L17077 |
| `verticalPenaltyCostP1` | `int` | — | L17078 |
| `verticalPenaltyCostP2` | `int` | — | L17079 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17080 | __init__(self: depthai.StereoDepthConfig.CostAggregation) -> None |

**Nested Class:**

<a id="class-p1config"></a>
##### class `P1Config`  — L17054

> Structure for adaptive P1 penalty configuration.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `defaultValue` | `int` | — | L17056 |
| `edgeThreshold` | `int` | — | L17057 |
| `edgeValue` | `int` | — | L17058 |
| `enableAdaptive` | `bool` | — | L17059 |
| `smoothThreshold` | `int` | — | L17060 |
| `smoothValue` | `int` | — | L17061 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17062 | __init__(self: depthai.StereoDepthConfig.CostAggregation.P1Config) -> None |

**Nested Class:**

<a id="class-p2config"></a>
##### class `P2Config`  — L17065

> Structure for adaptive P2 penalty configuration.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `defaultValue` | `int` | — | L17067 |
| `edgeValue` | `int` | — | L17068 |
| `enableAdaptive` | `bool` | — | L17069 |
| `smoothValue` | `int` | — | L17070 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17071 | __init__(self: depthai.StereoDepthConfig.CostAggregation.P2Config) -> None |

**Nested Class:**

<a id="class-costmatching"></a>
#### class `CostMatching`  — L17083

> The matching cost is way of measuring the similarity of image locations in
stereo correspondence algorithm. Based on the configuration parameters and based
on the descriptor type, a linear equation is applied to computing the cost for
each candidate disparity at each pixel.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `confidenceThreshold` | `int` | — | L17134 |
| `disparityWidth` | `StereoDepthConfig.CostMatching.DisparityWidth` | — | L17135 |
| `enableCompanding` | `bool` | — | L17136 |
| `enableSwConfidenceThresholding` | `bool` | — | L17137 |
| `invalidDisparityValue` | `int` | — | L17138 |
| `linearEquationParameters` | `StereoDepthConfig.CostMatching.LinearEquationParameters` | — | L17139 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17140 | __init__(self: depthai.StereoDepthConfig.CostMatching) -> None |

**Nested Class:**

<a id="class-disparitywidth"></a>
##### class `DisparityWidth`  — L17089

> Disparity search range: 64 or 96 pixels are supported by the HW.

Members:

  DISPARITY_64 : 

  DISPARITY_96 : 

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L17097 |
| `DISPARITY_64` | `ClassVar[StereoDepthConfig.CostMatching.DisparityWidth]` | `...` | L17098 |
| `DISPARITY_96` | `ClassVar[StereoDepthConfig.CostMatching.DisparityWidth]` | `...` | L17099 |
| `__entries` | `ClassVar[dict]` | `...` | L17100 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L17101 | __init__(self: depthai.StereoDepthConfig.CostMatching.DisparityWidth, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L17103 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L17105 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L17107 | __index__(self: depthai.StereoDepthConfig.CostMatching.DisparityWidth) -> int |
| `def __int__(self) -> int` | `(self)` | L17109 | __int__(self: depthai.StereoDepthConfig.CostMatching.DisparityWidth) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L17111 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L17114 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L17120 | (arg0: depthai.StereoDepthConfig.CostMatching.DisparityWidth) -> int |

**Nested Class:**

<a id="class-linearequationparameters"></a>
##### class `LinearEquationParameters`  — L17123

> The linear equation applied for computing the cost is: COMB_COST = α*AD +
β*(CTC<<3). CLAMP(COMB_COST >> 5, threshold). Where AD is the Absolute
Difference between 2 pixels values. CTC is the Census Transform Cost between 2
pixels, based on Hamming distance (xor). The α and β parameters are subject to
fine tuning by the user.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `alpha` | `int` | — | L17129 |
| `beta` | `int` | — | L17130 |
| `threshold` | `int` | — | L17131 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17132 | __init__(self: depthai.StereoDepthConfig.CostMatching.LinearEquationParameters) -> None |

**Nested Class:**

<a id="class-postprocessing"></a>
#### class `PostProcessing`  — L17143

> Post-processing filters, all the filters are applied in disparity domain.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `SpatialFilter` | `ClassVar[type[filters.params.SpatialFilter]]` | `...` | L17267 |
| `SpeckleFilter` | `ClassVar[type[filters.params.SpeckleFilter]]` | `...` | L17268 |
| `TemporalFilter` | `ClassVar[type[filters.params.TemporalFilter]]` | `...` | L17269 |
| `adaptiveMedianFilter` | `StereoDepthConfig.PostProcessing.AdaptiveMedianFilter` | — | L17270 |
| `bilateralSigmaValue` | `int` | — | L17271 |
| `brightnessFilter` | `StereoDepthConfig.PostProcessing.BrightnessFilter` | — | L17272 |
| `decimationFilter` | `StereoDepthConfig.PostProcessing.DecimationFilter` | — | L17273 |
| `filteringOrder` | `Incomplete` | — | L17274 |
| `holeFilling` | `StereoDepthConfig.PostProcessing.HoleFilling` | — | L17275 |
| `median` | `filters.params.MedianFilter` | — | L17276 |
| `spatialFilter` | `filters.params.SpatialFilter` | — | L17277 |
| `speckleFilter` | `filters.params.SpeckleFilter` | — | L17278 |
| `temporalFilter` | `filters.params.TemporalFilter` | — | L17279 |
| `thresholdFilter` | `StereoDepthConfig.PostProcessing.ThresholdFilter` | — | L17280 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17281 | __init__(self: depthai.StereoDepthConfig.PostProcessing) -> None |

**Nested Class:**

<a id="class-adaptivemedianfilter"></a>
##### class `AdaptiveMedianFilter`  — L17146

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `confidenceThreshold` | `int` | — | L17147 |
| `enable` | `bool` | — | L17148 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17149 | __init__(self: depthai.StereoDepthConfig.PostProcessing.AdaptiveMedianFilter) -> None |

**Nested Class:**

<a id="class-brightnessfilter"></a>
##### class `BrightnessFilter`  — L17152

> Brightness filtering. If input frame pixel is too dark or too bright, disparity
will be invalidated. The idea is that for too dark/too bright pixels we have low
confidence, since that area was under/over exposed and details were lost.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `maxBrightness` | `int` | — | L17156 |
| `minBrightness` | `int` | — | L17157 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17158 | __init__(self: depthai.StereoDepthConfig.PostProcessing.BrightnessFilter) -> None |

**Nested Class:**

<a id="class-decimationfilter"></a>
##### class `DecimationFilter`  — L17161

> Decimation filter. Reduces the depth scene complexity. The filter runs on kernel
sizes [2x2] to [8x8] pixels.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `decimationFactor` | `int` | — | L17201 |
| `decimationMode` | `StereoDepthConfig.PostProcessing.DecimationFilter.DecimationMode` | — | L17202 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17203 | __init__(self: depthai.StereoDepthConfig.PostProcessing.DecimationFilter) -> None |

**Nested Class:**

<a id="class-decimationmode"></a>
###### class `DecimationMode`  — L17165

> Decimation algorithm type.

Members:

  PIXEL_SKIPPING : 

  NON_ZERO_MEDIAN : 

  NON_ZERO_MEAN : 

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L17175 |
| `NON_ZERO_MEAN` | `ClassVar[StereoDepthConfig.PostProcessing.DecimationFilter.DecimationMode]` | `...` | L17176 |
| `NON_ZERO_MEDIAN` | `ClassVar[StereoDepthConfig.PostProcessing.DecimationFilter.DecimationMode]` | `...` | L17177 |
| `PIXEL_SKIPPING` | `ClassVar[StereoDepthConfig.PostProcessing.DecimationFilter.DecimationMode]` | `...` | L17178 |
| `__entries` | `ClassVar[dict]` | `...` | L17179 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L17180 | __init__(self: depthai.StereoDepthConfig.PostProcessing.DecimationFilter.DecimationMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L17182 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L17184 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L17186 | __index__(self: depthai.StereoDepthConfig.PostProcessing.DecimationFilter.DecimationMode) -> int |
| `def __int__(self) -> int` | `(self)` | L17188 | __int__(self: depthai.StereoDepthConfig.PostProcessing.DecimationFilter.DecimationMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L17190 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L17193 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L17199 | (arg0: depthai.StereoDepthConfig.PostProcessing.DecimationFilter.DecimationMode) -> int |

**Nested Class:**

<a id="class-filter"></a>
##### class `Filter`  — L17206

> Members:

  NONE : 

  DECIMATION : 

  SPECKLE : 

  MEDIAN : 

  SPATIAL : 

  TEMPORAL : 

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L17222 |
| `DECIMATION` | `ClassVar[StereoDepthConfig.PostProcessing.Filter]` | `...` | L17223 |
| `MEDIAN` | `ClassVar[StereoDepthConfig.PostProcessing.Filter]` | `...` | L17224 |
| `NONE` | `ClassVar[StereoDepthConfig.PostProcessing.Filter]` | `...` | L17225 |
| `SPATIAL` | `ClassVar[StereoDepthConfig.PostProcessing.Filter]` | `...` | L17226 |
| `SPECKLE` | `ClassVar[StereoDepthConfig.PostProcessing.Filter]` | `...` | L17227 |
| `TEMPORAL` | `ClassVar[StereoDepthConfig.PostProcessing.Filter]` | `...` | L17228 |
| `__entries` | `ClassVar[dict]` | `...` | L17229 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L17230 | __init__(self: depthai.StereoDepthConfig.PostProcessing.Filter, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L17232 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L17234 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L17236 | __index__(self: depthai.StereoDepthConfig.PostProcessing.Filter) -> int |
| `def __int__(self) -> int` | `(self)` | L17238 | __int__(self: depthai.StereoDepthConfig.PostProcessing.Filter) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L17240 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L17243 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L17249 | (arg0: depthai.StereoDepthConfig.PostProcessing.Filter) -> int |

**Nested Class:**

<a id="class-holefilling"></a>
##### class `HoleFilling`  — L17252

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `enable` | `bool` | — | L17253 |
| `fillConfidenceThreshold` | `int` | — | L17254 |
| `highConfidenceThreshold` | `int` | — | L17255 |
| `invalidateDisparities` | `bool` | — | L17256 |
| `minValidDisparity` | `int` | — | L17257 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17258 | __init__(self: depthai.StereoDepthConfig.PostProcessing.HoleFilling) -> None |

**Nested Class:**

<a id="class-thresholdfilter"></a>
##### class `ThresholdFilter`  — L17261

> Threshold filtering. Filters out distances outside of a given interval.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `maxRange` | `int` | — | L17263 |
| `minRange` | `int` | — | L17264 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17265 | __init__(self: depthai.StereoDepthConfig.PostProcessing.ThresholdFilter) -> None |

<a id="class-stereodepthproperties"></a>
### class `StereoDepthProperties`  — L17471

> Specify properties for StereoDepth

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `alphaScaling` | `float | None` | — | L17482 |
| `baseline` | `float | None` | — | L17483 |
| `depthAlignCamera` | `CameraBoardSocket` | — | L17484 |
| `depthAlignmentUseSpecTranslation` | `bool | None` | — | L17485 |
| `disparityToDepthUseSpecTranslation` | `bool | None` | — | L17486 |
| `enableRectification` | `bool` | — | L17487 |
| `enableRuntimeStereoModeSwitch` | `bool` | — | L17488 |
| `focalLength` | `float | None` | — | L17489 |
| `focalLengthFromCalibration` | `bool` | — | L17490 |
| `height` | `int | None` | — | L17491 |
| `initialConfig` | `StereoDepthConfig` | — | L17492 |
| `mesh` | `StereoDepthProperties.RectificationMesh` | — | L17493 |
| `numFramesPool` | `int` | — | L17494 |
| `numPostProcessingMemorySlices` | `int` | — | L17495 |
| `numPostProcessingShaves` | `int` | — | L17496 |
| `outHeight` | `int | None` | — | L17497 |
| `outKeepAspectRatio` | `bool` | — | L17498 |
| `outWidth` | `int | None` | — | L17499 |
| `rectificationUseSpecTranslation` | `bool | None` | — | L17500 |
| `rectifyEdgeFillColor` | `int` | — | L17501 |
| `useHomographyRectification` | `bool | None` | — | L17502 |
| `width` | `int | None` | — | L17503 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L17504 | Initialize self.  See help(type(self)) for accurate signature. |

**Nested Class:**

<a id="class-rectificationmesh"></a>
#### class `RectificationMesh`  — L17474

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `meshLeftUri` | `str` | — | L17475 |
| `meshRightUri` | `str` | — | L17476 |
| `meshSize` | `int | None` | — | L17477 |
| `stepHeight` | `int` | — | L17478 |
| `stepWidth` | `int` | — | L17479 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L17480 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-stereopair"></a>
### class `StereoPair`  — L17507

> Describes which camera sockets can be used for stereo and their baseline.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `baseline` | `float` | — | L17509 |
| `isVertical` | `bool` | — | L17510 |
| `left` | `CameraBoardSocket` | — | L17511 |
| `right` | `CameraBoardSocket` | — | L17512 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17513 | __init__(self: depthai.StereoPair) -> None |

<a id="class-stereorectification"></a>
### class `StereoRectification`  — L17516

> StereoRectification structure

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `leftCameraSocket` | `CameraBoardSocket` | — | L17518 |
| `rectifiedRotationLeft` | `list[list[float]]` | — | L17519 |
| `rectifiedRotationRight` | `list[list[float]]` | — | L17520 |
| `rightCameraSocket` | `CameraBoardSocket` | — | L17521 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17522 | __init__(self: depthai.StereoRectification) -> None |

<a id="class-syncproperties"></a>
### class `SyncProperties`  — L17525

> Specify properties for Sync.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `syncAttempts` | `int` | — | L17527 |
| `syncThresholdNs` | `int` | — | L17528 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L17529 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-systeminformation"></a>
### class `SystemInformation(Buffer)`  — L17532

> SystemInformation message. Carries memory usage, cpu usage and chip
temperatures.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `chipTemperature` | `ChipTemperature` | — | L17535 |
| `cmxMemoryUsage` | `MemoryInfo` | — | L17536 |
| `ddrMemoryUsage` | `MemoryInfo` | — | L17537 |
| `leonCssCpuUsage` | `CpuUsage` | — | L17538 |
| `leonCssMemoryUsage` | `MemoryInfo` | — | L17539 |
| `leonMssCpuUsage` | `CpuUsage` | — | L17540 |
| `leonMssMemoryUsage` | `MemoryInfo` | — | L17541 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17542 | __init__(self: depthai.SystemInformation) -> None |

<a id="class-systeminformationrvc4"></a>
### class `SystemInformationRVC4(Buffer)`  — L17545

> SystemInformation message Carries memory usage, cpu usage and chip temperatures.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `chipTemperature` | `ChipTemperatureRVC4` | — | L17547 |
| `cpuAvgUsage` | `CpuUsage` | — | L17548 |
| `cpuUsages` | `list[CpuUsage]` | — | L17549 |
| `ddrMemoryUsage` | `MemoryInfo` | — | L17550 |
| `processCpuAvgUsage` | `CpuUsage` | — | L17551 |
| `processMemoryUsage` | `int` | — | L17552 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17553 | __init__(self: depthai.SystemInformationRVC4) -> None |

<a id="class-systemloggerproperties"></a>
### class `SystemLoggerProperties`  — L17556

> SystemLoggerProperties structure

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `rateHz` | `float` | — | L17558 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L17559 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-tensorinfo"></a>
### class `TensorInfo`  — L17562

> TensorInfo structure

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `dataType` | `TensorInfo.DataType` | — | L17676 |
| `dims` | `list[int]` | — | L17677 |
| `name` | `str` | — | L17678 |
| `numDimensions` | `int` | — | L17679 |
| `offset` | `int` | — | L17680 |
| `order` | `TensorInfo.StorageOrder` | — | L17681 |
| `qpScale` | `float` | — | L17682 |
| `qpZp` | `float` | — | L17683 |
| `quantization` | `bool` | — | L17684 |
| `strides` | `list[int]` | — | L17685 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17686 | __init__(self: depthai.TensorInfo) -> None |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getTensorSize(self) -> int` | `(self)` | L17688 | getTensorSize(self: depthai.TensorInfo) -> int |

**Nested Class:**

<a id="class-datatype"></a>
#### class `DataType`  — L17565

> Members:

FP16

U8F

INT

FP32

I8

FP64

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L17579 |
| `FP16` | `ClassVar[TensorInfo.DataType]` | `...` | L17580 |
| `FP32` | `ClassVar[TensorInfo.DataType]` | `...` | L17581 |
| `FP64` | `ClassVar[TensorInfo.DataType]` | `...` | L17582 |
| `I8` | `ClassVar[TensorInfo.DataType]` | `...` | L17583 |
| `INT` | `ClassVar[TensorInfo.DataType]` | `...` | L17584 |
| `U8F` | `ClassVar[TensorInfo.DataType]` | `...` | L17585 |
| `__entries` | `ClassVar[dict]` | `...` | L17586 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L17587 | __init__(self: depthai.TensorInfo.DataType, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L17589 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L17591 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L17593 | __index__(self: depthai.TensorInfo.DataType) -> int |
| `def __int__(self) -> int` | `(self)` | L17595 | __int__(self: depthai.TensorInfo.DataType) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L17597 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L17600 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L17606 | (arg0: depthai.TensorInfo.DataType) -> int |

**Nested Class:**

<a id="class-storageorder"></a>
#### class `StorageOrder`  — L17609

> Members:

NHWC

NHCW

NCHW

HWC

CHW

WHC

HCW

WCH

CWH

NC

CN

C

H

W

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L17639 |
| `C` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17640 |
| `CHW` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17641 |
| `CN` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17642 |
| `CWH` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17643 |
| `H` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17644 |
| `HCW` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17645 |
| `HWC` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17646 |
| `NC` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17647 |
| `NCHW` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17648 |
| `NHCW` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17649 |
| `NHWC` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17650 |
| `W` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17651 |
| `WCH` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17652 |
| `WHC` | `ClassVar[TensorInfo.StorageOrder]` | `...` | L17653 |
| `__entries` | `ClassVar[dict]` | `...` | L17654 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L17655 | __init__(self: depthai.TensorInfo.StorageOrder, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L17657 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L17659 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L17661 | __index__(self: depthai.TensorInfo.StorageOrder) -> int |
| `def __int__(self) -> int` | `(self)` | L17663 | __int__(self: depthai.TensorInfo.StorageOrder) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L17665 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L17668 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L17674 | (arg0: depthai.TensorInfo.StorageOrder) -> int |

<a id="class-textannotation"></a>
### class `TextAnnotation`  — L17691

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `backgroundColor` | `Color` | — | L17692 |
| `fontSize` | `float` | — | L17693 |
| `position` | `Point2f` | — | L17694 |
| `text` | `str` | — | L17695 |
| `textColor` | `Color` | — | L17696 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17697 | __init__(self: depthai.TextAnnotation) -> None |

<a id="class-thermalambientparams"></a>
### class `ThermalAmbientParams`  — L17700

> Ambient factors that affect the temperature measurement of a Thermal sensor.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `atmosphericTemperature` | `int | None` | — | L17702 |
| `atmosphericTransmittance` | `int | None` | — | L17703 |
| `distance` | `int | None` | — | L17704 |
| `gainMode` | `ThermalGainMode | None` | — | L17705 |
| `reflectionTemperature` | `int | None` | — | L17706 |
| `targetEmissivity` | `int | None` | — | L17707 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17708 | __init__(self: depthai.ThermalAmbientParams) -> None |

<a id="class-thermalconfig"></a>
### class `ThermalConfig(Buffer)`  — L17711

> ThermalConfig message. Currently unused.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `ambientParams` | `ThermalAmbientParams` | — | L17713 |
| `ffcParams` | `ThermalFFCParams` | — | L17714 |
| `imageParams` | `ThermalImageParams` | — | L17715 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17716 | __init__(self: depthai.ThermalConfig) -> None |

<a id="class-thermalffcparams"></a>
### class `ThermalFFCParams`  — L17719

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `antiFallProtectionThresholdHighGainMode` | `int | None` | — | L17720 |
| `antiFallProtectionThresholdLowGainMode` | `int | None` | — | L17721 |
| `autoFFC` | `bool | None` | — | L17722 |
| `autoFFCTempThreshold` | `int | None` | — | L17723 |
| `closeManualShutter` | `bool | None` | — | L17724 |
| `fallProtection` | `bool | None` | — | L17725 |
| `maxFFCInterval` | `int | None` | — | L17726 |
| `minFFCInterval` | `int | None` | — | L17727 |
| `minShutterInterval` | `int | None` | — | L17728 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17729 | __init__(self: depthai.ThermalFFCParams) -> None |

<a id="class-thermalgainmode"></a>
### class `ThermalGainMode`  — L17732

> Thermal sensor gain mode. Use low gain in high energy environments.

Members:

  LOW : 

  HIGH : 

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L17740 |
| `HIGH` | `ClassVar[ThermalGainMode]` | `...` | L17741 |
| `LOW` | `ClassVar[ThermalGainMode]` | `...` | L17742 |
| `__entries` | `ClassVar[dict]` | `...` | L17743 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L17744 | __init__(self: depthai.ThermalGainMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L17746 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L17748 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L17750 | __index__(self: depthai.ThermalGainMode) -> int |
| `def __int__(self) -> int` | `(self)` | L17752 | __int__(self: depthai.ThermalGainMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L17754 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L17757 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L17763 | (arg0: depthai.ThermalGainMode) -> int |

<a id="class-thermalimageparams"></a>
### class `ThermalImageParams`  — L17766

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `brightnessLevel` | `int | None` | — | L17767 |
| `contrastLevel` | `int | None` | — | L17768 |
| `digitalDetailEnhanceLevel` | `int | None` | — | L17769 |
| `orientation` | `Incomplete` | — | L17770 |
| `spatialNoiseFilterLevel` | `int | None` | — | L17771 |
| `timeNoiseFilterLevel` | `int | None` | — | L17772 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17773 | __init__(self: depthai.ThermalImageParams) -> None |

<a id="class-thermalproperties"></a>
### class `ThermalProperties`  — L17776

> Specify properties for Thermal

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `boardSocket` | `CameraBoardSocket` | — | L17778 |
| `fps` | `float` | — | L17779 |
| `initialConfig` | `ThermalConfig` | — | L17780 |
| `numFramesPool` | `int` | — | L17781 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L17782 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-threadednode"></a>
### class `ThreadedNode(Node)`  — L17785

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L17786 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def pipelineEventOutput(self) -> Node.Output` | `(self)` | L17844 | (self: depthai.ThreadedNode) -> depthai.Node.Output |

**🔹 Public Methods (13):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def blockEvent(self, type: PipelineEvent.Type, source: str) -> BlockPipelineEvent` | `(self, type: PipelineEvent.Type, source: str)` | L17788 | blockEvent(self: depthai.ThreadedNode, type: depthai.PipelineEvent.Type, source: str) -> depthai.BlockPipelineEvent |
| `def critical(self, arg0: str) -> None` | `(self, arg0: str)` | L17799 | critical(self: depthai.ThreadedNode, arg0: str) -> None |
| `def debug(self, arg0: str) -> None` | `(self, arg0: str)` | L17801 | debug(self: depthai.ThreadedNode, arg0: str) -> None |
| `def error(self, arg0: str) -> None` | `(self, arg0: str)` | L17803 | error(self: depthai.ThreadedNode, arg0: str) -> None |
| `def getLogLevel(self) -> LogLevel` | `(self)` | L17805 | getLogLevel(self: depthai.ThreadedNode) -> depthai.LogLevel |
| `def info(self, arg0: str) -> None` | `(self, arg0: str)` | L17813 | info(self: depthai.ThreadedNode, arg0: str) -> None |
| `def inputBlockEvent(self) -> BlockPipelineEvent` | `(self)` | L17815 | inputBlockEvent(self: depthai.ThreadedNode) -> depthai.BlockPipelineEvent |
| `def isRunning(self) -> bool` | `(self)` | L17821 | isRunning(self: depthai.ThreadedNode) -> bool |
| `def mainLoop(self) -> bool` | `(self)` | L17823 | mainLoop(self: depthai.ThreadedNode) -> bool |
| `def outputBlockEvent(self) -> BlockPipelineEvent` | `(self)` | L17825 | outputBlockEvent(self: depthai.ThreadedNode) -> depthai.BlockPipelineEvent |
| `def setLogLevel(self, arg0: LogLevel) -> None` | `(self, arg0: LogLevel)` | L17831 | setLogLevel(self: depthai.ThreadedNode, arg0: depthai.LogLevel) -> None |
| `def trace(self, arg0: str) -> None` | `(self, arg0: str)` | L17839 | trace(self: depthai.ThreadedNode, arg0: str) -> None |
| `def warn(self, arg0: str) -> None` | `(self, arg0: str)` | L17841 | warn(self: depthai.ThreadedNode, arg0: str) -> None |

<a id="class-timestamp"></a>
### class `Timestamp`  — L17847

> Timestamp structure

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `nsec` | `int` | — | L17849 |
| `sec` | `int` | — | L17850 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17851 | __init__(self: depthai.Timestamp) -> None |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def get(self) -> datetime.timedelta` | `(self)` | L17853 | get(self: depthai.Timestamp) -> datetime.timedelta |

<a id="class-tofconfig"></a>
### class `ToFConfig(Buffer)`  — L17856

> ToFConfig message. Carries config for feature tracking algorithm

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `enableBurstMode` | `bool` | — | L17858 |
| `enableDistortionCorrection` | `bool` | — | L17859 |
| `enableFPPNCorrection` | `bool | None` | — | L17860 |
| `enableOpticalCorrection` | `bool | None` | — | L17861 |
| `enablePhaseShuffleTemporalFilter` | `bool` | — | L17862 |
| `enablePhaseUnwrapping` | `bool | None` | — | L17863 |
| `enableTemperatureCorrection` | `bool | None` | — | L17864 |
| `enableWiggleCorrection` | `bool | None` | — | L17865 |
| `median` | `filters.params.MedianFilter` | — | L17866 |
| `phaseUnwrapErrorThreshold` | `int` | — | L17867 |
| `phaseUnwrappingLevel` | `int` | — | L17868 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17869 | __init__(self: depthai.ToFConfig) -> None |

**🔹 Public Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def setMedianFilter(self, arg0: filters.params.MedianFilter) -> ToFConfig` | `(self, arg0: filters.params.MedianFilter)` | L17871 | setMedianFilter(self: depthai.ToFConfig, arg0: depthai.filters.params.MedianFilter) -> depthai.ToFConfig |
| `def setProfilePreset(self, arg0: ImageFiltersPresetMode) -> None` | `(self, arg0: ImageFiltersPresetMode)` | L17877 | setProfilePreset(self: depthai.ToFConfig, arg0: depthai.ImageFiltersPresetMode) -> None |

<a id="class-tofdepthconfidencefilterconfig"></a>
### class `ToFDepthConfidenceFilterConfig(Buffer)`  — L17886

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `confidenceThreshold` | `float` | — | L17887 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17888 | __init__(self: depthai.ToFDepthConfidenceFilterConfig) -> None |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def setProfilePreset(self, arg0) -> None` | `(self, arg0)` | L17890 | setProfilePreset(self: depthai.ToFDepthConfidenceFilterConfig, arg0: dai::ImageFiltersPresetMode) -> None |

<a id="class-tofdepthconfidencefilterproperties"></a>
### class `ToFDepthConfidenceFilterProperties`  — L17899

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L17900 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-tofproperties"></a>
### class `ToFProperties`  — L17903

> Specify properties for ToF

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `initialConfig` | `ToFConfig` | — | L17905 |
| `numFramesPool` | `int` | — | L17906 |
| `numShaves` | `int | None` | — | L17907 |
| `warpHwIds` | `list[int]` | — | L17908 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L17909 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-trackedfeature"></a>
### class `TrackedFeature`  — L17912

> TrackedFeature structure

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `age` | `int` | — | L17914 |
| `descriptor` | `Incomplete` | — | L17915 |
| `harrisScore` | `float` | — | L17916 |
| `id` | `int` | — | L17917 |
| `position` | `Point2f` | — | L17918 |
| `trackingError` | `float` | — | L17919 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17920 | __init__(self: depthai.TrackedFeature) -> None |

<a id="class-trackedfeatures"></a>
### class `TrackedFeatures(Buffer)`  — L17923

> TrackedFeatures message. Carries position (X, Y) of tracked features and their
ID.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `trackedFeatures` | `list[TrackedFeature]` | — | L17926 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L17927 | __init__(self: depthai.TrackedFeatures) -> None |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getSequenceNum(self) -> int` | `(self)` | L17929 | getSequenceNum(self: depthai.TrackedFeatures) -> int |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L17934 | getTimestamp(self: depthai.TrackedFeatures) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L17939 | getTimestampDevice(self: depthai.TrackedFeatures) -> datetime.timedelta |

<a id="class-trackeridassignmentpolicy"></a>
### class `TrackerIdAssignmentPolicy`  — L17946

> Members:

UNIQUE_ID

SMALLEST_ID

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L17952 |
| `SMALLEST_ID` | `ClassVar[TrackerIdAssignmentPolicy]` | `...` | L17953 |
| `UNIQUE_ID` | `ClassVar[TrackerIdAssignmentPolicy]` | `...` | L17954 |
| `__entries` | `ClassVar[dict]` | `...` | L17955 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L17956 | __init__(self: depthai.TrackerIdAssignmentPolicy, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L17958 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L17960 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L17962 | __index__(self: depthai.TrackerIdAssignmentPolicy) -> int |
| `def __int__(self) -> int` | `(self)` | L17964 | __int__(self: depthai.TrackerIdAssignmentPolicy) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L17966 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L17969 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L17975 | (arg0: depthai.TrackerIdAssignmentPolicy) -> int |

<a id="class-trackertype"></a>
### class `TrackerType`  — L17978

> Members:

SHORT_TERM_KCF : Kernelized Correlation Filter tracking

SHORT_TERM_IMAGELESS : Short term tracking without using image data

ZERO_TERM_IMAGELESS : Ability to track the objects without accessing image data.

ZERO_TERM_COLOR_HISTOGRAM : Tracking using image data too.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L17988 |
| `SHORT_TERM_IMAGELESS` | `ClassVar[TrackerType]` | `...` | L17989 |
| `SHORT_TERM_KCF` | `ClassVar[TrackerType]` | `...` | L17990 |
| `ZERO_TERM_COLOR_HISTOGRAM` | `ClassVar[TrackerType]` | `...` | L17991 |
| `ZERO_TERM_IMAGELESS` | `ClassVar[TrackerType]` | `...` | L17992 |
| `__entries` | `ClassVar[dict]` | `...` | L17993 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L17994 | __init__(self: depthai.TrackerType, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L17996 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L17998 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L18000 | __index__(self: depthai.TrackerType) -> int |
| `def __int__(self) -> int` | `(self)` | L18002 | __int__(self: depthai.TrackerType) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L18004 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L18007 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L18013 | (arg0: depthai.TrackerType) -> int |

<a id="class-tracklet"></a>
### class `Tracklet`  — L18016

> Tracklet structure

Contains tracklets from object tracker output.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `age` | `int` | — | L18060 |
| `id` | `int` | — | L18061 |
| `label` | `int` | — | L18062 |
| `roi` | `Rect` | — | L18063 |
| `spatialCoordinates` | `Point3f` | — | L18064 |
| `srcImgDetection` | `ImgDetection` | — | L18065 |
| `status` | `Tracklet.TrackingStatus` | — | L18066 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L18067 | __init__(self: depthai.Tracklet) -> None |

**Nested Class:**

<a id="class-trackingstatus"></a>
#### class `TrackingStatus`  — L18021

> Members:

  NEW

  TRACKED

  LOST

  REMOVED

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L18033 |
| `LOST` | `ClassVar[Tracklet.TrackingStatus]` | `...` | L18034 |
| `NEW` | `ClassVar[Tracklet.TrackingStatus]` | `...` | L18035 |
| `REMOVED` | `ClassVar[Tracklet.TrackingStatus]` | `...` | L18036 |
| `TRACKED` | `ClassVar[Tracklet.TrackingStatus]` | `...` | L18037 |
| `__entries` | `ClassVar[dict]` | `...` | L18038 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L18039 | __init__(self: depthai.Tracklet.TrackingStatus, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L18041 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L18043 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L18045 | __index__(self: depthai.Tracklet.TrackingStatus) -> int |
| `def __int__(self) -> int` | `(self)` | L18047 | __int__(self: depthai.Tracklet.TrackingStatus) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L18049 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L18052 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L18058 | (arg0: depthai.Tracklet.TrackingStatus) -> int |

<a id="class-tracklets"></a>
### class `Tracklets(Buffer)`  — L18070

> Tracklets message. Carries object tracking information.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `tracklets` | `list[Tracklet]` | — | L18072 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L18073 | __init__(self: depthai.Tracklets) -> None |

**🔹 Public Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getSequenceNum(self) -> int` | `(self)` | L18075 | getSequenceNum(self: depthai.Tracklets) -> int |
| `def getTimestamp(self) -> datetime.timedelta` | `(self)` | L18080 | getTimestamp(self: depthai.Tracklets) -> datetime.timedelta |
| `def getTimestampDevice(self) -> datetime.timedelta` | `(self)` | L18085 | getTimestampDevice(self: depthai.Tracklets) -> datetime.timedelta |
| `def getTransformation(self) -> ImgTransformation` | `(self)` | L18091 | getTransformation(self: depthai.Tracklets) -> depthai.ImgTransformation |
| `def setTransformation(self, arg0: ImgTransformation) -> None` | `(self, arg0: ImgTransformation)` | L18093 | setTransformation(self: depthai.Tracklets, arg0: depthai.ImgTransformation) -> None |

<a id="class-transformdata"></a>
### class `TransformData(Buffer)`  — L18096

> TransformData message. Carries transform in x,y,z,qx,qy,qz,qw format.

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L18098 | __init__(self: depthai.TransformData) -> None |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getQuaternion(self) -> Quaterniond` | `(self)` | L18100 | getQuaternion(self: depthai.TransformData) -> depthai.Quaterniond |
| `def getRotationEuler(self) -> Point3d` | `(self)` | L18102 | getRotationEuler(self: depthai.TransformData) -> depthai.Point3d |
| `def getTranslation(self) -> Point3d` | `(self)` | L18104 | getTranslation(self: depthai.TransformData) -> depthai.Point3d |

<a id="class-uvcproperties"></a>
### class `UVCProperties`  — L18107

> Properties for UVC node

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `gpioInit` | `dict[int, int]` | — | L18109 |
| `gpioStreamOff` | `dict[int, int]` | — | L18110 |
| `gpioStreamOn` | `dict[int, int]` | — | L18111 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L18112 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-usbspeed"></a>
### class `UsbSpeed`  — L18115

> Get USB Speed

Members:

  UNKNOWN

  LOW

  FULL

  HIGH

  SUPER

  SUPER_PLUS

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L18131 |
| `FULL` | `ClassVar[UsbSpeed]` | `...` | L18132 |
| `HIGH` | `ClassVar[UsbSpeed]` | `...` | L18133 |
| `LOW` | `ClassVar[UsbSpeed]` | `...` | L18134 |
| `SUPER` | `ClassVar[UsbSpeed]` | `...` | L18135 |
| `SUPER_PLUS` | `ClassVar[UsbSpeed]` | `...` | L18136 |
| `UNKNOWN` | `ClassVar[UsbSpeed]` | `...` | L18137 |
| `__entries` | `ClassVar[dict]` | `...` | L18138 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L18139 | __init__(self: depthai.UsbSpeed, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L18141 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L18143 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L18145 | __index__(self: depthai.UsbSpeed) -> int |
| `def __int__(self) -> int` | `(self)` | L18147 | __int__(self: depthai.UsbSpeed) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L18149 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L18152 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L18158 | (arg0: depthai.UsbSpeed) -> int |

<a id="class-vectorcircleannotation"></a>
### class `VectorCircleAnnotation`  — L18161

**🔧 Dunder Methods (12):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L18163 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: VectorCircleAnnotation) -> None` | `(self, arg0: VectorCircleAnnotation)` | L18176 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: Iterable) -> None` | `(self, arg0: Iterable)` | L18189 | __init__(*args, **kwargs) |
| `def __bool__(self) -> bool` | `(self)` | L18268 | __bool__(self: depthai.VectorCircleAnnotation) -> bool |
| `@overload` `def __delitem__(self, arg0: int) -> None` | `(self, arg0: int)` | L18274 | __delitem__(*args, **kwargs) |
| `@overload` `def __delitem__(self, arg0: slice) -> None` | `(self, arg0: slice)` | L18287 | __delitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, s: slice) -> VectorCircleAnnotation` | `(self, s: slice)` | L18300 | __getitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, arg0: int) -> CircleAnnotation` | `(self, arg0: int)` | L18311 | __getitem__(*args, **kwargs) |
| `def __iter__(self) -> Iterator[CircleAnnotation]` | `(self)` | L18321 | __iter__(self: depthai.VectorCircleAnnotation) -> Iterator[depthai.CircleAnnotation] |
| `def __len__(self) -> int` | `(self)` | L18323 | __len__(self: depthai.VectorCircleAnnotation) -> int |
| `@overload` `def __setitem__(self, arg0: int, arg1: CircleAnnotation) -> None` | `(self, arg0: int, arg1: CircleAnnotation)` | L18326 | __setitem__(*args, **kwargs) |
| `@overload` `def __setitem__(self, arg0: slice, arg1: VectorCircleAnnotation) -> None` | `(self, arg0: slice, arg1: VectorCircleAnnotation)` | L18337 | __setitem__(*args, **kwargs) |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def append(self, x: CircleAnnotation) -> None` | `(self, x: CircleAnnotation)` | L18201 | append(self: depthai.VectorCircleAnnotation, x: depthai.CircleAnnotation) -> None |
| `def clear(self) -> None` | `(self)` | L18206 | clear(self: depthai.VectorCircleAnnotation) -> None |
| `@overload` `def extend(self, L: VectorCircleAnnotation) -> None` | `(self, L: VectorCircleAnnotation)` | L18212 | extend(*args, **kwargs) |
| `@overload` `def extend(self, L: Iterable) -> None` | `(self, L: Iterable)` | L18225 | extend(*args, **kwargs) |
| `def insert(self, i: int, x: CircleAnnotation) -> None` | `(self, i: int, x: CircleAnnotation)` | L18237 | insert(self: depthai.VectorCircleAnnotation, i: int, x: depthai.CircleAnnotation) -> None |
| `@overload` `def pop(self) -> CircleAnnotation` | `(self)` | L18243 | pop(*args, **kwargs) |
| `@overload` `def pop(self, i: int) -> CircleAnnotation` | `(self, i: int)` | L18256 | pop(*args, **kwargs) |

<a id="class-vectorcolor"></a>
### class `VectorColor`  — L18348

**🔧 Dunder Methods (12):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L18350 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: VectorColor) -> None` | `(self, arg0: VectorColor)` | L18363 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: Iterable) -> None` | `(self, arg0: Iterable)` | L18376 | __init__(*args, **kwargs) |
| `def __bool__(self) -> bool` | `(self)` | L18455 | __bool__(self: depthai.VectorColor) -> bool |
| `@overload` `def __delitem__(self, arg0: int) -> None` | `(self, arg0: int)` | L18461 | __delitem__(*args, **kwargs) |
| `@overload` `def __delitem__(self, arg0: slice) -> None` | `(self, arg0: slice)` | L18474 | __delitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, s: slice) -> VectorColor` | `(self, s: slice)` | L18487 | __getitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, arg0: int) -> Color` | `(self, arg0: int)` | L18498 | __getitem__(*args, **kwargs) |
| `def __iter__(self) -> Iterator[Color]` | `(self)` | L18508 | __iter__(self: depthai.VectorColor) -> Iterator[depthai.Color] |
| `def __len__(self) -> int` | `(self)` | L18510 | __len__(self: depthai.VectorColor) -> int |
| `@overload` `def __setitem__(self, arg0: int, arg1: Color) -> None` | `(self, arg0: int, arg1: Color)` | L18513 | __setitem__(*args, **kwargs) |
| `@overload` `def __setitem__(self, arg0: slice, arg1: VectorColor) -> None` | `(self, arg0: slice, arg1: VectorColor)` | L18524 | __setitem__(*args, **kwargs) |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def append(self, x: Color) -> None` | `(self, x: Color)` | L18388 | append(self: depthai.VectorColor, x: depthai.Color) -> None |
| `def clear(self) -> None` | `(self)` | L18393 | clear(self: depthai.VectorColor) -> None |
| `@overload` `def extend(self, L: VectorColor) -> None` | `(self, L: VectorColor)` | L18399 | extend(*args, **kwargs) |
| `@overload` `def extend(self, L: Iterable) -> None` | `(self, L: Iterable)` | L18412 | extend(*args, **kwargs) |
| `def insert(self, i: int, x: Color) -> None` | `(self, i: int, x: Color)` | L18424 | insert(self: depthai.VectorColor, i: int, x: depthai.Color) -> None |
| `@overload` `def pop(self) -> Color` | `(self)` | L18430 | pop(*args, **kwargs) |
| `@overload` `def pop(self, i: int) -> Color` | `(self, i: int)` | L18443 | pop(*args, **kwargs) |

<a id="class-vectorimgannotation"></a>
### class `VectorImgAnnotation`  — L18535

**🔧 Dunder Methods (12):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L18537 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: VectorImgAnnotation) -> None` | `(self, arg0: VectorImgAnnotation)` | L18550 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: Iterable) -> None` | `(self, arg0: Iterable)` | L18563 | __init__(*args, **kwargs) |
| `def __bool__(self) -> bool` | `(self)` | L18642 | __bool__(self: depthai.VectorImgAnnotation) -> bool |
| `@overload` `def __delitem__(self, arg0: int) -> None` | `(self, arg0: int)` | L18648 | __delitem__(*args, **kwargs) |
| `@overload` `def __delitem__(self, arg0: slice) -> None` | `(self, arg0: slice)` | L18661 | __delitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, s: slice) -> VectorImgAnnotation` | `(self, s: slice)` | L18674 | __getitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, arg0: int) -> ImgAnnotation` | `(self, arg0: int)` | L18685 | __getitem__(*args, **kwargs) |
| `def __iter__(self) -> Iterator[ImgAnnotation]` | `(self)` | L18695 | __iter__(self: depthai.VectorImgAnnotation) -> Iterator[depthai.ImgAnnotation] |
| `def __len__(self) -> int` | `(self)` | L18697 | __len__(self: depthai.VectorImgAnnotation) -> int |
| `@overload` `def __setitem__(self, arg0: int, arg1: ImgAnnotation) -> None` | `(self, arg0: int, arg1: ImgAnnotation)` | L18700 | __setitem__(*args, **kwargs) |
| `@overload` `def __setitem__(self, arg0: slice, arg1: VectorImgAnnotation) -> None` | `(self, arg0: slice, arg1: VectorImgAnnotation)` | L18711 | __setitem__(*args, **kwargs) |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def append(self, x: ImgAnnotation) -> None` | `(self, x: ImgAnnotation)` | L18575 | append(self: depthai.VectorImgAnnotation, x: depthai.ImgAnnotation) -> None |
| `def clear(self) -> None` | `(self)` | L18580 | clear(self: depthai.VectorImgAnnotation) -> None |
| `@overload` `def extend(self, L: VectorImgAnnotation) -> None` | `(self, L: VectorImgAnnotation)` | L18586 | extend(*args, **kwargs) |
| `@overload` `def extend(self, L: Iterable) -> None` | `(self, L: Iterable)` | L18599 | extend(*args, **kwargs) |
| `def insert(self, i: int, x: ImgAnnotation) -> None` | `(self, i: int, x: ImgAnnotation)` | L18611 | insert(self: depthai.VectorImgAnnotation, i: int, x: depthai.ImgAnnotation) -> None |
| `@overload` `def pop(self) -> ImgAnnotation` | `(self)` | L18617 | pop(*args, **kwargs) |
| `@overload` `def pop(self, i: int) -> ImgAnnotation` | `(self, i: int)` | L18630 | pop(*args, **kwargs) |

<a id="class-vectorpoint2f"></a>
### class `VectorPoint2f`  — L18722

**🔧 Dunder Methods (12):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L18724 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: VectorPoint2f) -> None` | `(self, arg0: VectorPoint2f)` | L18737 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: Iterable) -> None` | `(self, arg0: Iterable)` | L18750 | __init__(*args, **kwargs) |
| `def __bool__(self) -> bool` | `(self)` | L18829 | __bool__(self: depthai.VectorPoint2f) -> bool |
| `@overload` `def __delitem__(self, arg0: int) -> None` | `(self, arg0: int)` | L18835 | __delitem__(*args, **kwargs) |
| `@overload` `def __delitem__(self, arg0: slice) -> None` | `(self, arg0: slice)` | L18848 | __delitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, s: slice) -> VectorPoint2f` | `(self, s: slice)` | L18861 | __getitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, arg0: int) -> Point2f` | `(self, arg0: int)` | L18872 | __getitem__(*args, **kwargs) |
| `def __iter__(self) -> Iterator[Point2f]` | `(self)` | L18882 | __iter__(self: depthai.VectorPoint2f) -> Iterator[depthai.Point2f] |
| `def __len__(self) -> int` | `(self)` | L18884 | __len__(self: depthai.VectorPoint2f) -> int |
| `@overload` `def __setitem__(self, arg0: int, arg1: Point2f) -> None` | `(self, arg0: int, arg1: Point2f)` | L18887 | __setitem__(*args, **kwargs) |
| `@overload` `def __setitem__(self, arg0: slice, arg1: VectorPoint2f) -> None` | `(self, arg0: slice, arg1: VectorPoint2f)` | L18898 | __setitem__(*args, **kwargs) |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def append(self, x: Point2f) -> None` | `(self, x: Point2f)` | L18762 | append(self: depthai.VectorPoint2f, x: depthai.Point2f) -> None |
| `def clear(self) -> None` | `(self)` | L18767 | clear(self: depthai.VectorPoint2f) -> None |
| `@overload` `def extend(self, L: VectorPoint2f) -> None` | `(self, L: VectorPoint2f)` | L18773 | extend(*args, **kwargs) |
| `@overload` `def extend(self, L: Iterable) -> None` | `(self, L: Iterable)` | L18786 | extend(*args, **kwargs) |
| `def insert(self, i: int, x: Point2f) -> None` | `(self, i: int, x: Point2f)` | L18798 | insert(self: depthai.VectorPoint2f, i: int, x: depthai.Point2f) -> None |
| `@overload` `def pop(self) -> Point2f` | `(self)` | L18804 | pop(*args, **kwargs) |
| `@overload` `def pop(self, i: int) -> Point2f` | `(self, i: int)` | L18817 | pop(*args, **kwargs) |

<a id="class-vectorpointsannotation"></a>
### class `VectorPointsAnnotation`  — L18909

**🔧 Dunder Methods (12):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L18911 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: VectorPointsAnnotation) -> None` | `(self, arg0: VectorPointsAnnotation)` | L18924 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: Iterable) -> None` | `(self, arg0: Iterable)` | L18937 | __init__(*args, **kwargs) |
| `def __bool__(self) -> bool` | `(self)` | L19016 | __bool__(self: depthai.VectorPointsAnnotation) -> bool |
| `@overload` `def __delitem__(self, arg0: int) -> None` | `(self, arg0: int)` | L19022 | __delitem__(*args, **kwargs) |
| `@overload` `def __delitem__(self, arg0: slice) -> None` | `(self, arg0: slice)` | L19035 | __delitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, s: slice) -> VectorPointsAnnotation` | `(self, s: slice)` | L19048 | __getitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, arg0: int) -> PointsAnnotation` | `(self, arg0: int)` | L19059 | __getitem__(*args, **kwargs) |
| `def __iter__(self) -> Iterator[PointsAnnotation]` | `(self)` | L19069 | __iter__(self: depthai.VectorPointsAnnotation) -> Iterator[depthai.PointsAnnotation] |
| `def __len__(self) -> int` | `(self)` | L19071 | __len__(self: depthai.VectorPointsAnnotation) -> int |
| `@overload` `def __setitem__(self, arg0: int, arg1: PointsAnnotation) -> None` | `(self, arg0: int, arg1: PointsAnnotation)` | L19074 | __setitem__(*args, **kwargs) |
| `@overload` `def __setitem__(self, arg0: slice, arg1: VectorPointsAnnotation) -> None` | `(self, arg0: slice, arg1: VectorPointsAnnotation)` | L19085 | __setitem__(*args, **kwargs) |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def append(self, x: PointsAnnotation) -> None` | `(self, x: PointsAnnotation)` | L18949 | append(self: depthai.VectorPointsAnnotation, x: depthai.PointsAnnotation) -> None |
| `def clear(self) -> None` | `(self)` | L18954 | clear(self: depthai.VectorPointsAnnotation) -> None |
| `@overload` `def extend(self, L: VectorPointsAnnotation) -> None` | `(self, L: VectorPointsAnnotation)` | L18960 | extend(*args, **kwargs) |
| `@overload` `def extend(self, L: Iterable) -> None` | `(self, L: Iterable)` | L18973 | extend(*args, **kwargs) |
| `def insert(self, i: int, x: PointsAnnotation) -> None` | `(self, i: int, x: PointsAnnotation)` | L18985 | insert(self: depthai.VectorPointsAnnotation, i: int, x: depthai.PointsAnnotation) -> None |
| `@overload` `def pop(self) -> PointsAnnotation` | `(self)` | L18991 | pop(*args, **kwargs) |
| `@overload` `def pop(self, i: int) -> PointsAnnotation` | `(self, i: int)` | L19004 | pop(*args, **kwargs) |

<a id="class-vectortextannotation"></a>
### class `VectorTextAnnotation`  — L19096

**🔧 Dunder Methods (12):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self) -> None` | `(self)` | L19098 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: VectorTextAnnotation) -> None` | `(self, arg0: VectorTextAnnotation)` | L19111 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: Iterable) -> None` | `(self, arg0: Iterable)` | L19124 | __init__(*args, **kwargs) |
| `def __bool__(self) -> bool` | `(self)` | L19203 | __bool__(self: depthai.VectorTextAnnotation) -> bool |
| `@overload` `def __delitem__(self, arg0: int) -> None` | `(self, arg0: int)` | L19209 | __delitem__(*args, **kwargs) |
| `@overload` `def __delitem__(self, arg0: slice) -> None` | `(self, arg0: slice)` | L19222 | __delitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, s: slice) -> VectorTextAnnotation` | `(self, s: slice)` | L19235 | __getitem__(*args, **kwargs) |
| `@overload` `def __getitem__(self, arg0: int) -> TextAnnotation` | `(self, arg0: int)` | L19246 | __getitem__(*args, **kwargs) |
| `def __iter__(self) -> Iterator[TextAnnotation]` | `(self)` | L19256 | __iter__(self: depthai.VectorTextAnnotation) -> Iterator[depthai.TextAnnotation] |
| `def __len__(self) -> int` | `(self)` | L19258 | __len__(self: depthai.VectorTextAnnotation) -> int |
| `@overload` `def __setitem__(self, arg0: int, arg1: TextAnnotation) -> None` | `(self, arg0: int, arg1: TextAnnotation)` | L19261 | __setitem__(*args, **kwargs) |
| `@overload` `def __setitem__(self, arg0: slice, arg1: VectorTextAnnotation) -> None` | `(self, arg0: slice, arg1: VectorTextAnnotation)` | L19272 | __setitem__(*args, **kwargs) |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def append(self, x: TextAnnotation) -> None` | `(self, x: TextAnnotation)` | L19136 | append(self: depthai.VectorTextAnnotation, x: depthai.TextAnnotation) -> None |
| `def clear(self) -> None` | `(self)` | L19141 | clear(self: depthai.VectorTextAnnotation) -> None |
| `@overload` `def extend(self, L: VectorTextAnnotation) -> None` | `(self, L: VectorTextAnnotation)` | L19147 | extend(*args, **kwargs) |
| `@overload` `def extend(self, L: Iterable) -> None` | `(self, L: Iterable)` | L19160 | extend(*args, **kwargs) |
| `def insert(self, i: int, x: TextAnnotation) -> None` | `(self, i: int, x: TextAnnotation)` | L19172 | insert(self: depthai.VectorTextAnnotation, i: int, x: depthai.TextAnnotation) -> None |
| `@overload` `def pop(self) -> TextAnnotation` | `(self)` | L19178 | pop(*args, **kwargs) |
| `@overload` `def pop(self, i: int) -> TextAnnotation` | `(self, i: int)` | L19191 | pop(*args, **kwargs) |

<a id="class-version"></a>
### class `Version`  — L19283

> Version structure

**🔧 Dunder Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self, v: str) -> None` | `(self, v: str)` | L19286 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, major: int, minor: int, patch: int) -> None` | `(self, major: int, minor: int, patch: int)` | L19299 | __init__(*args, **kwargs) |
| `def __eq__(self, arg0: Version) -> bool` | `(self, arg0: Version)` | L19321 | __eq__(self: depthai.Version, arg0: depthai.Version) -> bool |
| `def __gt__(self, arg0: Version) -> bool` | `(self, arg0: Version)` | L19323 | __gt__(self: depthai.Version, arg0: depthai.Version) -> bool |
| `def __lt__(self, arg0: Version) -> bool` | `(self, arg0: Version)` | L19325 | __lt__(self: depthai.Version, arg0: depthai.Version) -> bool |

**🔹 Public Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getBuildInfo(self) -> str` | `(self)` | L19311 | getBuildInfo(self: depthai.Version) -> str |
| `def toStringSemver(self) -> str` | `(self)` | L19316 | toStringSemver(self: depthai.Version) -> str |

<a id="class-videoencoderproperties"></a>
### class `VideoEncoderProperties`  — L19328

> Specify properties for VideoEncoder such as profile, bitrate, ...

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `bitrate` | `int` | — | L19408 |
| `keyframeFrequency` | `int` | — | L19409 |
| `maxBitrate` | `int` | — | L19410 |
| `numBFrames` | `int` | — | L19411 |
| `numFramesPool` | `int` | — | L19412 |
| `outputFrameSize` | `int` | — | L19413 |
| `profile` | `VideoEncoderProperties.Profile` | — | L19414 |
| `quality` | `int` | — | L19415 |
| `rateCtrlMode` | `VideoEncoderProperties.RateControlMode` | — | L19416 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L19417 | Initialize self.  See help(type(self)) for accurate signature. |

**Nested Class:**

<a id="class-profile"></a>
#### class `Profile`  — L19331

> Encoding profile, H264 (AVC), H265 (HEVC) or MJPEG

Members:

  H264_BASELINE

  H264_HIGH

  H264_MAIN

  H265_MAIN

  MJPEG

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L19345 |
| `H264_BASELINE` | `ClassVar[VideoEncoderProperties.Profile]` | `...` | L19346 |
| `H264_HIGH` | `ClassVar[VideoEncoderProperties.Profile]` | `...` | L19347 |
| `H264_MAIN` | `ClassVar[VideoEncoderProperties.Profile]` | `...` | L19348 |
| `H265_MAIN` | `ClassVar[VideoEncoderProperties.Profile]` | `...` | L19349 |
| `MJPEG` | `ClassVar[VideoEncoderProperties.Profile]` | `...` | L19350 |
| `__entries` | `ClassVar[dict]` | `...` | L19351 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L19352 | __init__(self: depthai.VideoEncoderProperties.Profile, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L19354 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L19356 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L19358 | __index__(self: depthai.VideoEncoderProperties.Profile) -> int |
| `def __int__(self) -> int` | `(self)` | L19360 | __int__(self: depthai.VideoEncoderProperties.Profile) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L19362 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L19365 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L19371 | (arg0: depthai.VideoEncoderProperties.Profile) -> int |

**Nested Class:**

<a id="class-ratecontrolmode"></a>
#### class `RateControlMode`  — L19374

> Rate control mode specifies if constant or variable bitrate should be used (H264
/ H265)

Members:

  CBR

  VBR

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L19383 |
| `CBR` | `ClassVar[VideoEncoderProperties.RateControlMode]` | `...` | L19384 |
| `VBR` | `ClassVar[VideoEncoderProperties.RateControlMode]` | `...` | L19385 |
| `__entries` | `ClassVar[dict]` | `...` | L19386 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L19387 | __init__(self: depthai.VideoEncoderProperties.RateControlMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L19389 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L19391 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L19393 | __index__(self: depthai.VideoEncoderProperties.RateControlMode) -> int |
| `def __int__(self) -> int` | `(self)` | L19395 | __int__(self: depthai.VideoEncoderProperties.RateControlMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L19397 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L19400 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L19406 | (arg0: depthai.VideoEncoderProperties.RateControlMode) -> int |

<a id="class-vppconfig"></a>
### class `VppConfig(Buffer)`  — L19420

> VppConfig message. Carries config for Virtual Projection Pattern algorithm

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `MAXDIST` | `ClassVar[VppConfig.PatchColoringType]` | `...` | L19466 |
| `RANDOM` | `ClassVar[VppConfig.PatchColoringType]` | `...` | L19467 |
| `blending` | `float` | — | L19468 |
| `distanceGamma` | `float` | — | L19469 |
| `injectionParameters` | `VppConfig.InjectionParameters` | — | L19470 |
| `maxFPS` | `int` | — | L19471 |
| `maxNumThreads` | `int` | — | L19472 |
| `maxPatchSize` | `int` | — | L19473 |
| `patchColoringType` | `VppConfig.PatchColoringType` | — | L19474 |
| `uniformPatch` | `bool` | — | L19475 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L19476 | __init__(self: depthai.VppConfig) -> None |

**Nested Class:**

<a id="class-injectionparameters"></a>
#### class `InjectionParameters`  — L19423

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `confidenceThreshold` | `float` | — | L19424 |
| `kernelSize` | `int` | — | L19425 |
| `morphologyIterations` | `int` | — | L19426 |
| `textureThreshold` | `float` | — | L19427 |
| `useInjection` | `bool` | — | L19428 |
| `useMorphology` | `bool` | — | L19429 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L19430 | __init__(self: depthai.VppConfig.InjectionParameters) -> None |

**Nested Class:**

<a id="class-patchcoloringtype"></a>
#### class `PatchColoringType`  — L19433

> Members:

  RANDOM : Random patch coloring

  MAXDIST : Color with most distant color

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L19441 |
| `MAXDIST` | `ClassVar[VppConfig.PatchColoringType]` | `...` | L19442 |
| `RANDOM` | `ClassVar[VppConfig.PatchColoringType]` | `...` | L19443 |
| `__entries` | `ClassVar[dict]` | `...` | L19444 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L19445 | __init__(self: depthai.VppConfig.PatchColoringType, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L19447 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L19449 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L19451 | __index__(self: depthai.VppConfig.PatchColoringType) -> int |
| `def __int__(self) -> int` | `(self)` | L19453 | __int__(self: depthai.VppConfig.PatchColoringType) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L19455 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L19458 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L19464 | (arg0: depthai.VppConfig.PatchColoringType) -> int |

<a id="class-vppproperties"></a>
### class `VppProperties`  — L19479

> Specify properties for Vpp node

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `initialConfig` | `VppConfig` | — | L19481 |
| `numFramesPool` | `int` | — | L19482 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L19483 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-warpproperties"></a>
### class `WarpProperties`  — L19486

> Specify properties for Warp

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L19488 | Initialize self.  See help(type(self)) for accurate signature. |

<a id="class-xlinkconnection"></a>
### class `XLinkConnection`  — L19491

> Represents connection between host and device over XLink protocol

**🔧 Dunder Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self, arg0: DeviceInfo, arg1, std) -> None` | `(self, arg0: DeviceInfo, arg1, std)` | L19494 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: DeviceInfo, arg1: str) -> None` | `(self, arg0: DeviceInfo, arg1: str)` | L19505 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, arg0: DeviceInfo) -> None` | `(self, arg0: DeviceInfo)` | L19516 | __init__(*args, **kwargs) |

**⚡ Static Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@staticmethod` `def bootBootloader(devInfo: DeviceInfo) -> DeviceInfo` | `(devInfo: DeviceInfo)` | L19527 | bootBootloader(devInfo: depthai.DeviceInfo) -> depthai.DeviceInfo |
| `@staticmethod` `def getAllConnectedDevices(state: XLinkDeviceState = ..., skipInvalidDevices: bool = ..., timeoutMs: int = ...) -> list[DeviceInfo]` | `(state: XLinkDeviceState = ..., skipInvalidDevices: bool = ..., timeoutMs: int = ...)` | L19530 | getAllConnectedDevices(state: depthai.XLinkDeviceState = <XLinkDeviceState.X_LINK_ANY_STATE: 0>, skipInvalidDevices: bool = True, timeoutMs: int = 500) -> list[depthai.DeviceInfo] |
| `@staticmethod` `def getDeviceById(deviceId: str, state: XLinkDeviceState = ..., skipInvalidDevice: bool = ...) -> tuple[bool, DeviceInfo]` | `(deviceId: str, state: XLinkDeviceState = ..., skipInvalidDevice: bool = ...)` | L19533 | getDeviceById(deviceId: str, state: depthai.XLinkDeviceState = <XLinkDeviceState.X_LINK_ANY_STATE: 0>, skipInvalidDevice: bool = True) -> tuple[bool, depthai.DeviceInfo] |
| `@staticmethod` `def getFirstDevice(state: XLinkDeviceState = ..., skipInvalidDevice: bool = ...) -> tuple[bool, DeviceInfo]` | `(state: XLinkDeviceState = ..., skipInvalidDevice: bool = ...)` | L19536 | getFirstDevice(state: depthai.XLinkDeviceState = <XLinkDeviceState.X_LINK_ANY_STATE: 0>, skipInvalidDevice: bool = True) -> tuple[bool, depthai.DeviceInfo] |
| `@staticmethod` `def getGlobalProfilingData() -> ProfilingData` | `()` | L19539 | getGlobalProfilingData() -> depthai.ProfilingData |

<a id="class-xlinkdevicestate"></a>
### class `XLinkDeviceState`  — L19548

> Members:

X_LINK_ANY_STATE

X_LINK_BOOTED

X_LINK_UNBOOTED

X_LINK_BOOTLOADER

X_LINK_FLASH_BOOTED

X_LINK_BOOTED_NON_EXCLUSIVE

X_LINK_GATE

X_LINK_GATE_BOOTED

X_LINK_GATE_SETUP

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L19568 |
| `X_LINK_ANY_STATE` | `ClassVar[XLinkDeviceState]` | `...` | L19569 |
| `X_LINK_BOOTED` | `ClassVar[XLinkDeviceState]` | `...` | L19570 |
| `X_LINK_BOOTED_NON_EXCLUSIVE` | `ClassVar[XLinkDeviceState]` | `...` | L19571 |
| `X_LINK_BOOTLOADER` | `ClassVar[XLinkDeviceState]` | `...` | L19572 |
| `X_LINK_FLASH_BOOTED` | `ClassVar[XLinkDeviceState]` | `...` | L19573 |
| `X_LINK_GATE` | `ClassVar[XLinkDeviceState]` | `...` | L19574 |
| `X_LINK_GATE_BOOTED` | `ClassVar[XLinkDeviceState]` | `...` | L19575 |
| `X_LINK_GATE_SETUP` | `ClassVar[XLinkDeviceState]` | `...` | L19576 |
| `X_LINK_UNBOOTED` | `ClassVar[XLinkDeviceState]` | `...` | L19577 |
| `__entries` | `ClassVar[dict]` | `...` | L19578 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L19579 | __init__(self: depthai.XLinkDeviceState, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L19581 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L19583 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L19585 | __index__(self: depthai.XLinkDeviceState) -> int |
| `def __int__(self) -> int` | `(self)` | L19587 | __int__(self: depthai.XLinkDeviceState) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L19589 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L19592 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L19598 | (arg0: depthai.XLinkDeviceState) -> int |

<a id="class-xlinkerror"></a>
### class `XLinkError(RuntimeError)`  — L19601

<a id="class-xlinkerror_t"></a>
### class `XLinkError_t`  — L19603

> Members:

X_LINK_SUCCESS

X_LINK_ALREADY_OPEN

X_LINK_COMMUNICATION_NOT_OPEN

X_LINK_COMMUNICATION_FAIL

X_LINK_COMMUNICATION_UNKNOWN_ERROR

X_LINK_DEVICE_NOT_FOUND

X_LINK_TIMEOUT

X_LINK_ERROR

X_LINK_OUT_OF_MEMORY

X_LINK_INSUFFICIENT_PERMISSIONS

X_LINK_DEVICE_ALREADY_IN_USE

X_LINK_NOT_IMPLEMENTED

X_LINK_INIT_USB_ERROR

X_LINK_INIT_TCP_IP_ERROR

X_LINK_INIT_PCIE_ERROR

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L19635 |
| `X_LINK_ALREADY_OPEN` | `ClassVar[XLinkError_t]` | `...` | L19636 |
| `X_LINK_COMMUNICATION_FAIL` | `ClassVar[XLinkError_t]` | `...` | L19637 |
| `X_LINK_COMMUNICATION_NOT_OPEN` | `ClassVar[XLinkError_t]` | `...` | L19638 |
| `X_LINK_COMMUNICATION_UNKNOWN_ERROR` | `ClassVar[XLinkError_t]` | `...` | L19639 |
| `X_LINK_DEVICE_ALREADY_IN_USE` | `ClassVar[XLinkError_t]` | `...` | L19640 |
| `X_LINK_DEVICE_NOT_FOUND` | `ClassVar[XLinkError_t]` | `...` | L19641 |
| `X_LINK_ERROR` | `ClassVar[XLinkError_t]` | `...` | L19642 |
| `X_LINK_INIT_PCIE_ERROR` | `ClassVar[XLinkError_t]` | `...` | L19643 |
| `X_LINK_INIT_TCP_IP_ERROR` | `ClassVar[XLinkError_t]` | `...` | L19644 |
| `X_LINK_INIT_USB_ERROR` | `ClassVar[XLinkError_t]` | `...` | L19645 |
| `X_LINK_INSUFFICIENT_PERMISSIONS` | `ClassVar[XLinkError_t]` | `...` | L19646 |
| `X_LINK_NOT_IMPLEMENTED` | `ClassVar[XLinkError_t]` | `...` | L19647 |
| `X_LINK_OUT_OF_MEMORY` | `ClassVar[XLinkError_t]` | `...` | L19648 |
| `X_LINK_SUCCESS` | `ClassVar[XLinkError_t]` | `...` | L19649 |
| `X_LINK_TIMEOUT` | `ClassVar[XLinkError_t]` | `...` | L19650 |
| `__entries` | `ClassVar[dict]` | `...` | L19651 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L19652 | __init__(self: depthai.XLinkError_t, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L19654 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L19656 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L19658 | __index__(self: depthai.XLinkError_t) -> int |
| `def __int__(self) -> int` | `(self)` | L19660 | __int__(self: depthai.XLinkError_t) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L19662 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L19665 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L19671 | (arg0: depthai.XLinkError_t) -> int |

<a id="class-xlinkplatform"></a>
### class `XLinkPlatform`  — L19674

> Members:

X_LINK_ANY_PLATFORM

X_LINK_MYRIAD_2

X_LINK_MYRIAD_X

X_LINK_RVC3

X_LINK_RVC4

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L19686 |
| `X_LINK_ANY_PLATFORM` | `ClassVar[XLinkPlatform]` | `...` | L19687 |
| `X_LINK_MYRIAD_2` | `ClassVar[XLinkPlatform]` | `...` | L19688 |
| `X_LINK_MYRIAD_X` | `ClassVar[XLinkPlatform]` | `...` | L19689 |
| `X_LINK_RVC3` | `ClassVar[XLinkPlatform]` | `...` | L19690 |
| `X_LINK_RVC4` | `ClassVar[XLinkPlatform]` | `...` | L19691 |
| `__entries` | `ClassVar[dict]` | `...` | L19692 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L19693 | __init__(self: depthai.XLinkPlatform, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L19695 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L19697 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L19699 | __index__(self: depthai.XLinkPlatform) -> int |
| `def __int__(self) -> int` | `(self)` | L19701 | __int__(self: depthai.XLinkPlatform) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L19703 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L19706 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L19712 | (arg0: depthai.XLinkPlatform) -> int |

<a id="class-xlinkprotocol"></a>
### class `XLinkProtocol`  — L19715

> Members:

X_LINK_USB_VSC

X_LINK_USB_CDC

X_LINK_PCIE

X_LINK_TCP_IP

X_LINK_IPC

X_LINK_NMB_OF_PROTOCOLS

X_LINK_ANY_PROTOCOL

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L19731 |
| `X_LINK_ANY_PROTOCOL` | `ClassVar[XLinkProtocol]` | `...` | L19732 |
| `X_LINK_IPC` | `ClassVar[XLinkProtocol]` | `...` | L19733 |
| `X_LINK_NMB_OF_PROTOCOLS` | `ClassVar[XLinkProtocol]` | `...` | L19734 |
| `X_LINK_PCIE` | `ClassVar[XLinkProtocol]` | `...` | L19735 |
| `X_LINK_TCP_IP` | `ClassVar[XLinkProtocol]` | `...` | L19736 |
| `X_LINK_USB_CDC` | `ClassVar[XLinkProtocol]` | `...` | L19737 |
| `X_LINK_USB_VSC` | `ClassVar[XLinkProtocol]` | `...` | L19738 |
| `__entries` | `ClassVar[dict]` | `...` | L19739 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L19740 | __init__(self: depthai.XLinkProtocol, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L19742 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L19744 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L19746 | __index__(self: depthai.XLinkProtocol) -> int |
| `def __int__(self) -> int` | `(self)` | L19748 | __int__(self: depthai.XLinkProtocol) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L19750 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L19753 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L19759 | (arg0: depthai.XLinkProtocol) -> int |

<a id="class-xlinkreaderror"></a>
### class `XLinkReadError(XLinkError)`  — L19762

<a id="class-xlinkwriteerror"></a>
### class `XLinkWriteError(XLinkError)`  — L19764

<a id="class-yolodecodingfamily"></a>
### class `YoloDecodingFamily`  — L19766

> Members:

TLBR

v5AB

v3AB

R1AF

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L19776 |
| `R1AF` | `ClassVar[YoloDecodingFamily]` | `...` | L19777 |
| `TLBR` | `ClassVar[YoloDecodingFamily]` | `...` | L19778 |
| `__entries` | `ClassVar[dict]` | `...` | L19779 |
| `v3AB` | `ClassVar[YoloDecodingFamily]` | `...` | L19780 |
| `v5AB` | `ClassVar[YoloDecodingFamily]` | `...` | L19781 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L19782 | __init__(self: depthai.YoloDecodingFamily, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L19784 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L19786 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L19788 | __index__(self: depthai.YoloDecodingFamily) -> int |
| `def __int__(self) -> int` | `(self)` | L19790 | __int__(self: depthai.YoloDecodingFamily) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L19792 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L19795 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L19801 | (arg0: depthai.YoloDecodingFamily) -> int |

<a id="class-connectioninterface"></a>
### class `connectionInterface`  — L19804

> Members:

  USB

  ETHERNET

  WIFI

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L19814 |
| `ETHERNET` | `ClassVar[connectionInterface]` | `...` | L19815 |
| `USB` | `ClassVar[connectionInterface]` | `...` | L19816 |
| `WIFI` | `ClassVar[connectionInterface]` | `...` | L19817 |
| `__entries` | `ClassVar[dict]` | `...` | L19818 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L19819 | __init__(self: depthai.connectionInterface, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L19821 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L19823 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L19825 | __index__(self: depthai.connectionInterface) -> int |
| `def __int__(self) -> int` | `(self)` | L19827 | __int__(self: depthai.connectionInterface) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L19829 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L19832 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L19838 | (arg0: depthai.connectionInterface) -> int |

<a id="class-apriltag"></a>
### class `AprilTag(depthai.DeviceNode)`  — L19943

> AprilTag node.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.AprilTagProperties]]` | `...` | L19945 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L19946 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def initialConfig(self) -> depthai.AprilTagConfig` | `(self)` | L19991 | Initial config to use when calculating spatial location data. |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L19996 | Input AprilTagConfig message with ability to modify parameters in runtime. |
| `@property` `def inputImage(self) -> depthai.Node.Input` | `(self)` | L20002 | Input message with depth data used to retrieve spatial information about |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L20008 | Outputs AprilTags message that carries spatial location results. |
| `@property` `def passthroughInputImage(self) -> depthai.Node.Output` | `(self)` | L20013 | Passthrough message on which the calculation was performed. Suitable for when |

**🔹 Public Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getNumThreads(self) -> int` | `(self)` | L19948 | getNumThreads(self: depthai.node.AprilTag) -> int |
| `def getWaitForConfigInput(self) -> bool` | `(self)` | L19956 | getWaitForConfigInput(self: depthai.node.AprilTag) -> bool |
| `def runOnHost(self) -> bool` | `(self)` | L19962 | runOnHost(self: depthai.node.AprilTag) -> bool |
| `def setNumThreads(self, numThreads: int) -> None` | `(self, numThreads: int)` | L19967 | setNumThreads(self: depthai.node.AprilTag, numThreads: int) -> None |
| `def setRunOnHost(self, arg0: bool) -> None` | `(self, arg0: bool)` | L19975 | setRunOnHost(self: depthai.node.AprilTag, arg0: bool) -> None |
| `def setWaitForConfigInput(self, wait: bool) -> None` | `(self, wait: bool)` | L19981 | setWaitForConfigInput(self: depthai.node.AprilTag, wait: bool) -> None |

<a id="class-benchmarkin"></a>
### class `BenchmarkIn(depthai.DeviceNode)`  — L20019

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L20020 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L20044 | Receive messages as fast as possible |
| `@property` `def passthrough(self) -> depthai.Node.Output` | `(self)` | L20049 | Passthrough for input messages (so the node can be placed between other nodes) |
| `@property` `def report(self) -> depthai.Node.Output` | `(self)` | L20054 | Send a benchmark report when the set number of messages are received |

**🔹 Public Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def logReportsAsWarnings(self, logReportsAsWarnings: bool) -> None` | `(self, logReportsAsWarnings: bool)` | L20022 | logReportsAsWarnings(self: depthai.node.BenchmarkIn, logReportsAsWarnings: bool) -> None |
| `def measureIndividualLatencies(self, attachLatencies: bool) -> None` | `(self, attachLatencies: bool)` | L20027 | measureIndividualLatencies(self: depthai.node.BenchmarkIn, attachLatencies: bool) -> None |
| `def sendReportEveryNMessages(self, num: int) -> None` | `(self, num: int)` | L20032 | sendReportEveryNMessages(self: depthai.node.BenchmarkIn, num: int) -> None |
| `def setRunOnHost(self, runOnHost: bool) -> None` | `(self, runOnHost: bool)` | L20037 | setRunOnHost(self: depthai.node.BenchmarkIn, runOnHost: bool) -> None |

<a id="class-benchmarkout"></a>
### class `BenchmarkOut(depthai.DeviceNode)`  — L20059

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L20060 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L20082 | Message that will be sent repeatedly |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L20087 | Send messages out as fast as possible |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def setFps(self, fps: float) -> None` | `(self, fps: float)` | L20062 | setFps(self: depthai.node.BenchmarkOut, fps: float) -> None |
| `def setNumMessagesToSend(self, num: int) -> None` | `(self, num: int)` | L20067 | setNumMessagesToSend(self: depthai.node.BenchmarkOut, num: int) -> None |
| `def setRunOnHost(self, runOnHost: bool) -> None` | `(self, runOnHost: bool)` | L20075 | setRunOnHost(self: depthai.node.BenchmarkOut, runOnHost: bool) -> None |

<a id="class-camera"></a>
### class `Camera(depthai.DeviceNode)`  — L20092

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L20093 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def initialControl(self) -> depthai.CameraControl` | `(self)` | L20373 | Initial control options to apply to sensor |
| `@property` `def inputControl(self) -> depthai.Node.Input` | `(self)` | L20378 | Input for CameraControl message, which can modify camera parameters in runtime |
| `@property` `def mockIsp(self) -> depthai.Node.Input` | `(self)` | L20383 | Input for mocking 'isp' functionality on RVC2. Default queue is blocking with |
| `@property` `def raw(self) -> depthai.Node.Output` | `(self)` | L20389 | Outputs ImgFrame message that carries RAW10-packed (MIPI CSI-2 format) frame |

**🔹 Public Methods (22):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def build(self, boardSocket: depthai.CameraBoardSocket = ..., sensorResolution: tuple[int, int] | None = ..., sensorFps: float | None = ...) -> Camera` | `(self, boardSocket: depthai.CameraBoardSocket = ..., sensorResolution: tuple[int, int] | None = ..., sensorFps: float | None = ...)` | L20095 | build(*args, **kwargs) |
| `def getBoardSocket(self) -> depthai.CameraBoardSocket` | `(self)` | L20144 | getBoardSocket(self: depthai.node.Camera) -> depthai.CameraBoardSocket |
| `def getIspNumFramesPool(self) -> int` | `(self)` | L20152 | getIspNumFramesPool(self: depthai.node.Camera) -> int |
| `def getMaxSizePoolIsp(self) -> int` | `(self)` | L20160 | getMaxSizePoolIsp(self: depthai.node.Camera) -> int |
| `def getMaxSizePoolRaw(self) -> int` | `(self)` | L20168 | getMaxSizePoolRaw(self: depthai.node.Camera) -> int |
| `def getOutputsMaxSizePool(self) -> int | None` | `(self)` | L20176 | getOutputsMaxSizePool(self: depthai.node.Camera) -> Optional[int] |
| `def getOutputsNumFramesPool(self) -> int | None` | `(self)` | L20184 | getOutputsNumFramesPool(self: depthai.node.Camera) -> Optional[int] |
| `def getRawNumFramesPool(self) -> int` | `(self)` | L20192 | getRawNumFramesPool(self: depthai.node.Camera) -> int |
| `def getSensorType(self) -> depthai.CameraSensorType` | `(self)` | L20200 | getSensorType(self: depthai.node.Camera) -> depthai.CameraSensorType |
| `def requestFullResolutionOutput(self, type: depthai.ImgFrame.Type | None = ..., fps: float | None = ..., useHighestResolution: bool = ...) -> depthai.Node.Output` | `(self, type: depthai.ImgFrame.Type | None = ..., fps: float | None = ..., useHighestResolution: bool = ...)` | L20208 | requestFullResolutionOutput(self: depthai.node.Camera, type: Optional[depthai.ImgFrame.Type] = None, fps: Optional[float] = None, useHighestResolution: bool = False) -> depthai.Node.Output |
| `@overload` `def requestOutput(self, size: tuple[int, int], type: depthai.ImgFrame.Type | None = ..., resizeMode: depthai.ImgResizeMode = ..., fps: float | None = ..., enableUndistortion: bool | None = ...) -> depthai.Node.Output` | `(self, size: tuple[int, int], type: depthai.ImgFrame.Type | None = ..., resizeMode: depthai.ImgResizeMode = ..., fps: float | None = ..., enableUndistortion: bool | None = ...)` | L20228 | requestOutput(*args, **kwargs) |
| `@overload` `def requestOutput(self, capability: depthai.Capability, onHost: bool) -> depthai.Node.Output` | `(self, capability: depthai.Capability, onHost: bool)` | L20241 | requestOutput(*args, **kwargs) |
| `def setIspNumFramesPool(self, num: int) -> Camera` | `(self, num: int)` | L20253 | setIspNumFramesPool(self: depthai.node.Camera, num: int) -> depthai.node.Camera |
| `def setMaxSizePoolIsp(self, size: int) -> Camera` | `(self, size: int)` | L20265 | setMaxSizePoolIsp(self: depthai.node.Camera, size: int) -> depthai.node.Camera |
| `def setMaxSizePoolRaw(self, size: int) -> Camera` | `(self, size: int)` | L20276 | setMaxSizePoolRaw(self: depthai.node.Camera, size: int) -> depthai.node.Camera |
| `def setMaxSizePools(self, raw: int, isp: int, imgmanip: int) -> Camera` | `(self, raw: int, isp: int, imgmanip: int)` | L20287 | setMaxSizePools(self: depthai.node.Camera, raw: int, isp: int, imgmanip: int) -> depthai.node.Camera |
| `def setMockIsp(self, mockIsp: ReplayVideo) -> Camera` | `(self, mockIsp: ReplayVideo)` | L20304 | setMockIsp(self: depthai.node.Camera, mockIsp: depthai.node.ReplayVideo) -> depthai.node.Camera |
| `def setNumFramesPools(self, raw: int, isp: int, imgmanip: int) -> Camera` | `(self, raw: int, isp: int, imgmanip: int)` | L20312 | setNumFramesPools(self: depthai.node.Camera, raw: int, isp: int, imgmanip: int) -> depthai.node.Camera |
| `def setOutputsMaxSizePool(self, size: int) -> Camera` | `(self, size: int)` | L20330 | setOutputsMaxSizePool(self: depthai.node.Camera, size: int) -> depthai.node.Camera |
| `def setOutputsNumFramesPool(self, num: int) -> Camera` | `(self, num: int)` | L20341 | setOutputsNumFramesPool(self: depthai.node.Camera, num: int) -> depthai.node.Camera |
| `def setRawNumFramesPool(self, num: int) -> Camera` | `(self, num: int)` | L20352 | setRawNumFramesPool(self: depthai.node.Camera, num: int) -> depthai.node.Camera |
| `def setSensorType(self, sensorType: depthai.CameraSensorType) -> Camera` | `(self, sensorType: depthai.CameraSensorType)` | L20364 | setSensorType(self: depthai.node.Camera, sensorType: depthai.CameraSensorType) -> depthai.node.Camera |

<a id="class-colorcamera"></a>
### class `ColorCamera(depthai.DeviceNode)`  — L20397

> ColorCamera node. For use with color sensors.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.ColorCameraProperties]]` | `...` | L20399 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L20400 | __init__(self: depthai.node.ColorCamera) -> None |

**📌 Properties (8):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def frameEvent(self) -> depthai.Node.Output` | `(self)` | L20898 | Outputs metadata-only ImgFrame message as an early indicator of an incoming |
| `@property` `def initialControl(self) -> depthai.CameraControl` | `(self)` | L20909 | Initial control options to apply to sensor |
| `@property` `def inputControl(self) -> depthai.Node.Input` | `(self)` | L20914 | Input for CameraControl message, which can modify camera parameters in runtime |
| `@property` `def isp(self) -> depthai.Node.Output` | `(self)` | L20919 | Outputs ImgFrame message that carries YUV420 planar (I420/IYUV) frame data. |
| `@property` `def preview(self) -> depthai.Node.Output` | `(self)` | L20927 | Outputs ImgFrame message that carries BGR/RGB planar/interleaved encoded frame |
| `@property` `def raw(self) -> depthai.Node.Output` | `(self)` | L20935 | Outputs ImgFrame message that carries RAW10-packed (MIPI CSI-2 format) frame |
| `@property` `def still(self) -> depthai.Node.Output` | `(self)` | L20943 | Outputs ImgFrame message that carries NV12 encoded (YUV420, UV plane |
| `@property` `def video(self) -> depthai.Node.Output` | `(self)` | L20952 | Outputs ImgFrame message that carries NV12 encoded (YUV420, UV plane |

**🔹 Public Methods (65):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getBoardSocket(self) -> depthai.CameraBoardSocket` | `(self)` | L20402 | getBoardSocket(self: depthai.node.ColorCamera) -> depthai.CameraBoardSocket |
| `def getCamId(self) -> int` | `(self)` | L20410 | getCamId(self: depthai.node.ColorCamera) -> int |
| `def getCamera(self) -> str` | `(self)` | L20412 | getCamera(self: depthai.node.ColorCamera) -> str |
| `def getColorOrder(self) -> depthai.ColorCameraProperties.ColorOrder` | `(self)` | L20420 | getColorOrder(self: depthai.node.ColorCamera) -> depthai.ColorCameraProperties.ColorOrder |
| `def getFp16(self) -> bool` | `(self)` | L20425 | getFp16(self: depthai.node.ColorCamera) -> bool |
| `def getFps(self) -> float` | `(self)` | L20430 | getFps(self: depthai.node.ColorCamera) -> float |
| `def getFrameEventFilter(self) -> list[depthai.FrameEvent]` | `(self)` | L20438 | getFrameEventFilter(self: depthai.node.ColorCamera) -> list[depthai.FrameEvent] |
| `def getImageOrientation(self) -> depthai.CameraImageOrientation` | `(self)` | L20440 | getImageOrientation(self: depthai.node.ColorCamera) -> depthai.CameraImageOrientation |
| `def getInterleaved(self) -> bool` | `(self)` | L20445 | getInterleaved(self: depthai.node.ColorCamera) -> bool |
| `def getIspHeight(self) -> int` | `(self)` | L20450 | getIspHeight(self: depthai.node.ColorCamera) -> int |
| `def getIspNumFramesPool(self) -> int` | `(self)` | L20455 | getIspNumFramesPool(self: depthai.node.ColorCamera) -> int |
| `def getIspSize(self) -> tuple[int, int]` | `(self)` | L20460 | getIspSize(self: depthai.node.ColorCamera) -> tuple[int, int] |
| `def getIspWidth(self) -> int` | `(self)` | L20465 | getIspWidth(self: depthai.node.ColorCamera) -> int |
| `def getPreviewHeight(self) -> int` | `(self)` | L20470 | getPreviewHeight(self: depthai.node.ColorCamera) -> int |
| `def getPreviewKeepAspectRatio(self) -> bool` | `(self)` | L20475 | getPreviewKeepAspectRatio(self: depthai.node.ColorCamera) -> bool |
| `def getPreviewNumFramesPool(self) -> int` | `(self)` | L20484 | getPreviewNumFramesPool(self: depthai.node.ColorCamera) -> int |
| `def getPreviewSize(self) -> tuple[int, int]` | `(self)` | L20489 | getPreviewSize(self: depthai.node.ColorCamera) -> tuple[int, int] |
| `def getPreviewWidth(self) -> int` | `(self)` | L20494 | getPreviewWidth(self: depthai.node.ColorCamera) -> int |
| `def getRawNumFramesPool(self) -> int` | `(self)` | L20499 | getRawNumFramesPool(self: depthai.node.ColorCamera) -> int |
| `def getResolution(self) -> depthai.ColorCameraProperties.SensorResolution` | `(self)` | L20504 | getResolution(self: depthai.node.ColorCamera) -> depthai.ColorCameraProperties.SensorResolution |
| `def getResolutionHeight(self) -> int` | `(self)` | L20509 | getResolutionHeight(self: depthai.node.ColorCamera) -> int |
| `def getResolutionSize(self) -> tuple[int, int]` | `(self)` | L20514 | getResolutionSize(self: depthai.node.ColorCamera) -> tuple[int, int] |
| `def getResolutionWidth(self) -> int` | `(self)` | L20519 | getResolutionWidth(self: depthai.node.ColorCamera) -> int |
| `def getSensorCrop(self) -> tuple[float, float]` | `(self)` | L20524 | getSensorCrop(self: depthai.node.ColorCamera) -> tuple[float, float] |
| `def getSensorCropX(self) -> float` | `(self)` | L20530 | getSensorCropX(self: depthai.node.ColorCamera) -> float |
| `def getSensorCropY(self) -> float` | `(self)` | L20535 | getSensorCropY(self: depthai.node.ColorCamera) -> float |
| `def getStillHeight(self) -> int` | `(self)` | L20540 | getStillHeight(self: depthai.node.ColorCamera) -> int |
| `def getStillNumFramesPool(self) -> int` | `(self)` | L20545 | getStillNumFramesPool(self: depthai.node.ColorCamera) -> int |
| `def getStillSize(self) -> tuple[int, int]` | `(self)` | L20550 | getStillSize(self: depthai.node.ColorCamera) -> tuple[int, int] |
| `def getStillWidth(self) -> int` | `(self)` | L20555 | getStillWidth(self: depthai.node.ColorCamera) -> int |
| `def getVideoHeight(self) -> int` | `(self)` | L20560 | getVideoHeight(self: depthai.node.ColorCamera) -> int |
| `def getVideoNumFramesPool(self) -> int` | `(self)` | L20565 | getVideoNumFramesPool(self: depthai.node.ColorCamera) -> int |
| `def getVideoSize(self) -> tuple[int, int]` | `(self)` | L20570 | getVideoSize(self: depthai.node.ColorCamera) -> tuple[int, int] |
| `def getVideoWidth(self) -> int` | `(self)` | L20575 | getVideoWidth(self: depthai.node.ColorCamera) -> int |
| `def sensorCenterCrop(self) -> None` | `(self)` | L20580 | sensorCenterCrop(self: depthai.node.ColorCamera) -> None |
| `def setBoardSocket(self, boardSocket: depthai.CameraBoardSocket) -> None` | `(self, boardSocket: depthai.CameraBoardSocket)` | L20585 | setBoardSocket(self: depthai.node.ColorCamera, boardSocket: depthai.CameraBoardSocket) -> None |
| `def setCamId(self, arg0: int) -> None` | `(self, arg0: int)` | L20593 | setCamId(self: depthai.node.ColorCamera, arg0: int) -> None |
| `def setCamera(self, name: str) -> None` | `(self, name: str)` | L20595 | setCamera(self: depthai.node.ColorCamera, name: str) -> None |
| `def setColorOrder(self, colorOrder: depthai.ColorCameraProperties.ColorOrder) -> None` | `(self, colorOrder: depthai.ColorCameraProperties.ColorOrder)` | L20603 | setColorOrder(self: depthai.node.ColorCamera, colorOrder: depthai.ColorCameraProperties.ColorOrder) -> None |
| `def setFp16(self, fp16: bool) -> None` | `(self, fp16: bool)` | L20608 | setFp16(self: depthai.node.ColorCamera, fp16: bool) -> None |
| `def setFps(self, fps: float) -> None` | `(self, fps: float)` | L20613 | setFps(self: depthai.node.ColorCamera, fps: float) -> None |
| `def setFrameEventFilter(self, events: list[depthai.FrameEvent]) -> None` | `(self, events: list[depthai.FrameEvent])` | L20621 | setFrameEventFilter(self: depthai.node.ColorCamera, events: list[depthai.FrameEvent]) -> None |
| `def setImageOrientation(self, imageOrientation: depthai.CameraImageOrientation) -> None` | `(self, imageOrientation: depthai.CameraImageOrientation)` | L20623 | setImageOrientation(self: depthai.node.ColorCamera, imageOrientation: depthai.CameraImageOrientation) -> None |
| `def setInterleaved(self, interleaved: bool) -> None` | `(self, interleaved: bool)` | L20628 | setInterleaved(self: depthai.node.ColorCamera, interleaved: bool) -> None |
| `def setIsp3aFps(self, arg0: int) -> None` | `(self, arg0: int)` | L20633 | setIsp3aFps(self: depthai.node.ColorCamera, arg0: int) -> None |
| `def setIspNumFramesPool(self, arg0: int) -> None` | `(self, arg0: int)` | L20644 | setIspNumFramesPool(self: depthai.node.ColorCamera, arg0: int) -> None |
| `@overload` `def setIspScale(self, numerator: int, denominator: int) -> None` | `(self, numerator: int, denominator: int)` | L20650 | setIspScale(*args, **kwargs) |
| `@overload` `def setIspScale(self, scale: tuple[int, int]) -> None` | `(self, scale: tuple[int, int])` | L20676 | setIspScale(*args, **kwargs) |
| `@overload` `def setIspScale(self, horizNum: int, horizDenom: int, vertNum: int, vertDenom: int) -> None` | `(self, horizNum: int, horizDenom: int, vertNum: int, vertDenom: int)` | L20702 | setIspScale(*args, **kwargs) |
| `@overload` `def setIspScale(self, horizScale: tuple[int, int], vertScale: tuple[int, int]) -> None` | `(self, horizScale: tuple[int, int], vertScale: tuple[int, int])` | L20728 | setIspScale(*args, **kwargs) |
| `def setNumFramesPool(self, raw: int, isp: int, preview: int, video: int, still: int) -> None` | `(self, raw: int, isp: int, preview: int, video: int, still: int)` | L20753 | setNumFramesPool(self: depthai.node.ColorCamera, raw: int, isp: int, preview: int, video: int, still: int) -> None |
| `def setPreviewKeepAspectRatio(self, keep: bool) -> None` | `(self, keep: bool)` | L20758 | setPreviewKeepAspectRatio(self: depthai.node.ColorCamera, keep: bool) -> None |
| `def setPreviewNumFramesPool(self, arg0: int) -> None` | `(self, arg0: int)` | L20769 | setPreviewNumFramesPool(self: depthai.node.ColorCamera, arg0: int) -> None |
| `@overload` `def setPreviewSize(self, width: int, height: int) -> None` | `(self, width: int, height: int)` | L20775 | setPreviewSize(*args, **kwargs) |
| `@overload` `def setPreviewSize(self, size: tuple[int, int]) -> None` | `(self, size: tuple[int, int])` | L20788 | setPreviewSize(*args, **kwargs) |
| `def setRawNumFramesPool(self, arg0: int) -> None` | `(self, arg0: int)` | L20800 | setRawNumFramesPool(self: depthai.node.ColorCamera, arg0: int) -> None |
| `def setRawOutputPacked(self, packed: bool) -> None` | `(self, packed: bool)` | L20805 | setRawOutputPacked(self: depthai.node.ColorCamera, packed: bool) -> None |
| `def setResolution(self, resolution: depthai.ColorCameraProperties.SensorResolution) -> None` | `(self, resolution: depthai.ColorCameraProperties.SensorResolution)` | L20816 | setResolution(self: depthai.node.ColorCamera, resolution: depthai.ColorCameraProperties.SensorResolution) -> None |
| `def setSensorCrop(self, x: float, y: float) -> None` | `(self, x: float, y: float)` | L20821 | setSensorCrop(self: depthai.node.ColorCamera, x: float, y: float) -> None |
| `def setStillNumFramesPool(self, arg0: int) -> None` | `(self, arg0: int)` | L20835 | setStillNumFramesPool(self: depthai.node.ColorCamera, arg0: int) -> None |
| `@overload` `def setStillSize(self, width: int, height: int) -> None` | `(self, width: int, height: int)` | L20841 | setStillSize(*args, **kwargs) |
| `@overload` `def setStillSize(self, size: tuple[int, int]) -> None` | `(self, size: tuple[int, int])` | L20854 | setStillSize(*args, **kwargs) |
| `def setVideoNumFramesPool(self, arg0: int) -> None` | `(self, arg0: int)` | L20866 | setVideoNumFramesPool(self: depthai.node.ColorCamera, arg0: int) -> None |
| `@overload` `def setVideoSize(self, width: int, height: int) -> None` | `(self, width: int, height: int)` | L20872 | setVideoSize(*args, **kwargs) |
| `@overload` `def setVideoSize(self, size: tuple[int, int]) -> None` | `(self, size: tuple[int, int])` | L20885 | setVideoSize(*args, **kwargs) |

<a id="class-detectionnetwork"></a>
### class `DetectionNetwork(depthai.DeviceNodeGroup)`  — L20960

> DetectionNetwork, base for different network specializations

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, input: depthai.Node.Output, nnArchive: depthai.NNArchive, confidenceThreshold: float = ...) -> None` | `(self, input: depthai.Node.Output, nnArchive: depthai.NNArchive, confidenceThreshold: float = ...)` | L20962 | __init__(self: depthai.node.DetectionNetwork, input: depthai.Node.Output, nnArchive: depthai.NNArchive, confidenceThreshold: float = 0.5) -> None |

**📌 Properties (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def detectionParser(self) -> DetectionParser` | `(self)` | L21282 | (arg0: depthai.node.DetectionNetwork) -> depthai.node.DetectionParser |
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L21285 | Input message with data to be inferred upon |
| `@property` `def neuralNetwork(self) -> NeuralNetwork` | `(self)` | L21290 | (arg0: depthai.node.DetectionNetwork) -> depthai.node.NeuralNetwork |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L21293 | Outputs ImgDetections message that carries parsed detection results. Overrides |
| `@property` `def outNetwork(self) -> depthai.Node.Output` | `(self)` | L21299 | Outputs unparsed inference results. |
| `@property` `def passthrough(self) -> depthai.Node.Output` | `(self)` | L21304 | Passthrough message on which the inference was performed. |

**🔹 Public Methods (18):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def build(self, input: depthai.Node.Output, nnArchive: depthai.NNArchive, confidenceThreshold: float = ...) -> DetectionNetwork` | `(self, input: depthai.Node.Output, nnArchive: depthai.NNArchive, confidenceThreshold: float = ...)` | L20965 | build(*args, **kwargs) |
| `@overload` `def build(self, input: Camera, model: depthai.NNModelDescription, fps: float | None = ..., resizeMode: depthai.ImgResizeMode | None = ...) -> DetectionNetwork` | `(self, input: Camera, model: depthai.NNModelDescription, fps: float | None = ..., resizeMode: depthai.ImgResizeMode | None = ...)` | L21038 | build(*args, **kwargs) |
| `def getClasses(self) -> list[str] | None` | `(self)` | L21110 | getClasses(self: depthai.node.DetectionNetwork) -> Optional[list[str]] |
| `def getConfidenceThreshold(self) -> float` | `(self)` | L21112 | getConfidenceThreshold(self: depthai.node.DetectionNetwork) -> float |
| `def getNumInferenceThreads(self) -> int` | `(self)` | L21120 | getNumInferenceThreads(self: depthai.node.DetectionNetwork) -> int |
| `def setBackend(self, setBackend: str) -> None` | `(self, setBackend: str)` | L21128 | setBackend(self: depthai.node.DetectionNetwork, setBackend: str) -> None |
| `def setBackendProperties(self, setBackendProperties: dict[str, str]) -> None` | `(self, setBackendProperties: dict[str, str])` | L21136 | setBackendProperties(self: depthai.node.DetectionNetwork, setBackendProperties: dict[str, str]) -> None |
| `@overload` `def setBlob(self, blob: depthai.OpenVINO.Blob) -> None` | `(self, blob: depthai.OpenVINO.Blob)` | L21145 | setBlob(*args, **kwargs) |
| `@overload` `def setBlob(self, path: os.PathLike) -> None` | `(self, path: os.PathLike)` | L21168 | setBlob(*args, **kwargs) |
| `def setBlobPath(self, path: os.PathLike) -> None` | `(self, path: os.PathLike)` | L21190 | setBlobPath(self: depthai.node.DetectionNetwork, path: os.PathLike) -> None |
| `def setConfidenceThreshold(self, thresh: float) -> None` | `(self, thresh: float)` | L21201 | setConfidenceThreshold(self: depthai.node.DetectionNetwork, thresh: float) -> None |
| `def setFromModelZoo(self, description: depthai.NNModelDescription, useCached: bool = ...) -> None` | `(self, description: depthai.NNModelDescription, useCached: bool = ...)` | L21210 | setFromModelZoo(self: depthai.node.DetectionNetwork, description: depthai.NNModelDescription, useCached: bool = False) -> None |
| `def setModelPath(self, modelPath: os.PathLike) -> None` | `(self, modelPath: os.PathLike)` | L21221 | setModelPath(self: depthai.node.DetectionNetwork, modelPath: os.PathLike) -> None |
| `def setNNArchive(self, archive: depthai.NNArchive) -> None` | `(self, archive: depthai.NNArchive)` | L21229 | setNNArchive(*args, **kwargs) |
| `def setNumInferenceThreads(self, numThreads: int) -> None` | `(self, numThreads: int)` | L21249 | setNumInferenceThreads(self: depthai.node.DetectionNetwork, numThreads: int) -> None |
| `def setNumNCEPerInferenceThread(self, numNCEPerThread: int) -> None` | `(self, numNCEPerThread: int)` | L21257 | setNumNCEPerInferenceThread(self: depthai.node.DetectionNetwork, numNCEPerThread: int) -> None |
| `def setNumPoolFrames(self, numFrames: int) -> None` | `(self, numFrames: int)` | L21265 | setNumPoolFrames(self: depthai.node.DetectionNetwork, numFrames: int) -> None |
| `def setNumShavesPerInferenceThread(self, numShavesPerInferenceThread: int) -> None` | `(self, numShavesPerInferenceThread: int)` | L21273 | setNumShavesPerInferenceThread(self: depthai.node.DetectionNetwork, numShavesPerInferenceThread: int) -> None |

<a id="class-detectionparser"></a>
### class `DetectionParser(depthai.DeviceNode)`  — L21311

> DetectionParser node. Parses detection results from Mobilenet-SSD or YOLO neural
networks. @note If multiple detection heads are present in the NNArchive, only
one type is supported (either YOLO or Mobilenet-SSD) and the last one will be
used.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.DetectionParserProperties]]` | `...` | L21316 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L21317 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L21652 | Input NN results with detection data to parse Default queue is blocking with |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L21658 | Outputs image frame with detected edges |

**🔹 Public Methods (39):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def build(self, arg0: depthai.Node.Output, arg1: depthai.NNArchive) -> DetectionParser` | `(self, arg0: depthai.Node.Output, arg1: depthai.NNArchive)` | L21319 | build(self: depthai.node.DetectionParser, arg0: depthai.Node.Output, arg1: depthai.NNArchive) -> depthai.node.DetectionParser |
| `def getAnchorMasks(self) -> dict[str, list[int]]` | `(self)` | L21331 | getAnchorMasks(self: depthai.node.DetectionParser) -> dict[str, list[int]] |
| `def getAnchors(self) -> list[float]` | `(self)` | L21336 | getAnchors(self: depthai.node.DetectionParser) -> list[float] |
| `def getClasses(self) -> list[str] | None` | `(self)` | L21341 | getClasses(self: depthai.node.DetectionParser) -> Optional[list[str]] |
| `def getConfidenceThreshold(self) -> float` | `(self)` | L21346 | getConfidenceThreshold(self: depthai.node.DetectionParser) -> float |
| `def getCoordinateSize(self) -> int` | `(self)` | L21354 | getCoordinateSize(self: depthai.node.DetectionParser) -> int |
| `def getDecodeKeypoints(self) -> bool` | `(self)` | L21359 | getDecodeKeypoints(self: depthai.node.DetectionParser) -> bool |
| `def getDecodeSegmentation(self) -> bool` | `(self)` | L21364 | getDecodeSegmentation(self: depthai.node.DetectionParser) -> bool |
| `def getIouThreshold(self) -> float` | `(self)` | L21369 | getIouThreshold(self: depthai.node.DetectionParser) -> float |
| `def getNNFamily(self) -> depthai.DetectionNetworkType` | `(self)` | L21374 | getNNFamily(self: depthai.node.DetectionParser) -> depthai.DetectionNetworkType |
| `def getNkeypoints(self) -> int` | `(self)` | L21379 | getNkeypoints(self: depthai.node.DetectionParser) -> int |
| `def getNumClasses(self) -> int` | `(self)` | L21384 | getNumClasses(self: depthai.node.DetectionParser) -> int |
| `def getNumFramesPool(self) -> int` | `(self)` | L21389 | getNumFramesPool(self: depthai.node.DetectionParser) -> int |
| `def getStrides(self) -> list[int]` | `(self)` | L21394 | getStrides(self: depthai.node.DetectionParser) -> list[int] |
| `def getSubtype(self) -> str` | `(self)` | L21399 | getSubtype(self: depthai.node.DetectionParser) -> str |
| `def runOnHost(self) -> bool` | `(self)` | L21404 | runOnHost(self: depthai.node.DetectionParser) -> bool |
| `def setAnchorMasks(self, anchorMasks: dict[str, list[int]]) -> None` | `(self, anchorMasks: dict[str, list[int]])` | L21409 | setAnchorMasks(self: depthai.node.DetectionParser, anchorMasks: dict[str, list[int]]) -> None |
| `@overload` `def setAnchors(self, anchors: list[list[list[float]]]) -> None` | `(self, anchors: list[list[list[float]]])` | L21418 | setAnchors(*args, **kwargs) |
| `@overload` `def setAnchors(self, anchors: list[float]) -> None` | `(self, anchors: list[float])` | L21439 | setAnchors(*args, **kwargs) |
| `@overload` `def setBlob(self, blob: depthai.OpenVINO.Blob) -> None` | `(self, blob: depthai.OpenVINO.Blob)` | L21460 | setBlob(*args, **kwargs) |
| `@overload` `def setBlob(self, path: os.PathLike) -> None` | `(self, path: os.PathLike)` | L21483 | setBlob(*args, **kwargs) |
| `def setBlobPath(self, path: os.PathLike) -> None` | `(self, path: os.PathLike)` | L21505 | setBlobPath(self: depthai.node.DetectionParser, path: os.PathLike) -> None |
| `def setClasses(self, classes: list[str]) -> None` | `(self, classes: list[str])` | L21516 | setClasses(self: depthai.node.DetectionParser, classes: list[str]) -> None |
| `def setConfidenceThreshold(self, thresh: float) -> None` | `(self, thresh: float)` | L21524 | setConfidenceThreshold(self: depthai.node.DetectionParser, thresh: float) -> None |
| `def setCoordinateSize(self, coordinates: int) -> None` | `(self, coordinates: int)` | L21533 | setCoordinateSize(self: depthai.node.DetectionParser, coordinates: int) -> None |
| `def setDecodeKeypoints(self, decode: bool) -> None` | `(self, decode: bool)` | L21535 | setDecodeKeypoints(self: depthai.node.DetectionParser, decode: bool) -> None |
| `def setDecodeSegmentation(self, decode: bool) -> None` | `(self, decode: bool)` | L21541 | setDecodeSegmentation(self: depthai.node.DetectionParser, decode: bool) -> None |
| `@overload` `def setInputImageSize(self, width: int, height: int) -> None` | `(self, width: int, height: int)` | L21547 | setInputImageSize(*args, **kwargs) |
| `@overload` `def setInputImageSize(self, size: tuple[int, int]) -> None` | `(self, size: tuple[int, int])` | L21560 | setInputImageSize(*args, **kwargs) |
| `def setIouThreshold(self, thresh: float) -> None` | `(self, thresh: float)` | L21572 | setIouThreshold(self: depthai.node.DetectionParser, thresh: float) -> None |
| `def setKeypointEdges(self, edges) -> None` | `(self, edges)` | L21580 | setKeypointEdges(self: depthai.node.DetectionParser, edges: list[Annotated[list[int], FixedSize(2)]]) -> None |
| `def setNNArchive(self, nnArchive: depthai.NNArchive) -> None` | `(self, nnArchive: depthai.NNArchive)` | L21589 | setNNArchive(self: depthai.node.DetectionParser, nnArchive: depthai.NNArchive) -> None |
| `def setNNFamily(self, type: depthai.DetectionNetworkType) -> None` | `(self, type: depthai.DetectionNetworkType)` | L21598 | setNNFamily(self: depthai.node.DetectionParser, type: depthai.DetectionNetworkType) -> None |
| `def setNumClasses(self, numClasses: int) -> None` | `(self, numClasses: int)` | L21609 | setNumClasses(self: depthai.node.DetectionParser, numClasses: int) -> None |
| `def setNumFramesPool(self, numFramesPool: int) -> None` | `(self, numFramesPool: int)` | L21617 | setNumFramesPool(self: depthai.node.DetectionParser, numFramesPool: int) -> None |
| `def setNumKeypoints(self, numKeypoints: int) -> None` | `(self, numKeypoints: int)` | L21625 | setNumKeypoints(self: depthai.node.DetectionParser, numKeypoints: int) -> None |
| `def setRunOnHost(self, runOnHost: bool) -> None` | `(self, runOnHost: bool)` | L21630 | setRunOnHost(self: depthai.node.DetectionParser, runOnHost: bool) -> None |
| `def setStrides(self, strides: list[int]) -> None` | `(self, strides: list[int])` | L21636 | setStrides(self: depthai.node.DetectionParser, strides: list[int]) -> None |
| `def setSubtype(self, subtype: str) -> None` | `(self, subtype: str)` | L21641 | setSubtype(self: depthai.node.DetectionParser, subtype: str) -> None |

<a id="class-dynamiccalibration"></a>
### class `DynamicCalibration(depthai.DeviceNode)`  — L21663

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.DynamicCalibrationProperties]]` | `...` | L21664 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L21665 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def calibrationOutput(self) -> depthai.Node.Output` | `(self)` | L21676 | Output calibration quality result |
| `@property` `def coverageOutput(self) -> depthai.Node.Output` | `(self)` | L21681 | (self: depthai.node.DynamicCalibration) -> depthai.Node.Output |
| `@property` `def inputControl(self) -> depthai.Node.Input` | `(self)` | L21684 | Input DynamicCalibrationControl message with ability to modify parameters in |
| `@property` `def left(self) -> depthai.Node.Input` | `(self)` | L21690 | (arg0: depthai.node.DynamicCalibration) -> depthai.Node.Input |
| `@property` `def qualityOutput(self) -> depthai.Node.Output` | `(self)` | L21693 | (self: depthai.node.DynamicCalibration) -> depthai.Node.Output |
| `@property` `def right(self) -> depthai.Node.Input` | `(self)` | L21696 | (arg0: depthai.node.DynamicCalibration) -> depthai.Node.Input |

**🔹 Public Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def runOnHost(self) -> bool` | `(self)` | L21667 | runOnHost(self: depthai.node.DynamicCalibration) -> bool |
| `def setRunOnHost(self, runOnHost: bool) -> None` | `(self, runOnHost: bool)` | L21669 | setRunOnHost(self: depthai.node.DynamicCalibration, runOnHost: bool) -> None |

<a id="class-edgedetector"></a>
### class `EdgeDetector(depthai.DeviceNode)`  — L21699

> EdgeDetector node. Performs edge detection using 3x3 Sobel filter

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.EdgeDetectorProperties]]` | `...` | L21701 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L21702 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def initialConfig(self) -> depthai.EdgeDetectorConfig` | `(self)` | L21721 | Initial config to use for edge detection. |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L21726 | Input EdgeDetectorConfig message with ability to modify parameters in runtime. |
| `@property` `def inputImage(self) -> depthai.Node.Input` | `(self)` | L21732 | Input image on which edge detection is performed. Default queue is non-blocking |
| `@property` `def outputImage(self) -> depthai.Node.Output` | `(self)` | L21738 | Outputs image frame with detected edges |

**🔹 Public Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def setMaxOutputFrameSize(self, arg0: int) -> None` | `(self, arg0: int)` | L21704 | setMaxOutputFrameSize(self: depthai.node.EdgeDetector, arg0: int) -> None |
| `def setNumFramesPool(self, arg0: int) -> None` | `(self, arg0: int)` | L21712 | setNumFramesPool(self: depthai.node.EdgeDetector, arg0: int) -> None |

<a id="class-featuretracker"></a>
### class `FeatureTracker(depthai.DeviceNode)`  — L21743

> FeatureTracker node. Performs feature tracking and reidentification using motion
estimation between 2 consecutive frames.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.FeatureTrackerProperties]]` | `...` | L21746 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L21747 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def initialConfig(self) -> depthai.FeatureTrackerConfig` | `(self)` | L21762 | Initial config to use for feature tracking. |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L21767 | Input FeatureTrackerConfig message with ability to modify parameters in runtime. |
| `@property` `def inputImage(self) -> depthai.Node.Input` | `(self)` | L21773 | Input message with frame data on which feature tracking is performed. Default |
| `@property` `def outputFeatures(self) -> depthai.Node.Output` | `(self)` | L21779 | Outputs TrackedFeatures message that carries tracked features results. |
| `@property` `def passthroughInputImage(self) -> depthai.Node.Output` | `(self)` | L21784 | Passthrough message on which the calculation was performed. Suitable for when |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def setHardwareResources(self, numShaves: int, numMemorySlices: int) -> None` | `(self, numShaves: int, numMemorySlices: int)` | L21749 | setHardwareResources(self: depthai.node.FeatureTracker, numShaves: int, numMemorySlices: int) -> None |

<a id="class-hostnode"></a>
### class `HostNode(ThreadedHostNode)`  — L21790

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `createSubnode` | `ClassVar[Callable]` | `...` | L21793 |
| `__init_subclass__` | `ClassVar[method]` | `...` | L21794 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args) -> None` | `(self, *args)` | L21792 | — |
| `def __init__(self) -> None` | `(self)` | L21795 | __init__(self: depthai.node.HostNode) -> None |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def inputs(self) -> depthai.Node.InputMap` | `(self)` | L21815 | (arg0: depthai.node.HostNode) -> depthai.Node.InputMap |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L21818 | (self: depthai.node.HostNode) -> depthai.Node.Output |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def link_args(self, *args) -> None` | `(self, *args)` | L21791 | — |
| `def onStart(self) -> None` | `(self)` | L21797 | onStart(self: depthai.node.HostNode) -> None |
| `def onStop(self) -> None` | `(self)` | L21799 | onStop(self: depthai.node.HostNode) -> None |
| `def processGroup(self, arg0: depthai.MessageGroup) -> depthai.Buffer` | `(self, arg0: depthai.MessageGroup)` | L21801 | processGroup(self: depthai.node.HostNode, arg0: depthai.MessageGroup) -> depthai.Buffer |
| `def runSyncingOnDevice(self) -> None` | `(self)` | L21803 | runSyncingOnDevice(self: depthai.node.HostNode) -> None |
| `def runSyncingOnHost(self) -> None` | `(self)` | L21805 | runSyncingOnHost(self: depthai.node.HostNode) -> None |
| `def sendProcessingToPipeline(self, arg0: bool) -> None` | `(self, arg0: bool)` | L21807 | sendProcessingToPipeline(self: depthai.node.HostNode, arg0: bool) -> None |

<a id="class-imu"></a>
### class `IMU(depthai.DeviceNode)`  — L21821

> IMU node for BNO08X.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.IMUProperties]]` | `...` | L21823 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L21824 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def mockIn(self) -> depthai.Node.Input` | `(self)` | L21933 | Mock IMU data for replaying recorded data |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L21938 | Outputs IMUData message that carries IMU packets. |

**🔹 Public Methods (9):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def enableFirmwareUpdate(self, arg0: bool) -> None` | `(self, arg0: bool)` | L21826 | enableFirmwareUpdate(self: depthai.node.IMU, arg0: bool) -> None |
| `@overload` `def enableIMUSensor(self, sensorConfig: depthai.IMUSensorConfig) -> None` | `(self, sensorConfig: depthai.IMUSensorConfig)` | L21829 | enableIMUSensor(*args, **kwargs) |
| `@overload` `def enableIMUSensor(self, sensorConfigs: list[depthai.IMUSensorConfig]) -> None` | `(self, sensorConfigs: list[depthai.IMUSensorConfig])` | L21850 | enableIMUSensor(*args, **kwargs) |
| `@overload` `def enableIMUSensor(self, sensor: depthai.IMUSensor, reportRate: int) -> None` | `(self, sensor: depthai.IMUSensor, reportRate: int)` | L21871 | enableIMUSensor(*args, **kwargs) |
| `@overload` `def enableIMUSensor(self, sensors: list[depthai.IMUSensor], reportRate: int) -> None` | `(self, sensors: list[depthai.IMUSensor], reportRate: int)` | L21892 | enableIMUSensor(*args, **kwargs) |
| `def getBatchReportThreshold(self) -> int` | `(self)` | L21912 | getBatchReportThreshold(self: depthai.node.IMU) -> int |
| `def getMaxBatchReports(self) -> int` | `(self)` | L21917 | getMaxBatchReports(self: depthai.node.IMU) -> int |
| `def setBatchReportThreshold(self, batchReportThreshold: int) -> None` | `(self, batchReportThreshold: int)` | L21922 | setBatchReportThreshold(self: depthai.node.IMU, batchReportThreshold: int) -> None |
| `def setMaxBatchReports(self, maxBatchReports: int) -> None` | `(self, maxBatchReports: int)` | L21927 | setMaxBatchReports(self: depthai.node.IMU, maxBatchReports: int) -> None |

<a id="class-imagealign"></a>
### class `ImageAlign(depthai.DeviceNode)`  — L21943

> ImageAlign node. Calculates spatial location data on a set of ROIs on depth map.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.ImageAlignProperties]]` | `...` | L21945 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L21946 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def initialConfig(self) -> depthai.ImageAlignConfig` | `(self)` | L21985 | Initial config to use when calculating spatial location data. |
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L21990 | Input message. Default queue is non-blocking with size 4. |
| `@property` `def inputAlignTo(self) -> depthai.Node.Input` | `(self)` | L21995 | Input align to message. Default queue is non-blocking with size 1. |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L22000 | Input message with ability to modify parameters in runtime. Default queue is |
| `@property` `def outputAligned(self) -> depthai.Node.Output` | `(self)` | L22006 | Outputs ImgFrame message that is aligned to inputAlignTo. |
| `@property` `def passthroughInput(self) -> depthai.Node.Output` | `(self)` | L22011 | Passthrough message on which the calculation was performed. Suitable for when |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def runOnHost(self) -> bool` | `(self)` | L21948 | runOnHost(self: depthai.node.ImageAlign) -> bool |
| `def setInterpolation(self, interp: depthai.Interpolation) -> ImageAlign` | `(self, interp: depthai.Interpolation)` | L21953 | setInterpolation(self: depthai.node.ImageAlign, interp: depthai.Interpolation) -> depthai.node.ImageAlign |
| `def setNumFramesPool(self, numFramesPool: int) -> ImageAlign` | `(self, numFramesPool: int)` | L21958 | setNumFramesPool(self: depthai.node.ImageAlign, numFramesPool: int) -> depthai.node.ImageAlign |
| `def setNumShaves(self, numShaves: int) -> ImageAlign` | `(self, numShaves: int)` | L21963 | setNumShaves(self: depthai.node.ImageAlign, numShaves: int) -> depthai.node.ImageAlign |
| `def setOutKeepAspectRatio(self, keep: bool) -> ImageAlign` | `(self, keep: bool)` | L21968 | setOutKeepAspectRatio(self: depthai.node.ImageAlign, keep: bool) -> depthai.node.ImageAlign |
| `def setOutputSize(self, alignWidth: int, alignHeight: int) -> ImageAlign` | `(self, alignWidth: int, alignHeight: int)` | L21973 | setOutputSize(self: depthai.node.ImageAlign, alignWidth: int, alignHeight: int) -> depthai.node.ImageAlign |
| `def setRunOnHost(self, runOnHost: bool) -> None` | `(self, runOnHost: bool)` | L21978 | setRunOnHost(self: depthai.node.ImageAlign, runOnHost: bool) -> None |

<a id="class-imagefilters"></a>
### class `ImageFilters(depthai.DeviceNode)`  — L22017

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `MedianFilterParams` | `ClassVar[type[depthai.filters.params.MedianFilter]]` | `...` | L22018 |
| `SpatialFilterParams` | `ClassVar[type[depthai.filters.params.SpatialFilter]]` | `...` | L22019 |
| `SpeckleFilterParams` | `ClassVar[type[depthai.filters.params.SpeckleFilter]]` | `...` | L22020 |
| `TemporalFilterParams` | `ClassVar[type[depthai.filters.params.TemporalFilter]]` | `...` | L22021 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L22022 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def initialConfig(self) -> depthai.ImageFiltersConfig` | `(self)` | L22098 | Initial config for image filters. |
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L22103 | Input for image frames to be filtered |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L22108 | Config to be set for a specific filter |
| `@property` `def output(self) -> depthai.Node.Output` | `(self)` | L22113 | Filtered frame |

**🔹 Public Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def build(self, input: depthai.Node.Output, presetMode: depthai.ImageFiltersPresetMode = ...) -> ImageFilters` | `(self, input: depthai.Node.Output, presetMode: depthai.ImageFiltersPresetMode = ...)` | L22025 | build(*args, **kwargs) |
| `@overload` `def build(self, presetMode: depthai.ImageFiltersPresetMode = ...) -> ImageFilters` | `(self, presetMode: depthai.ImageFiltersPresetMode = ...)` | L22056 | build(*args, **kwargs) |
| `def runOnHost(self) -> bool` | `(self)` | L22086 | runOnHost(self: depthai.node.ImageFilters) -> bool |
| `def setRunOnHost(self, runOnHost: bool) -> None` | `(self, runOnHost: bool)` | L22091 | setRunOnHost(self: depthai.node.ImageFilters, runOnHost: bool) -> None |

<a id="class-imagemanip"></a>
### class `ImageManip(depthai.DeviceNode)`  — L22118

> ImageManip node. Capability to crop, resize, warp, ... incoming image frames

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L22187 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def initialConfig(self) -> depthai.ImageManipConfig` | `(self)` | L22230 | Initial config to use when manipulating frames |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L22235 | Input ImageManipConfig message with ability to modify parameters in runtime |
| `@property` `def inputImage(self) -> depthai.Node.Input` | `(self)` | L22240 | Input image to be modified |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L22245 | (self: depthai.node.ImageManip) -> depthai.Node.Output |

**🔹 Public Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def setBackend(self, arg0: ImageManip.Backend) -> ImageManip` | `(self, arg0: ImageManip.Backend)` | L22189 | setBackend(self: depthai.node.ImageManip, arg0: depthai.node.ImageManip.Backend) -> depthai.node.ImageManip |
| `def setMaxOutputFrameSize(self, arg0: int) -> None` | `(self, arg0: int)` | L22197 | setMaxOutputFrameSize(self: depthai.node.ImageManip, arg0: int) -> None |
| `def setNumFramesPool(self, arg0: int) -> None` | `(self, arg0: int)` | L22205 | setNumFramesPool(self: depthai.node.ImageManip, arg0: int) -> None |
| `def setPerformanceMode(self, arg0: ImageManip.PerformanceMode) -> ImageManip` | `(self, arg0: ImageManip.PerformanceMode)` | L22213 | setPerformanceMode(self: depthai.node.ImageManip, arg0: depthai.node.ImageManip.PerformanceMode) -> depthai.node.ImageManip |
| `def setRunOnHost(self, arg0: bool) -> ImageManip` | `(self, arg0: bool)` | L22221 | setRunOnHost(self: depthai.node.ImageManip, arg0: bool) -> depthai.node.ImageManip |

**Nested Class:**

<a id="class-backend"></a>
#### class `Backend`  — L22121

> Members:

HW

CPU

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L22127 |
| `CPU` | `ClassVar[ImageManip.Backend]` | `...` | L22128 |
| `HW` | `ClassVar[ImageManip.Backend]` | `...` | L22129 |
| `__entries` | `ClassVar[dict]` | `...` | L22130 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L22131 | __init__(self: depthai.node.ImageManip.Backend, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L22133 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L22135 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L22137 | __index__(self: depthai.node.ImageManip.Backend) -> int |
| `def __int__(self) -> int` | `(self)` | L22139 | __int__(self: depthai.node.ImageManip.Backend) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L22141 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L22144 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L22150 | (arg0: depthai.node.ImageManip.Backend) -> int |

**Nested Class:**

<a id="class-performancemode"></a>
#### class `PerformanceMode`  — L22153

> Members:

BALANCED

PERFORMANCE

LOW_POWER

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L22161 |
| `BALANCED` | `ClassVar[ImageManip.PerformanceMode]` | `...` | L22162 |
| `LOW_POWER` | `ClassVar[ImageManip.PerformanceMode]` | `...` | L22163 |
| `PERFORMANCE` | `ClassVar[ImageManip.PerformanceMode]` | `...` | L22164 |
| `__entries` | `ClassVar[dict]` | `...` | L22165 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L22166 | __init__(self: depthai.node.ImageManip.PerformanceMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L22168 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L22170 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L22172 | __index__(self: depthai.node.ImageManip.PerformanceMode) -> int |
| `def __int__(self) -> int` | `(self)` | L22174 | __int__(self: depthai.node.ImageManip.PerformanceMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L22176 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L22179 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L22185 | (arg0: depthai.node.ImageManip.PerformanceMode) -> int |

<a id="class-messagedemux"></a>
### class `MessageDemux(depthai.DeviceNode)`  — L22248

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.MessageDemuxProperties]]` | `...` | L22249 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L22250 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L22253 | Input message of type MessageGroup |
| `@property` `def outputs(self) -> depthai.Node.OutputMap` | `(self)` | L22258 | A map of outputs, where keys are same as in the input MessageGroup |

<a id="class-monocamera"></a>
### class `MonoCamera(depthai.DeviceNode)`  — L22263

> MonoCamera node. For use with grayscale sensors.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.MonoCameraProperties]]` | `...` | L22265 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L22266 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def frameEvent(self) -> depthai.Node.Output` | `(self)` | L22402 | (self: depthai.node.MonoCamera) -> depthai.Node.Output |
| `@property` `def initialControl(self) -> depthai.CameraControl` | `(self)` | L22405 | Initial control options to apply to sensor |
| `@property` `def inputControl(self) -> depthai.Node.Input` | `(self)` | L22410 | (self: depthai.node.MonoCamera) -> depthai.Node.Input |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L22413 | (self: depthai.node.MonoCamera) -> depthai.Node.Output |
| `@property` `def raw(self) -> depthai.Node.Output` | `(self)` | L22416 | (self: depthai.node.MonoCamera) -> depthai.Node.Output |

**🔹 Public Methods (23):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getBoardSocket(self) -> depthai.CameraBoardSocket` | `(self)` | L22268 | getBoardSocket(self: depthai.node.MonoCamera) -> depthai.CameraBoardSocket |
| `def getCamId(self) -> int` | `(self)` | L22276 | getCamId(self: depthai.node.MonoCamera) -> int |
| `def getCamera(self) -> str` | `(self)` | L22278 | getCamera(self: depthai.node.MonoCamera) -> str |
| `def getFps(self) -> float` | `(self)` | L22286 | getFps(self: depthai.node.MonoCamera) -> float |
| `def getFrameEventFilter(self) -> list[depthai.FrameEvent]` | `(self)` | L22294 | getFrameEventFilter(self: depthai.node.MonoCamera) -> list[depthai.FrameEvent] |
| `def getImageOrientation(self) -> depthai.CameraImageOrientation` | `(self)` | L22296 | getImageOrientation(self: depthai.node.MonoCamera) -> depthai.CameraImageOrientation |
| `def getNumFramesPool(self) -> int` | `(self)` | L22301 | getNumFramesPool(self: depthai.node.MonoCamera) -> int |
| `def getRawNumFramesPool(self) -> int` | `(self)` | L22306 | getRawNumFramesPool(self: depthai.node.MonoCamera) -> int |
| `def getResolution(self) -> depthai.MonoCameraProperties.SensorResolution` | `(self)` | L22311 | getResolution(self: depthai.node.MonoCamera) -> depthai.MonoCameraProperties.SensorResolution |
| `def getResolutionHeight(self) -> int` | `(self)` | L22316 | getResolutionHeight(self: depthai.node.MonoCamera) -> int |
| `def getResolutionSize(self) -> tuple[int, int]` | `(self)` | L22321 | getResolutionSize(self: depthai.node.MonoCamera) -> tuple[int, int] |
| `def getResolutionWidth(self) -> int` | `(self)` | L22326 | getResolutionWidth(self: depthai.node.MonoCamera) -> int |
| `def setBoardSocket(self, boardSocket: depthai.CameraBoardSocket) -> None` | `(self, boardSocket: depthai.CameraBoardSocket)` | L22331 | setBoardSocket(self: depthai.node.MonoCamera, boardSocket: depthai.CameraBoardSocket) -> None |
| `def setCamId(self, arg0: int) -> None` | `(self, arg0: int)` | L22339 | setCamId(self: depthai.node.MonoCamera, arg0: int) -> None |
| `def setCamera(self, name: str) -> None` | `(self, name: str)` | L22341 | setCamera(self: depthai.node.MonoCamera, name: str) -> None |
| `def setFps(self, fps: float) -> None` | `(self, fps: float)` | L22349 | setFps(self: depthai.node.MonoCamera, fps: float) -> None |
| `def setFrameEventFilter(self, events: list[depthai.FrameEvent]) -> None` | `(self, events: list[depthai.FrameEvent])` | L22357 | setFrameEventFilter(self: depthai.node.MonoCamera, events: list[depthai.FrameEvent]) -> None |
| `def setImageOrientation(self, imageOrientation: depthai.CameraImageOrientation) -> None` | `(self, imageOrientation: depthai.CameraImageOrientation)` | L22359 | setImageOrientation(self: depthai.node.MonoCamera, imageOrientation: depthai.CameraImageOrientation) -> None |
| `def setIsp3aFps(self, arg0: int) -> None` | `(self, arg0: int)` | L22364 | setIsp3aFps(self: depthai.node.MonoCamera, arg0: int) -> None |
| `def setNumFramesPool(self, arg0: int) -> None` | `(self, arg0: int)` | L22375 | setNumFramesPool(self: depthai.node.MonoCamera, arg0: int) -> None |
| `def setRawNumFramesPool(self, arg0: int) -> None` | `(self, arg0: int)` | L22380 | setRawNumFramesPool(self: depthai.node.MonoCamera, arg0: int) -> None |
| `def setRawOutputPacked(self, packed: bool) -> None` | `(self, packed: bool)` | L22385 | setRawOutputPacked(self: depthai.node.MonoCamera, packed: bool) -> None |
| `def setResolution(self, resolution: depthai.MonoCameraProperties.SensorResolution) -> None` | `(self, resolution: depthai.MonoCameraProperties.SensorResolution)` | L22396 | setResolution(self: depthai.node.MonoCamera, resolution: depthai.MonoCameraProperties.SensorResolution) -> None |

<a id="class-neuralassistedstereo"></a>
### class `NeuralAssistedStereo(depthai.DeviceNode)`  — L22419

> NeuralAssistedStereo node. Combines Neural Depth with VPP and traditional Stereo
Depth.

This composite node internally creates and connects: - Rectification node (full
resolution) - NeuralDepth node (low resolution depth estimation) - VPP node
(applies virtual projection pattern) - StereoDepth node (final depth computation
on VPP-enhanced images)

Pipeline structure: Left/Right Cameras → Rectification → [Full res to VPP] ↓
NeuralDepth (low res) → [disparity + confidence to VPP] ↓ VPP (combines neural
depth with full res images) ↓ StereoDepth → Final Depth Output

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L22431 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (17):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def depth(self) -> depthai.Node.Output` | `(self)` | L22436 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.Node.Output |
| `@property` `def disparity(self) -> depthai.Node.Output` | `(self)` | L22439 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.Node.Output |
| `@property` `def inputNeuralConfig(self) -> depthai.Node.Input` | `(self)` | L22442 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.Node.Input |
| `@property` `def inputStereoConfig(self) -> depthai.Node.Input` | `(self)` | L22445 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.Node.Input |
| `@property` `def inputVppConfig(self) -> depthai.Node.Input` | `(self)` | L22448 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.Node.Input |
| `@property` `def left(self) -> depthai.Node.Input` | `(self)` | L22451 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.Node.Input |
| `@property` `def neuralConfidence(self) -> depthai.Node.Output` | `(self)` | L22454 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.Node.Output |
| `@property` `def neuralDepth(self) -> NeuralDepth` | `(self)` | L22457 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.node.NeuralDepth |
| `@property` `def neuralDisparity(self) -> depthai.Node.Output` | `(self)` | L22460 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.Node.Output |
| `@property` `def rectification(self) -> Rectification` | `(self)` | L22463 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.node.Rectification |
| `@property` `def rectifiedLeft(self) -> depthai.Node.Output` | `(self)` | L22466 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.Node.Output |
| `@property` `def rectifiedRight(self) -> depthai.Node.Output` | `(self)` | L22469 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.Node.Output |
| `@property` `def right(self) -> depthai.Node.Input` | `(self)` | L22472 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.Node.Input |
| `@property` `def stereoDepth(self) -> StereoDepth` | `(self)` | L22475 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.node.StereoDepth |
| `@property` `def vpp(self) -> Vpp` | `(self)` | L22478 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.node.Vpp |
| `@property` `def vppLeft(self) -> depthai.Node.Output` | `(self)` | L22481 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.Node.Output |
| `@property` `def vppRight(self) -> depthai.Node.Output` | `(self)` | L22484 | (arg0: depthai.node.NeuralAssistedStereo) -> depthai.Node.Output |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def build(self, leftInput: depthai.Node.Output, rightInput: depthai.Node.Output, neuralModel: depthai.DeviceModelZoo = ..., rectifyImages: bool = ...) -> NeuralAssistedStereo` | `(self, leftInput: depthai.Node.Output, rightInput: depthai.Node.Output, neuralModel: depthai.DeviceModelZoo = ..., rectifyImages: bool = ...)` | L22433 | build(self: depthai.node.NeuralAssistedStereo, leftInput: depthai.Node.Output, rightInput: depthai.Node.Output, neuralModel: depthai.DeviceModelZoo = <DeviceModelZoo.???: 3>, rectifyImages: bool = True) -> depthai.node.NeuralAssistedStereo |

<a id="class-neuraldepth"></a>
### class `NeuralDepth(depthai.DeviceNode)`  — L22487

> NeuralDepth node. Compute depth from left-right image pair using neural network.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.NeuralDepthProperties]]` | `...` | L22489 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L22490 | Initialize self.  See help(type(self)) for accurate signature. |

**⚡ Static Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@staticmethod` `def getInputSize(model: depthai.DeviceModelZoo) -> tuple[int, int]` | `(model: depthai.DeviceModelZoo)` | L22495 | getInputSize(model: depthai.DeviceModelZoo) -> tuple[int, int] |

**📌 Properties (14):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def confidence(self) -> depthai.Node.Output` | `(self)` | L22506 | Output confidence ImgFrame |
| `@property` `def depth(self) -> depthai.Node.Output` | `(self)` | L22511 | Output depth ImgFrame |
| `@property` `def disparity(self) -> depthai.Node.Output` | `(self)` | L22516 | Output disparity ImgFrame |
| `@property` `def edge(self) -> depthai.Node.Output` | `(self)` | L22521 | Output edge ImgFrame |
| `@property` `def initialConfig(self) -> depthai.NeuralDepthConfig` | `(self)` | L22526 | Initial config to use for NeuralDepth. |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L22531 | Input config to modify parameters in runtime. |
| `@property` `def left(self) -> depthai.Node.Input` | `(self)` | L22536 | Input for left ImgFrame of left-right pair |
| `@property` `def messageDemux(self) -> MessageDemux` | `(self)` | L22541 | (arg0: depthai.node.NeuralDepth) -> depthai.node.MessageDemux |
| `@property` `def neuralNetwork(self) -> NeuralNetwork` | `(self)` | L22544 | (arg0: depthai.node.NeuralDepth) -> depthai.node.NeuralNetwork |
| `@property` `def rectification(self) -> Rectification` | `(self)` | L22547 | (arg0: depthai.node.NeuralDepth) -> depthai.node.Rectification |
| `@property` `def rectifiedLeft(self) -> depthai.Node.Output` | `(self)` | L22550 | Output for rectified left ImgFrame |
| `@property` `def rectifiedRight(self) -> depthai.Node.Output` | `(self)` | L22555 | Output for rectified right ImgFrame |
| `@property` `def right(self) -> depthai.Node.Input` | `(self)` | L22560 | Input for right ImgFrame of left-right pair |
| `@property` `def sync(self) -> Sync` | `(self)` | L22565 | (arg0: depthai.node.NeuralDepth) -> depthai.node.Sync |

**🔹 Public Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def build(self, leftInput: depthai.Node.Output, rightInput: depthai.Node.Output, model: depthai.DeviceModelZoo = ...) -> NeuralDepth` | `(self, leftInput: depthai.Node.Output, rightInput: depthai.Node.Output, model: depthai.DeviceModelZoo = ...)` | L22492 | build(self: depthai.node.NeuralDepth, leftInput: depthai.Node.Output, rightInput: depthai.Node.Output, model: depthai.DeviceModelZoo = <DeviceModelZoo.???: 2>) -> depthai.node.NeuralDepth |
| `def setRectification(self, enable: bool) -> NeuralDepth` | `(self, enable: bool)` | L22500 | setRectification(self: depthai.node.NeuralDepth, enable: bool) -> depthai.node.NeuralDepth |

<a id="class-neuralnetwork"></a>
### class `NeuralNetwork(depthai.DeviceNode)`  — L22568

> NeuralNetwork node. Runs a neural inference on input data.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.NeuralNetworkProperties]]` | `...` | L22570 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L22571 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L22850 | Input message with data to be inferred upon |
| `@property` `def inputs(self) -> depthai.Node.InputMap` | `(self)` | L22855 | Inputs mapped to network inputs. Useful for inferring from separate data sources |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L22861 | Outputs NNData message that carries inference results |
| `@property` `def passthrough(self) -> depthai.Node.Output` | `(self)` | L22866 | Passthrough message on which the inference was performed. |
| `@property` `def passthroughs(self) -> depthai.Node.OutputMap` | `(self)` | L22873 | Passthroughs which correspond to specified input |

**🔹 Public Methods (16):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def build(self, input: depthai.Node.Output, nnArchive: depthai.NNArchive) -> NeuralNetwork` | `(self, input: depthai.Node.Output, nnArchive: depthai.NNArchive)` | L22573 | build(*args, **kwargs) |
| `def getNNArchive(self) -> depthai.NNArchive | None` | `(self)` | L22678 | getNNArchive(self: depthai.node.NeuralNetwork) -> Optional[depthai.NNArchive] |
| `def getNumInferenceThreads(self) -> int` | `(self)` | L22686 | getNumInferenceThreads(self: depthai.node.NeuralNetwork) -> int |
| `def setBackend(self, setBackend: str) -> None` | `(self, setBackend: str)` | L22694 | setBackend(self: depthai.node.NeuralNetwork, setBackend: str) -> None |
| `def setBackendProperties(self, setBackendProperties: dict[str, str]) -> None` | `(self, setBackendProperties: dict[str, str])` | L22702 | setBackendProperties(self: depthai.node.NeuralNetwork, setBackendProperties: dict[str, str]) -> None |
| `@overload` `def setBlob(self, blob: depthai.OpenVINO.Blob) -> None` | `(self, blob: depthai.OpenVINO.Blob)` | L22711 | setBlob(*args, **kwargs) |
| `@overload` `def setBlob(self, path: os.PathLike) -> None` | `(self, path: os.PathLike)` | L22734 | setBlob(*args, **kwargs) |
| `def setBlobPath(self, path: os.PathLike) -> None` | `(self, path: os.PathLike)` | L22756 | setBlobPath(self: depthai.node.NeuralNetwork, path: os.PathLike) -> None |
| `def setFromModelZoo(self, description: depthai.NNModelDescription, useCached: bool) -> None` | `(self, description: depthai.NNModelDescription, useCached: bool)` | L22767 | setFromModelZoo(self: depthai.node.NeuralNetwork, description: depthai.NNModelDescription, useCached: bool) -> None |
| `def setModelFromDeviceZoo(self, model: depthai.DeviceModelZoo) -> None` | `(self, model: depthai.DeviceModelZoo)` | L22778 | setModelFromDeviceZoo(self: depthai.node.NeuralNetwork, model: depthai.DeviceModelZoo) -> None |
| `def setModelPath(self, modelPath: os.PathLike) -> None` | `(self, modelPath: os.PathLike)` | L22787 | setModelPath(self: depthai.node.NeuralNetwork, modelPath: os.PathLike) -> None |
| `def setNNArchive(self, nnArchive: depthai.NNArchive) -> None` | `(self, nnArchive: depthai.NNArchive)` | L22795 | setNNArchive(*args, **kwargs) |
| `def setNumInferenceThreads(self, numThreads: int) -> None` | `(self, numThreads: int)` | L22817 | setNumInferenceThreads(self: depthai.node.NeuralNetwork, numThreads: int) -> None |
| `def setNumNCEPerInferenceThread(self, numNCEPerThread: int) -> None` | `(self, numNCEPerThread: int)` | L22825 | setNumNCEPerInferenceThread(self: depthai.node.NeuralNetwork, numNCEPerThread: int) -> None |
| `def setNumPoolFrames(self, numFrames: int) -> None` | `(self, numFrames: int)` | L22833 | setNumPoolFrames(self: depthai.node.NeuralNetwork, numFrames: int) -> None |
| `def setNumShavesPerInferenceThread(self, numShavesPerInferenceThread: int) -> None` | `(self, numShavesPerInferenceThread: int)` | L22841 | setNumShavesPerInferenceThread(self: depthai.node.NeuralNetwork, numShavesPerInferenceThread: int) -> None |

<a id="class-objecttracker"></a>
### class `ObjectTracker(depthai.DeviceNode)`  — L22878

> ObjectTracker node. Performs object tracking using Kalman filter and hungarian
algorithm.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.ObjectTrackerProperties]]` | `...` | L22881 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L22882 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (8):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L22965 | Input ObjectTrackerConfig message with ability to modify parameters at runtime. |
| `@property` `def inputDetectionFrame(self) -> depthai.Node.Input` | `(self)` | L22971 | Input ImgFrame message on which object detection was performed. Default queue is |
| `@property` `def inputDetections(self) -> depthai.Node.Input` | `(self)` | L22977 | Input message with image detection from neural network. Default queue is non- |
| `@property` `def inputTrackerFrame(self) -> depthai.Node.Input` | `(self)` | L22983 | Input ImgFrame message on which tracking will be performed. RGBp, BGRp, NV12, |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L22989 | Outputs Tracklets message that carries object tracking results. |
| `@property` `def passthroughDetectionFrame(self) -> depthai.Node.Output` | `(self)` | L22994 | Passthrough ImgFrame message on which object detection was performed. Suitable |
| `@property` `def passthroughDetections(self) -> depthai.Node.Output` | `(self)` | L23000 | Passthrough image detections message from neural network output. Suitable for |
| `@property` `def passthroughTrackerFrame(self) -> depthai.Node.Output` | `(self)` | L23006 | Passthrough ImgFrame message on which tracking was performed. Suitable for when |

**🔹 Public Methods (10):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def setDetectionLabelsToTrack(self, labels: list[int]) -> None` | `(self, labels: list[int])` | L22884 | setDetectionLabelsToTrack(self: depthai.node.ObjectTracker, labels: list[int]) -> None |
| `def setMaxObjectsToTrack(self, maxObjectsToTrack: int) -> None` | `(self, maxObjectsToTrack: int)` | L22893 | setMaxObjectsToTrack(self: depthai.node.ObjectTracker, maxObjectsToTrack: int) -> None |
| `def setOcclusionRatioThreshold(self, threshold: float) -> None` | `(self, threshold: float)` | L22902 | setOcclusionRatioThreshold(self: depthai.node.ObjectTracker, threshold: float) -> None |
| `def setRunOnHost(self, runOnHost: bool) -> None` | `(self, runOnHost: bool)` | L22910 | setRunOnHost(self: depthai.node.ObjectTracker, runOnHost: bool) -> None |
| `def setTrackerIdAssignmentPolicy(self, type: depthai.TrackerIdAssignmentPolicy) -> None` | `(self, type: depthai.TrackerIdAssignmentPolicy)` | L22916 | setTrackerIdAssignmentPolicy(self: depthai.node.ObjectTracker, type: depthai.TrackerIdAssignmentPolicy) -> None |
| `def setTrackerThreshold(self, threshold: float) -> None` | `(self, threshold: float)` | L22924 | setTrackerThreshold(self: depthai.node.ObjectTracker, threshold: float) -> None |
| `def setTrackerType(self, type: depthai.TrackerType) -> None` | `(self, type: depthai.TrackerType)` | L22933 | setTrackerType(self: depthai.node.ObjectTracker, type: depthai.TrackerType) -> None |
| `def setTrackingPerClass(self, trackingPerClass: bool) -> None` | `(self, trackingPerClass: bool)` | L22941 | setTrackingPerClass(self: depthai.node.ObjectTracker, trackingPerClass: bool) -> None |
| `def setTrackletBirthThreshold(self, trackletBirthThreshold: int) -> None` | `(self, trackletBirthThreshold: int)` | L22946 | setTrackletBirthThreshold(self: depthai.node.ObjectTracker, trackletBirthThreshold: int) -> None |
| `def setTrackletMaxLifespan(self, trackletMaxLifespan: int) -> None` | `(self, trackletMaxLifespan: int)` | L22955 | setTrackletMaxLifespan(self: depthai.node.ObjectTracker, trackletMaxLifespan: int) -> None |

<a id="class-pointcloud"></a>
### class `PointCloud(depthai.DeviceNode)`  — L23012

> PointCloud node. Computes point cloud from depth frames.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.PointCloudProperties]]` | `...` | L23014 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L23015 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def initialConfig(self) -> depthai.PointCloudConfig` | `(self)` | L23026 | Initial config to use when computing the point cloud. |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L23031 | Input PointCloudConfig message with ability to modify parameters in runtime. |
| `@property` `def inputDepth(self) -> depthai.Node.Input` | `(self)` | L23037 | Input message with depth data used to create the point cloud. Default queue is |
| `@property` `def outputPointCloud(self) -> depthai.Node.Output` | `(self)` | L23043 | Outputs PointCloudData message |
| `@property` `def passthroughDepth(self) -> depthai.Node.Output` | `(self)` | L23048 | Passthrough depth from which the point cloud was calculated. Suitable for when |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def setNumFramesPool(self, arg0: int) -> None` | `(self, arg0: int)` | L23017 | setNumFramesPool(self: depthai.node.PointCloud, arg0: int) -> None |

<a id="class-rgbd"></a>
### class `RGBD(ThreadedHostNode)`  — L23054

> RGBD node. Combines depth and color frames into a single point cloud.

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L23056 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def inColor(self) -> depthai.Node.Input` | `(self)` | L23155 | (arg0: depthai.node.RGBD) -> depthai.Node.Input |
| `@property` `def inDepth(self) -> depthai.Node.Input` | `(self)` | L23158 | (arg0: depthai.node.RGBD) -> depthai.Node.Input |
| `@property` `def pcl(self) -> depthai.Node.Output` | `(self)` | L23161 | Output point cloud. |
| `@property` `def rgbd(self) -> depthai.Node.Output` | `(self)` | L23166 | Output RGBD frames. |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def build(self) -> RGBD` | `(self)` | L23059 | build(*args, **kwargs) |
| `@overload` `def build(self, autocreate: bool, mode: StereoDepth.PresetMode = ..., size: tuple[int, int] = ..., fps: float | None = ...) -> RGBD` | `(self, autocreate: bool, mode: StereoDepth.PresetMode = ..., size: tuple[int, int] = ..., fps: float | None = ...)` | L23093 | build(*args, **kwargs) |
| `def printDevices(self) -> None` | `(self)` | L23126 | printDevices(self: depthai.node.RGBD) -> None |
| `def setDepthUnits(self, units: depthai.DepthUnit) -> None` | `(self, units: depthai.DepthUnit)` | L23131 | setDepthUnits(self: depthai.node.RGBD, units: depthai.DepthUnit) -> None |
| `def useCPU(self) -> None` | `(self)` | L23133 | useCPU(self: depthai.node.RGBD) -> None |
| `def useCPUMT(self, numThreads: int = ...) -> None` | `(self, numThreads: int = ...)` | L23138 | useCPUMT(self: depthai.node.RGBD, numThreads: int = 2) -> None |
| `def useGPU(self, device: int = ...) -> None` | `(self, device: int = ...)` | L23146 | useGPU(self: depthai.node.RGBD, device: int = 0) -> None |

<a id="class-rtabmapslam"></a>
### class `RTABMapSLAM(ThreadedHostNode)`  — L23171

> RTABMap SLAM node. Performs SLAM on given odometry pose, rectified frame and
depth frame.

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L23174 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (13):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def depth(self) -> depthai.Node.Input` | `(self)` | L23248 | (arg0: depthai.node.RTABMapSLAM) -> depthai.Node.Input |
| `@property` `def features(self) -> depthai.Node.Input` | `(self)` | L23251 | Input tracked features on which SLAM is performed (optional). |
| `@property` `def groundPCL(self) -> depthai.Node.Output` | `(self)` | L23256 | Output ground point cloud. |
| `@property` `def obstaclePCL(self) -> depthai.Node.Output` | `(self)` | L23261 | Output obstacle point cloud. |
| `@property` `def occupancyGridMap(self) -> depthai.Node.Output` | `(self)` | L23266 | Output occupancy grid map. |
| `@property` `def odom(self) -> depthai.Node.Input` | `(self)` | L23271 | Input odometry pose. |
| `@property` `def odomCorrection(self) -> depthai.Node.Output` | `(self)` | L23276 | Output odometry correction (map to odom). |
| `@property` `def passthroughDepth(self) -> depthai.Node.Output` | `(self)` | L23281 | Output passthrough depth image. |
| `@property` `def passthroughFeatures(self) -> depthai.Node.Output` | `(self)` | L23286 | Output passthrough features. |
| `@property` `def passthroughOdom(self) -> depthai.Node.Output` | `(self)` | L23291 | Output passthrough odometry pose. |
| `@property` `def passthroughRect(self) -> depthai.Node.Output` | `(self)` | L23296 | Output passthrough rectified image. |
| `@property` `def rect(self) -> depthai.Node.Input` | `(self)` | L23301 | (arg0: depthai.node.RTABMapSLAM) -> depthai.Node.Input |
| `@property` `def transform(self) -> depthai.Node.Output` | `(self)` | L23304 | Output transform. |

**🔹 Public Methods (16):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getLocalTransform(self) -> depthai.TransformData` | `(self)` | L23176 | getLocalTransform(self: depthai.node.RTABMapSLAM) -> depthai.TransformData |
| `def saveDatabase(self) -> None` | `(self)` | L23178 | saveDatabase(self: depthai.node.RTABMapSLAM) -> None |
| `def setAlphaScaling(self, alpha: float) -> None` | `(self, alpha: float)` | L23180 | setAlphaScaling(self: depthai.node.RTABMapSLAM, alpha: float) -> None |
| `def setDatabasePath(self, path: str) -> None` | `(self, path: str)` | L23185 | setDatabasePath(self: depthai.node.RTABMapSLAM, path: str) -> None |
| `def setFreq(self, f: float) -> None` | `(self, f: float)` | L23190 | setFreq(self: depthai.node.RTABMapSLAM, f: float) -> None |
| `def setLoadDatabaseOnStart(self, load: bool) -> None` | `(self, load: bool)` | L23195 | setLoadDatabaseOnStart(self: depthai.node.RTABMapSLAM, load: bool) -> None |
| `def setLocalTransform(self, transform: depthai.TransformData) -> None` | `(self, transform: depthai.TransformData)` | L23200 | setLocalTransform(self: depthai.node.RTABMapSLAM, transform: depthai.TransformData) -> None |
| `def setParams(self, params: dict[str, str]) -> None` | `(self, params: dict[str, str])` | L23202 | setParams(self: depthai.node.RTABMapSLAM, params: dict[str, str]) -> None |
| `def setPublishGrid(self, publish: bool) -> None` | `(self, publish: bool)` | L23207 | setPublishGrid(self: depthai.node.RTABMapSLAM, publish: bool) -> None |
| `def setPublishGroundCloud(self, publish: bool) -> None` | `(self, publish: bool)` | L23212 | setPublishGroundCloud(self: depthai.node.RTABMapSLAM, publish: bool) -> None |
| `def setPublishObstacleCloud(self, publish: bool) -> None` | `(self, publish: bool)` | L23217 | setPublishObstacleCloud(self: depthai.node.RTABMapSLAM, publish: bool) -> None |
| `def setSaveDatabaseOnClose(self, save: bool) -> None` | `(self, save: bool)` | L23222 | setSaveDatabaseOnClose(self: depthai.node.RTABMapSLAM, save: bool) -> None |
| `def setSaveDatabasePeriod(self, period: float) -> None` | `(self, period: float)` | L23227 | setSaveDatabasePeriod(self: depthai.node.RTABMapSLAM, period: float) -> None |
| `def setSaveDatabasePeriodically(self, save: bool) -> None` | `(self, save: bool)` | L23232 | setSaveDatabasePeriodically(self: depthai.node.RTABMapSLAM, save: bool) -> None |
| `def setUseFeatures(self, useFeatures: bool) -> None` | `(self, useFeatures: bool)` | L23237 | setUseFeatures(self: depthai.node.RTABMapSLAM, useFeatures: bool) -> None |
| `def triggerNewMap(self) -> None` | `(self)` | L23242 | triggerNewMap(self: depthai.node.RTABMapSLAM) -> None |

<a id="class-rtabmapvio"></a>
### class `RTABMapVIO(ThreadedHostNode)`  — L23309

> RTABMap Visual Inertial Odometry node. Performs VIO on rectified frame, depth
frame and IMU data.

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L23312 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (8):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def depth(self) -> depthai.Node.Input` | `(self)` | L23332 | (arg0: depthai.node.RTABMapVIO) -> depthai.Node.Input |
| `@property` `def features(self) -> depthai.Node.Input` | `(self)` | L23335 | Input tracked features on which VIO is performed (optional). |
| `@property` `def imu(self) -> depthai.Node.Input` | `(self)` | L23340 | Input IMU data. |
| `@property` `def passthroughDepth(self) -> depthai.Node.Output` | `(self)` | L23345 | Passthrough depth frame. |
| `@property` `def passthroughFeatures(self) -> depthai.Node.Output` | `(self)` | L23350 | Passthrough features. |
| `@property` `def passthroughRect(self) -> depthai.Node.Output` | `(self)` | L23355 | Passthrough rectified frame. |
| `@property` `def rect(self) -> depthai.Node.Input` | `(self)` | L23360 | (arg0: depthai.node.RTABMapVIO) -> depthai.Node.Input |
| `@property` `def transform(self) -> depthai.Node.Output` | `(self)` | L23363 | Output transform. |

**🔹 Public Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def reset(self, transform: depthai.TransformData) -> None` | `(self, transform: depthai.TransformData)` | L23314 | reset(self: depthai.node.RTABMapVIO, transform: depthai.TransformData) -> None |
| `def setLocalTransform(self, transform: depthai.TransformData) -> None` | `(self, transform: depthai.TransformData)` | L23319 | setLocalTransform(self: depthai.node.RTABMapVIO, transform: depthai.TransformData) -> None |
| `def setParams(self, params: dict[str, str]) -> None` | `(self, params: dict[str, str])` | L23321 | setParams(self: depthai.node.RTABMapVIO, params: dict[str, str]) -> None |
| `def setUseFeatures(self, useFeatures: bool) -> None` | `(self, useFeatures: bool)` | L23326 | setUseFeatures(self: depthai.node.RTABMapVIO, useFeatures: bool) -> None |

<a id="class-recordmetadataonly"></a>
### class `RecordMetadataOnly(ThreadedHostNode)`  — L23368

> RecordMetadataOnly node, used to record a source stream to a file

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L23370 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L23381 | Input IMU messages to be recorded (will support other types in the future) |

**🔹 Public Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getCompressionLevel(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L23372 | getCompressionLevel(self: depthai.node.RecordMetadataOnly) -> dai::RecordConfig::CompressionLevel |
| `def getRecordFile(self) -> os.PathLike` | `(self)` | L23374 | getRecordFile(self: depthai.node.RecordMetadataOnly) -> os.PathLike |
| `def setCompressionLevel(self, compressionLevel) -> RecordMetadataOnly` | `(self, compressionLevel)` | L23376 | setCompressionLevel(self: depthai.node.RecordMetadataOnly, compressionLevel: dai::RecordConfig::CompressionLevel) -> depthai.node.RecordMetadataOnly |
| `def setRecordFile(self, recordFile: os.PathLike) -> RecordMetadataOnly` | `(self, recordFile: os.PathLike)` | L23378 | setRecordFile(self: depthai.node.RecordMetadataOnly, recordFile: os.PathLike) -> depthai.node.RecordMetadataOnly |

<a id="class-recordvideo"></a>
### class `RecordVideo(ThreadedHostNode)`  — L23388

> RecordVideo node, used to record a video source stream to a file

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L23390 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L23405 | Input for ImgFrame or EncodedFrame messages to be recorded |

**🔹 Public Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getCompressionLevel(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L23392 | getCompressionLevel(self: depthai.node.RecordVideo) -> dai::RecordConfig::CompressionLevel |
| `def getRecordMetadataFile(self) -> os.PathLike` | `(self)` | L23394 | getRecordMetadataFile(self: depthai.node.RecordVideo) -> os.PathLike |
| `def getRecordVideoFile(self) -> os.PathLike` | `(self)` | L23396 | getRecordVideoFile(self: depthai.node.RecordVideo) -> os.PathLike |
| `def setCompressionLevel(self, compressionLevel) -> RecordVideo` | `(self, compressionLevel)` | L23398 | setCompressionLevel(self: depthai.node.RecordVideo, compressionLevel: dai::RecordConfig::CompressionLevel) -> depthai.node.RecordVideo |
| `def setRecordMetadataFile(self, recordFile: os.PathLike) -> RecordVideo` | `(self, recordFile: os.PathLike)` | L23400 | setRecordMetadataFile(self: depthai.node.RecordVideo, recordFile: os.PathLike) -> depthai.node.RecordVideo |
| `def setRecordVideoFile(self, recordFile: os.PathLike) -> RecordVideo` | `(self, recordFile: os.PathLike)` | L23402 | setRecordVideoFile(self: depthai.node.RecordVideo, recordFile: os.PathLike) -> depthai.node.RecordVideo |

<a id="class-rectification"></a>
### class `Rectification(depthai.DeviceNode)`  — L23412

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.RectificationProperties]]` | `...` | L23413 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L23414 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def input1(self) -> depthai.Node.Input` | `(self)` | L23454 | Input images to be rectified |
| `@property` `def input2(self) -> depthai.Node.Input` | `(self)` | L23459 | (self: depthai.node.Rectification) -> depthai.Node.Input |
| `@property` `def output1(self) -> depthai.Node.Output` | `(self)` | L23462 | Send outputs |
| `@property` `def output2(self) -> depthai.Node.Output` | `(self)` | L23467 | (self: depthai.node.Rectification) -> depthai.Node.Output |
| `@property` `def passthrough1(self) -> depthai.Node.Output` | `(self)` | L23470 | Passthrough for input messages (so the node can be placed between other nodes) |
| `@property` `def passthrough2(self) -> depthai.Node.Output` | `(self)` | L23475 | (self: depthai.node.Rectification) -> depthai.Node.Output |

**🔹 Public Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def enableRectification(self, enable: bool) -> Rectification` | `(self, enable: bool)` | L23416 | enableRectification(self: depthai.node.Rectification, enable: bool) -> depthai.node.Rectification |
| `@overload` `def setOutputSize(self, width: int, height: int) -> Rectification` | `(self, width: int, height: int)` | L23422 | setOutputSize(*args, **kwargs) |
| `@overload` `def setOutputSize(self, size: tuple[int, int]) -> Rectification` | `(self, size: tuple[int, int])` | L23435 | setOutputSize(*args, **kwargs) |
| `def setRunOnHost(self, runOnHost: bool) -> None` | `(self, runOnHost: bool)` | L23447 | setRunOnHost(self: depthai.node.Rectification, runOnHost: bool) -> None |

<a id="class-replaymetadataonly"></a>
### class `ReplayMetadataOnly(ThreadedHostNode)`  — L23478

> Replay node, used to replay a file to a source node

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L23480 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L23495 | Output for any type of messages to be transferred over XLink stream |

**🔹 Public Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getFps(self) -> float` | `(self)` | L23482 | getFps(self: depthai.node.ReplayMetadataOnly) -> float |
| `def getLoop(self) -> bool` | `(self)` | L23484 | getLoop(self: depthai.node.ReplayMetadataOnly) -> bool |
| `def getReplayFile(self) -> os.PathLike` | `(self)` | L23486 | getReplayFile(self: depthai.node.ReplayMetadataOnly) -> os.PathLike |
| `def setFps(self, fps: float) -> ReplayMetadataOnly` | `(self, fps: float)` | L23488 | setFps(self: depthai.node.ReplayMetadataOnly, fps: float) -> depthai.node.ReplayMetadataOnly |
| `def setLoop(self, loop: bool) -> ReplayMetadataOnly` | `(self, loop: bool)` | L23490 | setLoop(self: depthai.node.ReplayMetadataOnly, loop: bool) -> depthai.node.ReplayMetadataOnly |
| `def setReplayFile(self, replayFile: os.PathLike) -> ReplayMetadataOnly` | `(self, replayFile: os.PathLike)` | L23492 | setReplayFile(self: depthai.node.ReplayMetadataOnly, replayFile: os.PathLike) -> depthai.node.ReplayMetadataOnly |

<a id="class-replayvideo"></a>
### class `ReplayVideo(ThreadedHostNode)`  — L23502

> Replay node, used to replay a file to a source node

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L23504 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L23547 | Output for any type of messages to be transferred over XLink stream |

**🔹 Public Methods (13):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getFps(self) -> float` | `(self)` | L23506 | getFps(self: depthai.node.ReplayVideo) -> float |
| `def getLoop(self) -> bool` | `(self)` | L23508 | getLoop(self: depthai.node.ReplayVideo) -> bool |
| `def getOutFrameType(self) -> depthai.ImgFrame.Type` | `(self)` | L23510 | getOutFrameType(self: depthai.node.ReplayVideo) -> depthai.ImgFrame.Type |
| `def getReplayMetadataFile(self) -> os.PathLike` | `(self)` | L23512 | getReplayMetadataFile(self: depthai.node.ReplayVideo) -> os.PathLike |
| `def getReplayVideoFile(self) -> os.PathLike` | `(self)` | L23514 | getReplayVideoFile(self: depthai.node.ReplayVideo) -> os.PathLike |
| `def getSize(self) -> tuple[int, int]` | `(self)` | L23516 | getSize(self: depthai.node.ReplayVideo) -> tuple[int, int] |
| `def setFps(self, fps: float) -> ReplayVideo` | `(self, fps: float)` | L23518 | setFps(self: depthai.node.ReplayVideo, fps: float) -> depthai.node.ReplayVideo |
| `def setLoop(self, loop: bool) -> ReplayVideo` | `(self, loop: bool)` | L23520 | setLoop(self: depthai.node.ReplayVideo, loop: bool) -> depthai.node.ReplayVideo |
| `def setOutFrameType(self, frameType: depthai.ImgFrame.Type) -> ReplayVideo` | `(self, frameType: depthai.ImgFrame.Type)` | L23522 | setOutFrameType(self: depthai.node.ReplayVideo, frameType: depthai.ImgFrame.Type) -> depthai.node.ReplayVideo |
| `def setReplayMetadataFile(self, replayFile: os.PathLike) -> ReplayVideo` | `(self, replayFile: os.PathLike)` | L23524 | setReplayMetadataFile(self: depthai.node.ReplayVideo, replayFile: os.PathLike) -> depthai.node.ReplayVideo |
| `def setReplayVideoFile(self, replayVideoFile: os.PathLike) -> ReplayVideo` | `(self, replayVideoFile: os.PathLike)` | L23526 | setReplayVideoFile(self: depthai.node.ReplayVideo, replayVideoFile: os.PathLike) -> depthai.node.ReplayVideo |
| `@overload` `def setSize(self, width: int, height: int) -> ReplayVideo` | `(self, width: int, height: int)` | L23529 | setSize(*args, **kwargs) |
| `@overload` `def setSize(self, size: tuple[int, int]) -> ReplayVideo` | `(self, size: tuple[int, int])` | L23538 | setSize(*args, **kwargs) |

<a id="class-spiin"></a>
### class `SPIIn(depthai.DeviceNode)`  — L23554

> SPIIn node. Receives messages over SPI.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.SPIInProperties]]` | `...` | L23556 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L23557 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L23612 | Outputs message of same type as send from host. |

**🔹 Public Methods (8):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getBusId(self) -> int` | `(self)` | L23559 | getBusId(self: depthai.node.SPIIn) -> int |
| `def getMaxDataSize(self) -> int` | `(self)` | L23564 | getMaxDataSize(self: depthai.node.SPIIn) -> int |
| `def getNumFrames(self) -> int` | `(self)` | L23569 | getNumFrames(self: depthai.node.SPIIn) -> int |
| `def getStreamName(self) -> str` | `(self)` | L23574 | getStreamName(self: depthai.node.SPIIn) -> str |
| `def setBusId(self, id: int) -> None` | `(self, id: int)` | L23579 | setBusId(self: depthai.node.SPIIn, id: int) -> None |
| `def setMaxDataSize(self, maxDataSize: int) -> None` | `(self, maxDataSize: int)` | L23587 | setMaxDataSize(self: depthai.node.SPIIn, maxDataSize: int) -> None |
| `def setNumFrames(self, numFrames: int) -> None` | `(self, numFrames: int)` | L23595 | setNumFrames(self: depthai.node.SPIIn, numFrames: int) -> None |
| `def setStreamName(self, name: str) -> None` | `(self, name: str)` | L23603 | setStreamName(self: depthai.node.SPIIn, name: str) -> None |

<a id="class-spiout"></a>
### class `SPIOut(depthai.DeviceNode)`  — L23617

> SPIOut node. Sends messages over SPI.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.SPIOutProperties]]` | `...` | L23619 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L23620 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L23639 | Input for any type of messages to be transferred over SPI stream Default queue |

**🔹 Public Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def setBusId(self, id: int) -> None` | `(self, id: int)` | L23622 | setBusId(self: depthai.node.SPIOut, id: int) -> None |
| `def setStreamName(self, name: str) -> None` | `(self, name: str)` | L23630 | setStreamName(self: depthai.node.SPIOut, name: str) -> None |

<a id="class-script"></a>
### class `Script(depthai.DeviceNode)`  — L23645

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.ScriptProperties]]` | `...` | L23646 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L23647 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def inputs(self) -> depthai.Node.InputMap` | `(self)` | L23782 | (self: depthai.node.Script) -> depthai.Node.InputMap |
| `@property` `def outputs(self) -> depthai.Node.OutputMap` | `(self)` | L23785 | (self: depthai.node.Script) -> depthai.Node.OutputMap |

**🔹 Public Methods (7):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getProcessor(self) -> depthai.ProcessorType` | `(self)` | L23649 | getProcessor(self: depthai.node.Script) -> depthai.ProcessorType |
| `def getScriptName(self) -> str` | `(self)` | L23657 | getScriptName(self: depthai.node.Script) -> str |
| `def setProcessor(self, arg0: depthai.ProcessorType) -> None` | `(self, arg0: depthai.ProcessorType)` | L23669 | setProcessor(self: depthai.node.Script, arg0: depthai.ProcessorType) -> None |
| `@overload` `def setScript(self, script: str, name: str = ...) -> None` | `(self, script: str, name: str = ...)` | L23678 | setScript(*args, **kwargs) |
| `@overload` `def setScript(self, data, std, name: str = ...) -> None` | `(self, data, std, name: str = ...)` | L23703 | setScript(*args, **kwargs) |
| `@overload` `def setScriptPath(self, arg0: os.PathLike, arg1: str) -> None` | `(self, arg0: os.PathLike, arg1: str)` | L23728 | setScriptPath(*args, **kwargs) |
| `@overload` `def setScriptPath(self, path: os.PathLike, name: str = ...) -> None` | `(self, path: os.PathLike, name: str = ...)` | L23755 | setScriptPath(*args, **kwargs) |

<a id="class-spatialdetectionnetwork"></a>
### class `SpatialDetectionNetwork(depthai.DeviceNode)`  — L23788

> SpatialDetectionNetwork node. Runs a neural inference on input image and
calculates spatial location data.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.SpatialDetectionNetworkProperties]]` | `...` | L23791 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L23792 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (10):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def boundingBoxMapping(self) -> depthai.Node.Output` | `(self)` | L24082 | Outputs mapping of detected bounding boxes relative to depth map Suitable for |
| `@property` `def detectionParser(self) -> DetectionParser` | `(self)` | L24088 | (arg0: depthai.node.SpatialDetectionNetwork) -> depthai.node.DetectionParser |
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L24091 | Input message with data to be inferred upon |
| `@property` `def inputDepth(self) -> depthai.Node.Input` | `(self)` | L24096 | Input message with depth data used to retrieve spatial information about |
| `@property` `def neuralNetwork(self) -> NeuralNetwork` | `(self)` | L24102 | (arg0: depthai.node.SpatialDetectionNetwork) -> depthai.node.NeuralNetwork |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L24105 | Outputs ImgDetections message that carries parsed detection results. |
| `@property` `def outNetwork(self) -> depthai.Node.Output` | `(self)` | L24110 | Outputs unparsed inference results. |
| `@property` `def passthrough(self) -> depthai.Node.Output` | `(self)` | L24115 | Passthrough message on which the inference was performed. |
| `@property` `def passthroughDepth(self) -> depthai.Node.Output` | `(self)` | L24122 | Passthrough message for depth frame on which the spatial location calculation |
| `@property` `def spatialLocationCalculatorOutput(self) -> depthai.Node.Output` | `(self)` | L24128 | Output of SpatialLocationCalculator node, which is used internally by |

**🔹 Public Methods (21):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def build(self, input: Camera, stereo: StereoDepth | NeuralDepth | ToF, model: depthai.NNModelDescription, fps: float | None = ..., resizeMode: depthai.ImgResizeMode | None = ...) -> SpatialDetectionNetwork` | `(self, input: Camera, stereo: StereoDepth | NeuralDepth | ToF, model: depthai.NNModelDescription, fps: float | None = ..., resizeMode: depthai.ImgResizeMode | None = ...)` | L23794 | build(*args, **kwargs) |
| `def getClasses(self) -> list[str] | None` | `(self)` | L23870 | getClasses(self: depthai.node.SpatialDetectionNetwork) -> Optional[list[str]] |
| `def getConfidenceThreshold(self) -> float` | `(self)` | L23875 | getConfidenceThreshold(self: depthai.node.SpatialDetectionNetwork) -> float |
| `def getNumInferenceThreads(self) -> int` | `(self)` | L23883 | getNumInferenceThreads(self: depthai.node.SpatialDetectionNetwork) -> int |
| `def setBackend(self, setBackend: str) -> None` | `(self, setBackend: str)` | L23891 | setBackend(self: depthai.node.SpatialDetectionNetwork, setBackend: str) -> None |
| `def setBackendProperties(self, setBackendProperties: dict[str, str]) -> None` | `(self, setBackendProperties: dict[str, str])` | L23899 | setBackendProperties(self: depthai.node.SpatialDetectionNetwork, setBackendProperties: dict[str, str]) -> None |
| `@overload` `def setBlob(self, blob: depthai.OpenVINO.Blob) -> None` | `(self, blob: depthai.OpenVINO.Blob)` | L23908 | setBlob(*args, **kwargs) |
| `@overload` `def setBlob(self, path: os.PathLike) -> None` | `(self, path: os.PathLike)` | L23931 | setBlob(*args, **kwargs) |
| `def setBlobPath(self, path: os.PathLike) -> None` | `(self, path: os.PathLike)` | L23953 | setBlobPath(self: depthai.node.SpatialDetectionNetwork, path: os.PathLike) -> None |
| `def setBoundingBoxScaleFactor(self, scaleFactor: float) -> None` | `(self, scaleFactor: float)` | L23964 | setBoundingBoxScaleFactor(self: depthai.node.SpatialDetectionNetwork, scaleFactor: float) -> None |
| `def setConfidenceThreshold(self, thresh: float) -> None` | `(self, thresh: float)` | L23974 | setConfidenceThreshold(self: depthai.node.SpatialDetectionNetwork, thresh: float) -> None |
| `def setDepthLowerThreshold(self, lowerThreshold: int) -> None` | `(self, lowerThreshold: int)` | L23983 | setDepthLowerThreshold(self: depthai.node.SpatialDetectionNetwork, lowerThreshold: int) -> None |
| `def setDepthUpperThreshold(self, upperThreshold: int) -> None` | `(self, upperThreshold: int)` | L23993 | setDepthUpperThreshold(self: depthai.node.SpatialDetectionNetwork, upperThreshold: int) -> None |
| `def setFromModelZoo(self, description: depthai.NNModelDescription, useCached: bool) -> None` | `(self, description: depthai.NNModelDescription, useCached: bool)` | L24002 | setFromModelZoo(self: depthai.node.SpatialDetectionNetwork, description: depthai.NNModelDescription, useCached: bool) -> None |
| `def setModelPath(self, modelPath: os.PathLike) -> None` | `(self, modelPath: os.PathLike)` | L24013 | setModelPath(self: depthai.node.SpatialDetectionNetwork, modelPath: os.PathLike) -> None |
| `def setNNArchive(self, archive: depthai.NNArchive) -> None` | `(self, archive: depthai.NNArchive)` | L24021 | setNNArchive(*args, **kwargs) |
| `def setNumInferenceThreads(self, numThreads: int) -> None` | `(self, numThreads: int)` | L24041 | setNumInferenceThreads(self: depthai.node.SpatialDetectionNetwork, numThreads: int) -> None |
| `def setNumNCEPerInferenceThread(self, numNCEPerThread: int) -> None` | `(self, numNCEPerThread: int)` | L24049 | setNumNCEPerInferenceThread(self: depthai.node.SpatialDetectionNetwork, numNCEPerThread: int) -> None |
| `def setNumPoolFrames(self, numFrames: int) -> None` | `(self, numFrames: int)` | L24057 | setNumPoolFrames(self: depthai.node.SpatialDetectionNetwork, numFrames: int) -> None |
| `def setNumShavesPerInferenceThread(self, numShavesPerInferenceThread: int) -> None` | `(self, numShavesPerInferenceThread: int)` | L24065 | setNumShavesPerInferenceThread(self: depthai.node.SpatialDetectionNetwork, numShavesPerInferenceThread: int) -> None |
| `def setSpatialCalculationAlgorithm(self, calculationAlgorithm: depthai.SpatialLocationCalculatorAlgorithm) -> None` | `(self, calculationAlgorithm: depthai.SpatialLocationCalculatorAlgorithm)` | L24073 | setSpatialCalculationAlgorithm(self: depthai.node.SpatialDetectionNetwork, calculationAlgorithm: depthai.SpatialLocationCalculatorAlgorithm) -> None |

<a id="class-spatiallocationcalculator"></a>
### class `SpatialLocationCalculator(depthai.DeviceNode)`  — L24135

> SpatialLocationCalculator node. Calculates spatial location data on a set of
ROIs on depth map.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.SpatialLocationCalculatorProperties]]` | `...` | L24138 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L24139 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def initialConfig(self) -> depthai.SpatialLocationCalculatorConfig` | `(self)` | L24142 | Initial config to use when calculating spatial location data. |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L24147 | Input SpatialLocationCalculatorConfig message with ability to modify parameters |
| `@property` `def inputDepth(self) -> depthai.Node.Input` | `(self)` | L24153 | Input message with depth data used to retrieve spatial information about |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L24159 | Outputs SpatialLocationCalculatorData message that carries spatial location |
| `@property` `def passthroughDepth(self) -> depthai.Node.Output` | `(self)` | L24165 | Passthrough message on which the calculation was performed. Suitable for when |

<a id="class-stereodepth"></a>
### class `StereoDepth(depthai.DeviceNode)`  — L24171

> StereoDepth node. Compute stereo disparity and depth from left-right image pair.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.StereoDepthProperties]]` | `...` | L24225 |

**🔧 Dunder Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def __init__(self, left: depthai.Node.Output, right: depthai.Node.Output, presetMode: StereoDepth.PresetMode = ...) -> None` | `(self, left: depthai.Node.Output, right: depthai.Node.Output, presetMode: StereoDepth.PresetMode = ...)` | L24227 | __init__(*args, **kwargs) |
| `@overload` `def __init__(self, autoCreateCameras: bool, presetMode: StereoDepth.PresetMode = ...) -> None` | `(self, autoCreateCameras: bool, presetMode: StereoDepth.PresetMode = ...)` | L24236 | __init__(*args, **kwargs) |

**📌 Properties (18):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def confidenceMap(self) -> depthai.Node.Output` | `(self)` | L24512 | Outputs ImgFrame message that carries RAW8 confidence map. Lower values mean |
| `@property` `def debugDispCostDump(self) -> depthai.Node.Output` | `(self)` | L24520 | Outputs ImgFrame message that carries cost dump of disparity map. Useful for |
| `@property` `def debugDispLrCheckIt1(self) -> depthai.Node.Output` | `(self)` | L24526 | Outputs ImgFrame message that carries left-right check first iteration (before |
| `@property` `def debugDispLrCheckIt2(self) -> depthai.Node.Output` | `(self)` | L24533 | Outputs ImgFrame message that carries left-right check second iteration (before |
| `@property` `def debugExtDispLrCheckIt1(self) -> depthai.Node.Output` | `(self)` | L24539 | Outputs ImgFrame message that carries extended left-right check first iteration |
| `@property` `def debugExtDispLrCheckIt2(self) -> depthai.Node.Output` | `(self)` | L24546 | Outputs ImgFrame message that carries extended left-right check second iteration |
| `@property` `def depth(self) -> depthai.Node.Output` | `(self)` | L24553 | Outputs ImgFrame message that carries RAW16 encoded (0..65535) depth data in |
| `@property` `def disparity(self) -> depthai.Node.Output` | `(self)` | L24561 | Outputs ImgFrame message that carries RAW8 / RAW16 encoded disparity data: RAW8 |
| `@property` `def initialConfig(self) -> depthai.StereoDepthConfig` | `(self)` | L24569 | Initial config to use for StereoDepth. |
| `@property` `def inputAlignTo(self) -> depthai.Node.Input` | `(self)` | L24574 | Input align to message. Default queue is non-blocking with size 1. |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L24579 | Input StereoDepthConfig message with ability to modify parameters in runtime. |
| `@property` `def left(self) -> depthai.Node.Input` | `(self)` | L24584 | Input for left ImgFrame of left-right pair |
| `@property` `def outConfig(self) -> depthai.Node.Output` | `(self)` | L24589 | Outputs StereoDepthConfig message that contains current stereo configuration. |
| `@property` `def rectifiedLeft(self) -> depthai.Node.Output` | `(self)` | L24594 | Outputs ImgFrame message that carries RAW8 encoded (grayscale) rectified frame |
| `@property` `def rectifiedRight(self) -> depthai.Node.Output` | `(self)` | L24600 | Outputs ImgFrame message that carries RAW8 encoded (grayscale) rectified frame |
| `@property` `def right(self) -> depthai.Node.Input` | `(self)` | L24606 | Input for right ImgFrame of left-right pair |
| `@property` `def syncedLeft(self) -> depthai.Node.Output` | `(self)` | L24611 | Passthrough ImgFrame message from 'left' Input. |
| `@property` `def syncedRight(self) -> depthai.Node.Output` | `(self)` | L24616 | Passthrough ImgFrame message from 'right' Input. |

**🔹 Public Methods (29):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def build(self, left: depthai.Node.Output, right: depthai.Node.Output, presetMode: StereoDepth.PresetMode = ...) -> StereoDepth` | `(self, left: depthai.Node.Output, right: depthai.Node.Output, presetMode: StereoDepth.PresetMode = ...)` | L24245 | build(*args, **kwargs) |
| `@overload` `def build(self, autoCreateCameras: bool, presetMode: StereoDepth.PresetMode = ..., size: tuple[int, int] = ..., fps: float | None = ...) -> StereoDepth` | `(self, autoCreateCameras: bool, presetMode: StereoDepth.PresetMode = ..., size: tuple[int, int] = ..., fps: float | None = ...)` | L24254 | build(*args, **kwargs) |
| `def enableDistortionCorrection(self, arg0: bool) -> None` | `(self, arg0: bool)` | L24262 | enableDistortionCorrection(self: depthai.node.StereoDepth, arg0: bool) -> None |
| `def loadMeshData(self, *args, **kwargs)` | `(self, *args, **kwargs)` | L24267 | loadMeshData(self: depthai.node.StereoDepth, dataLeft: std::vector<unsigned char,std::allocator<unsigned char> >, dataRight: std::vector<unsigned char,std::allocator<unsigned char> >) -> None |
| `def loadMeshFiles(self, pathLeft: os.PathLike, pathRight: os.PathLike) -> None` | `(self, pathLeft: os.PathLike, pathRight: os.PathLike)` | L24274 | loadMeshFiles(self: depthai.node.StereoDepth, pathLeft: os.PathLike, pathRight: os.PathLike) -> None |
| `def setAlphaScaling(self, arg0: float) -> None` | `(self, arg0: float)` | L24292 | setAlphaScaling(self: depthai.node.StereoDepth, arg0: float) -> None |
| `def setBaseline(self, arg0: float) -> None` | `(self, arg0: float)` | L24302 | setBaseline(self: depthai.node.StereoDepth, arg0: float) -> None |
| `def setDefaultProfilePreset(self, arg0: StereoDepth.PresetMode) -> None` | `(self, arg0: StereoDepth.PresetMode)` | L24308 | setDefaultProfilePreset(self: depthai.node.StereoDepth, arg0: depthai.node.StereoDepth.PresetMode) -> None |
| `@overload` `def setDepthAlign(self, align: depthai.StereoDepthConfig.AlgorithmControl.DepthAlign) -> None` | `(self, align: depthai.StereoDepthConfig.AlgorithmControl.DepthAlign)` | L24317 | setDepthAlign(*args, **kwargs) |
| `@overload` `def setDepthAlign(self, camera: depthai.CameraBoardSocket) -> None` | `(self, camera: depthai.CameraBoardSocket)` | L24333 | setDepthAlign(*args, **kwargs) |
| `def setDepthAlignmentUseSpecTranslation(self, arg0: bool) -> None` | `(self, arg0: bool)` | L24348 | setDepthAlignmentUseSpecTranslation(self: depthai.node.StereoDepth, arg0: bool) -> None |
| `def setDisparityToDepthUseSpecTranslation(self, arg0: bool) -> None` | `(self, arg0: bool)` | L24354 | setDisparityToDepthUseSpecTranslation(self: depthai.node.StereoDepth, arg0: bool) -> None |
| `def setExtendedDisparity(self, enable: bool) -> None` | `(self, enable: bool)` | L24360 | setExtendedDisparity(self: depthai.node.StereoDepth, enable: bool) -> None |
| `def setFocalLength(self, arg0: float) -> None` | `(self, arg0: float)` | L24369 | setFocalLength(self: depthai.node.StereoDepth, arg0: float) -> None |
| `@overload` `def setInputResolution(self, width: int, height: int) -> None` | `(self, width: int, height: int)` | L24376 | setInputResolution(*args, **kwargs) |
| `@overload` `def setInputResolution(self, resolution: tuple[int, int]) -> None` | `(self, resolution: tuple[int, int])` | L24393 | setInputResolution(*args, **kwargs) |
| `def setLeftRightCheck(self, enable: bool) -> None` | `(self, enable: bool)` | L24409 | setLeftRightCheck(self: depthai.node.StereoDepth, enable: bool) -> None |
| `def setMeshStep(self, width: int, height: int) -> None` | `(self, width: int, height: int)` | L24417 | setMeshStep(self: depthai.node.StereoDepth, width: int, height: int) -> None |
| `def setNumFramesPool(self, arg0: int) -> None` | `(self, arg0: int)` | L24422 | setNumFramesPool(self: depthai.node.StereoDepth, arg0: int) -> None |
| `def setOutputKeepAspectRatio(self, keep: bool) -> None` | `(self, keep: bool)` | L24430 | setOutputKeepAspectRatio(self: depthai.node.StereoDepth, keep: bool) -> None |
| `def setOutputSize(self, width: int, height: int) -> None` | `(self, width: int, height: int)` | L24436 | setOutputSize(self: depthai.node.StereoDepth, width: int, height: int) -> None |
| `def setPostProcessingHardwareResources(self, arg0: int, arg1: int) -> None` | `(self, arg0: int, arg1: int)` | L24443 | setPostProcessingHardwareResources(self: depthai.node.StereoDepth, arg0: int, arg1: int) -> None |
| `def setRectification(self, enable: bool) -> None` | `(self, enable: bool)` | L24455 | setRectification(self: depthai.node.StereoDepth, enable: bool) -> None |
| `def setRectificationUseSpecTranslation(self, arg0: bool) -> None` | `(self, arg0: bool)` | L24460 | setRectificationUseSpecTranslation(self: depthai.node.StereoDepth, arg0: bool) -> None |
| `def setRectifyEdgeFillColor(self, color: int) -> None` | `(self, color: int)` | L24466 | setRectifyEdgeFillColor(self: depthai.node.StereoDepth, color: int) -> None |
| `def setRuntimeModeSwitch(self, arg0: bool) -> None` | `(self, arg0: bool)` | L24474 | setRuntimeModeSwitch(self: depthai.node.StereoDepth, arg0: bool) -> None |
| `def setSubpixel(self, enable: bool) -> None` | `(self, enable: bool)` | L24480 | setSubpixel(self: depthai.node.StereoDepth, enable: bool) -> None |
| `def setSubpixelFractionalBits(self, subpixelFractionalBits: int) -> None` | `(self, subpixelFractionalBits: int)` | L24487 | setSubpixelFractionalBits(self: depthai.node.StereoDepth, subpixelFractionalBits: int) -> None |
| `def useHomographyRectification(self, arg0: bool) -> None` | `(self, arg0: bool)` | L24494 | useHomographyRectification(self: depthai.node.StereoDepth, arg0: bool) -> None |

**Nested Class:**

<a id="class-presetmode"></a>
#### class `PresetMode`  — L24174

> Preset modes for stereo depth.

Members:

  FAST_ACCURACY

  FAST_DENSITY

  DEFAULT

  FACE

  HIGH_DETAIL

  ROBOTICS

  DENSITY

  ACCURACY

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `__members__` | `ClassVar[dict]` | `...` | L24194 |
| `ACCURACY` | `ClassVar[StereoDepth.PresetMode]` | `...` | L24195 |
| `DEFAULT` | `ClassVar[StereoDepth.PresetMode]` | `...` | L24196 |
| `DENSITY` | `ClassVar[StereoDepth.PresetMode]` | `...` | L24197 |
| `FACE` | `ClassVar[StereoDepth.PresetMode]` | `...` | L24198 |
| `FAST_ACCURACY` | `ClassVar[StereoDepth.PresetMode]` | `...` | L24199 |
| `FAST_DENSITY` | `ClassVar[StereoDepth.PresetMode]` | `...` | L24200 |
| `HIGH_DETAIL` | `ClassVar[StereoDepth.PresetMode]` | `...` | L24201 |
| `ROBOTICS` | `ClassVar[StereoDepth.PresetMode]` | `...` | L24202 |
| `__entries` | `ClassVar[dict]` | `...` | L24203 |

**🔧 Dunder Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, value: int) -> None` | `(self, value: int)` | L24204 | __init__(self: depthai.node.StereoDepth.PresetMode, value: int) -> None |
| `def __eq__(self, other: object) -> bool` | `(self, other: object)` | L24206 | __eq__(self: object, other: object) -> bool |
| `def __hash__(self) -> int` | `(self)` | L24208 | __hash__(self: object) -> int |
| `def __index__(self) -> int` | `(self)` | L24210 | __index__(self: depthai.node.StereoDepth.PresetMode) -> int |
| `def __int__(self) -> int` | `(self)` | L24212 | __int__(self: depthai.node.StereoDepth.PresetMode) -> int |
| `def __ne__(self, other: object) -> bool` | `(self, other: object)` | L24214 | __ne__(self: object, other: object) -> bool |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def name(self) -> str` | `(self)` | L24217 | name(self: object) -> str |
| `@property` `def value(self) -> int` | `(self)` | L24223 | (arg0: depthai.node.StereoDepth.PresetMode) -> int |

<a id="class-sync"></a>
### class `Sync(depthai.DeviceNode)`  — L24621

> Sync node. Performs syncing between image frames

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.SyncProperties]]` | `...` | L24623 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L24624 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def inputs(self) -> depthai.Node.InputMap` | `(self)` | L24670 | A map of inputs |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L24675 | (self: depthai.node.Sync) -> depthai.Node.Output |

**🔹 Public Methods (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getSyncAttempts(self) -> int` | `(self)` | L24626 | getSyncAttempts(self: depthai.node.Sync) -> int |
| `def getSyncThreshold(self) -> datetime.timedelta` | `(self)` | L24631 | getSyncThreshold(self: depthai.node.Sync) -> datetime.timedelta |
| `def runOnHost(self) -> bool` | `(self)` | L24636 | runOnHost(self: depthai.node.Sync) -> bool |
| `def setRunOnHost(self, runOnHost: bool) -> None` | `(self, runOnHost: bool)` | L24641 | setRunOnHost(self: depthai.node.Sync, runOnHost: bool) -> None |
| `def setSyncAttempts(self, maxDataSize: int) -> None` | `(self, maxDataSize: int)` | L24647 | setSyncAttempts(self: depthai.node.Sync, maxDataSize: int) -> None |
| `def setSyncThreshold(self, syncThreshold: datetime.timedelta) -> None` | `(self, syncThreshold: datetime.timedelta)` | L24661 | setSyncThreshold(self: depthai.node.Sync, syncThreshold: datetime.timedelta) -> None |

<a id="class-systemlogger"></a>
### class `SystemLogger(depthai.DeviceNode)`  — L24678

> SystemLogger node. Send system information periodically.

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L24680 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L24696 | Outputs SystemInformation[RVC4] message that carries various system information |

**🔹 Public Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getRate(self) -> float` | `(self)` | L24682 | getRate(self: depthai.node.SystemLogger) -> float |
| `def setRate(self, hz: float) -> None` | `(self, hz: float)` | L24687 | setRate(self: depthai.node.SystemLogger, hz: float) -> None |

<a id="class-thermal"></a>
### class `Thermal(depthai.DeviceNode)`  — L24704

> Thermal node.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.ThermalProperties]]` | `...` | L24706 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L24707 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def color(self) -> depthai.Node.Output` | `(self)` | L24723 | Outputs YUV422i grayscale thermal image. |
| `@property` `def initialConfig(self) -> depthai.ThermalConfig` | `(self)` | L24728 | Initial config to use for thermal sensor. |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L24733 | Input ThermalConfig message with ability to modify parameters in runtime. |
| `@property` `def temperature(self) -> depthai.Node.Output` | `(self)` | L24739 | Outputs FP16 (degC) thermal image. |

**🔹 Public Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def build(self, boardSocket: depthai.CameraBoardSocket = ..., fps: float = ...) -> Thermal` | `(self, boardSocket: depthai.CameraBoardSocket = ..., fps: float = ...)` | L24709 | build(self: depthai.node.Thermal, boardSocket: depthai.CameraBoardSocket = <CameraBoardSocket.???: -1>, fps: float = 25.0) -> depthai.node.Thermal |
| `def getBoardSocket(self) -> depthai.CameraBoardSocket` | `(self)` | L24714 | getBoardSocket(self: depthai.node.Thermal) -> depthai.CameraBoardSocket |

<a id="class-threadedhostnode"></a>
### class `ThreadedHostNode(depthai.ThreadedNode)`  — L24744

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `createSubnode` | `ClassVar[Callable]` | `...` | L24745 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self) -> None` | `(self)` | L24746 | __init__(self: depthai.node.ThreadedHostNode) -> None |

**🔹 Public Methods (5):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def createInput(self, name: str = ..., group: str = ..., blocking: bool = ..., queueSize: int = ..., types: list[depthai.Node.DatatypeHierarchy] = ..., waitForMessage: bool = ...) -> depthai.Node.Input` | `(self, name: str = ..., group: str = ..., blocking: bool = ..., queueSize: int = ..., types: list[depthai.Node.DatatypeHierarchy] = ..., waitForMessage: bool = ...)` | L24748 | createInput(self: depthai.node.ThreadedHostNode, name: str = '', group: str = '', blocking: bool = True, queueSize: int = 3, types: list[depthai.Node.DatatypeHierarchy] = [<depthai.Node.DatatypeHierarchy object at 0x0000023408A94570>], waitForMessage: bool = False) -> depthai.Node.Input |
| `def createOutput(self, name: str = ..., group: str = ..., possibleDatatypes: list[depthai.Node.DatatypeHierarchy] = ...) -> depthai.Node.Output` | `(self, name: str = ..., group: str = ..., possibleDatatypes: list[depthai.Node.DatatypeHierarchy] = ...)` | L24750 | createOutput(self: depthai.node.ThreadedHostNode, name: str = '', group: str = '', possibleDatatypes: list[depthai.Node.DatatypeHierarchy] = [<depthai.Node.DatatypeHierarchy object at 0x000002347EF740B0>]) -> depthai.Node.Output |
| `def onStart(self) -> None` | `(self)` | L24752 | onStart(self: depthai.node.ThreadedHostNode) -> None |
| `def onStop(self) -> None` | `(self)` | L24754 | onStop(self: depthai.node.ThreadedHostNode) -> None |
| `def run(self) -> None` | `(self)` | L24756 | run(self: depthai.node.ThreadedHostNode) -> None |

<a id="class-tof"></a>
### class `ToF(depthai.DeviceNodeGroup)`  — L24759

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L24760 | Initialize self.  See help(type(self)) for accurate signature. |

**⚡ Static Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@staticmethod` `def create(device: depthai.Device) -> ToF` | `(device: depthai.Device)` | L24765 | create(device: depthai.Device) -> depthai.node.ToF |

**📌 Properties (9):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def amplitude(self) -> depthai.Node.Output` | `(self)` | L24772 | Amplitude output |
| `@property` `def depth(self) -> depthai.Node.Output` | `(self)` | L24777 | Filtered depth output |
| `@property` `def imageFiltersInputConfig(self) -> depthai.Node.Input` | `(self)` | L24782 | Input config for image filters |
| `@property` `def imageFiltersNode(self) -> ImageFilters` | `(self)` | L24787 | Image filters node |
| `@property` `def intensity(self) -> depthai.Node.Output` | `(self)` | L24792 | Intensity output |
| `@property` `def phase(self) -> depthai.Node.Output` | `(self)` | L24797 | Phase output |
| `@property` `def rawDepth(self) -> depthai.Node.Output` | `(self)` | L24802 | Raw depth output from ToF sensor |
| `@property` `def tofBaseInputConfig(self) -> depthai.Node.Input` | `(self)` | L24807 | Input config for ToF base node |
| `@property` `def tofBaseNode(self) -> ToFBase` | `(self)` | L24812 | ToF base node |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def build(self, boardSocket: depthai.CameraBoardSocket = ..., presetMode: depthai.ImageFiltersPresetMode = ..., fps: float | None = ...) -> ToF` | `(self, boardSocket: depthai.CameraBoardSocket = ..., presetMode: depthai.ImageFiltersPresetMode = ..., fps: float | None = ...)` | L24762 | build(self: depthai.node.ToF, boardSocket: depthai.CameraBoardSocket = <CameraBoardSocket.???: -1>, presetMode: depthai.ImageFiltersPresetMode = <ImageFiltersPresetMode.TOF_MID_RANGE: 1>, fps: Optional[float] = None) -> depthai.node.ToF |
| `def getInitialConfig(self) -> depthai.ToFConfig` | `(self)` | L24767 | getInitialConfig(self: depthai.node.ToF) -> depthai.ToFConfig |
| `def setInitialConfig(self, arg0: depthai.ToFConfig) -> None` | `(self, arg0: depthai.ToFConfig)` | L24769 | setInitialConfig(self: depthai.node.ToF, arg0: depthai.ToFConfig) -> None |

<a id="class-tofbase"></a>
### class `ToFBase(depthai.DeviceNode)`  — L24817

> ToFBase node. Performs feature tracking and reidentification using motion
estimation between 2 consecutive frames.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.ToFProperties]]` | `...` | L24820 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L24821 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def amplitude(self) -> depthai.Node.Output` | `(self)` | L24837 | (self: depthai.node.ToFBase) -> depthai.Node.Output |
| `@property` `def depth(self) -> depthai.Node.Output` | `(self)` | L24840 | (self: depthai.node.ToFBase) -> depthai.Node.Output |
| `@property` `def initialConfig(self) -> depthai.ToFConfig` | `(self)` | L24843 | Initial config to use for feature tracking. |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L24848 | Input ToFConfig message with ability to modify parameters in runtime. Default |
| `@property` `def intensity(self) -> depthai.Node.Output` | `(self)` | L24854 | (self: depthai.node.ToFBase) -> depthai.Node.Output |
| `@property` `def phase(self) -> depthai.Node.Output` | `(self)` | L24857 | (self: depthai.node.ToFBase) -> depthai.Node.Output |

**🔹 Public Methods (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def build(self, boardSocket: depthai.CameraBoardSocket = ..., presetMode: depthai.ImageFiltersPresetMode = ..., fps: float | None = ...) -> ToFBase` | `(self, boardSocket: depthai.CameraBoardSocket = ..., presetMode: depthai.ImageFiltersPresetMode = ..., fps: float | None = ...)` | L24823 | build(self: depthai.node.ToFBase, boardSocket: depthai.CameraBoardSocket = <CameraBoardSocket.???: -1>, presetMode: depthai.ImageFiltersPresetMode = <ImageFiltersPresetMode.TOF_MID_RANGE: 1>, fps: Optional[float] = None) -> depthai.node.ToFBase |
| `def getBoardSocket(self) -> depthai.CameraBoardSocket` | `(self)` | L24828 | getBoardSocket(self: depthai.node.ToFBase) -> depthai.CameraBoardSocket |

<a id="class-tofdepthconfidencefilter"></a>
### class `ToFDepthConfidenceFilter(depthai.DeviceNode)`  — L24860

> Node for depth confidence filter, designed to be used with the `ToF` node.

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L24862 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (6):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def amplitude(self) -> depthai.Node.Input` | `(self)` | L24950 | Amplitude frame image, expected ImgFrame type is RAW8 or RAW16. |
| `@property` `def confidence(self) -> depthai.Node.Output` | `(self)` | L24955 | RAW16 encoded confidence frame |
| `@property` `def depth(self) -> depthai.Node.Input` | `(self)` | L24960 | Depth frame image, expected ImgFrame type is RAW8 or RAW16. |
| `@property` `def filteredDepth(self) -> depthai.Node.Output` | `(self)` | L24965 | RAW16 encoded filtered depth frame |
| `@property` `def initialConfig(self) -> depthai.ToFDepthConfidenceFilterConfig` | `(self)` | L24970 | Initial config for ToF depth confidence filter. |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L24975 | Config message for runtime filter configuration |

**🔹 Public Methods (4):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@overload` `def build(self, depth: depthai.Node.Output, amplitude: depthai.Node.Output, presetMode: depthai.ImageFiltersPresetMode = ...) -> ToFDepthConfidenceFilter` | `(self, depth: depthai.Node.Output, amplitude: depthai.Node.Output, presetMode: depthai.ImageFiltersPresetMode = ...)` | L24865 | build(*args, **kwargs) |
| `@overload` `def build(self, presetMode: depthai.ImageFiltersPresetMode = ...) -> ToFDepthConfidenceFilter` | `(self, presetMode: depthai.ImageFiltersPresetMode = ...)` | L24902 | build(*args, **kwargs) |
| `def runOnHost(self) -> bool` | `(self)` | L24938 | runOnHost(self: depthai.node.ToFDepthConfidenceFilter) -> bool |
| `def setRunOnHost(self, runOnHost: bool) -> None` | `(self, runOnHost: bool)` | L24943 | setRunOnHost(self: depthai.node.ToFDepthConfidenceFilter, runOnHost: bool) -> None |

<a id="class-uvc"></a>
### class `UVC(depthai.DeviceNode)`  — L24980

> UVC (USB Video Class) node

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.UVCProperties]]` | `...` | L24982 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, USBVideoClass) -> Any` | `(self, USBVideoClass)` | L24983 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L25001 | Input for image frames to be streamed over UVC Default queue is blocking with |

**🔹 Public Methods (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def setGpiosOnInit(self, list: dict[int, int]) -> None` | `(self, list: dict[int, int])` | L24985 | setGpiosOnInit(self: depthai.node.UVC, list: dict[int, int]) -> None |
| `def setGpiosOnStreamOff(self, list: dict[int, int]) -> None` | `(self, list: dict[int, int])` | L24990 | setGpiosOnStreamOff(self: depthai.node.UVC, list: dict[int, int]) -> None |
| `def setGpiosOnStreamOn(self, list: dict[int, int]) -> None` | `(self, list: dict[int, int])` | L24995 | setGpiosOnStreamOn(self: depthai.node.UVC, list: dict[int, int]) -> None |

<a id="class-videoencoder"></a>
### class `VideoEncoder(depthai.DeviceNode)`  — L25007

> VideoEncoder node. Encodes frames into MJPEG, H264 or H265.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.VideoEncoderProperties]]` | `...` | L25009 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, input: depthai.Node.Output, bitrate: float = ..., frameRate: float = ..., profile: depthai.VideoEncoderProperties.Profile = ..., keyframeFrequency: int = ..., lossless: bool = ..., quality: int = ...) -> None` | `(self, input: depthai.Node.Output, bitrate: float = ..., frameRate: float = ..., profile: depthai.VideoEncoderProperties.Profile = ..., keyframeFrequency: int = ..., lossless: bool = ..., quality: int = ...)` | L25010 | __init__(self: depthai.node.VideoEncoder, input: depthai.Node.Output, bitrate: float = 0, frameRate: float = 30.0, profile: depthai.VideoEncoderProperties.Profile = <Profile.H264_BASELINE: 0>, keyframeFrequency: int = 30, lossless: bool = False, quality: int = 80) -> None |

**📌 Properties (3):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def bitstream(self) -> depthai.Node.Output` | `(self)` | L25158 | Outputs ImgFrame message that carries BITSTREAM encoded (MJPEG, H264 or H265) |
| `@property` `def input(self) -> depthai.Node.Input` | `(self)` | L25164 | Input for NV12 ImgFrame to be encoded |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L25169 | Outputs EncodedFrame message that carries encoded (MJPEG, H264 or H265) frame |

**🔹 Public Methods (24):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def build(self, input: depthai.Node.Output, bitrate: float = ..., frameRate: float = ..., profile: depthai.VideoEncoderProperties.Profile = ..., keyframeFrequency: int = ..., lossless: bool = ..., quality: int = ...) -> VideoEncoder` | `(self, input: depthai.Node.Output, bitrate: float = ..., frameRate: float = ..., profile: depthai.VideoEncoderProperties.Profile = ..., keyframeFrequency: int = ..., lossless: bool = ..., quality: int = ...)` | L25012 | build(self: depthai.node.VideoEncoder, input: depthai.Node.Output, bitrate: float = 0, frameRate: float = 30.0, profile: depthai.VideoEncoderProperties.Profile = <Profile.H264_BASELINE: 0>, keyframeFrequency: int = 30, lossless: bool = False, quality: int = 80) -> depthai.node.VideoEncoder |
| `def getBitrate(self) -> int` | `(self)` | L25014 | getBitrate(self: depthai.node.VideoEncoder) -> int |
| `def getBitrateKbps(self) -> int` | `(self)` | L25019 | getBitrateKbps(self: depthai.node.VideoEncoder) -> int |
| `def getFrameRate(self) -> float` | `(self)` | L25024 | getFrameRate(self: depthai.node.VideoEncoder) -> float |
| `def getKeyframeFrequency(self) -> int` | `(self)` | L25029 | getKeyframeFrequency(self: depthai.node.VideoEncoder) -> int |
| `def getLossless(self) -> bool` | `(self)` | L25034 | getLossless(self: depthai.node.VideoEncoder) -> bool |
| `def getMaxOutputFrameSize(self) -> int` | `(self)` | L25039 | getMaxOutputFrameSize(self: depthai.node.VideoEncoder) -> int |
| `def getNumBFrames(self) -> int` | `(self)` | L25041 | getNumBFrames(self: depthai.node.VideoEncoder) -> int |
| `def getNumFramesPool(self) -> int` | `(self)` | L25046 | getNumFramesPool(self: depthai.node.VideoEncoder) -> int |
| `def getProfile(self) -> depthai.VideoEncoderProperties.Profile` | `(self)` | L25054 | getProfile(self: depthai.node.VideoEncoder) -> depthai.VideoEncoderProperties.Profile |
| `def getQuality(self) -> int` | `(self)` | L25059 | getQuality(self: depthai.node.VideoEncoder) -> int |
| `def getRateControlMode(self) -> depthai.VideoEncoderProperties.RateControlMode` | `(self)` | L25064 | getRateControlMode(self: depthai.node.VideoEncoder) -> depthai.VideoEncoderProperties.RateControlMode |
| `def setBitrate(self, bitrate: int) -> None` | `(self, bitrate: int)` | L25069 | setBitrate(self: depthai.node.VideoEncoder, bitrate: int) -> None |
| `def setBitrateKbps(self, bitrateKbps: int) -> None` | `(self, bitrateKbps: int)` | L25075 | setBitrateKbps(self: depthai.node.VideoEncoder, bitrateKbps: int) -> None |
| `def setDefaultProfilePreset(self, fps: float, profile: depthai.VideoEncoderProperties.Profile) -> None` | `(self, fps: float, profile: depthai.VideoEncoderProperties.Profile)` | L25081 | setDefaultProfilePreset(self: depthai.node.VideoEncoder, fps: float, profile: depthai.VideoEncoderProperties.Profile) -> None |
| `def setFrameRate(self, frameRate: float) -> None` | `(self, frameRate: float)` | L25092 | setFrameRate(self: depthai.node.VideoEncoder, frameRate: float) -> None |
| `def setKeyframeFrequency(self, freq: int) -> None` | `(self, freq: int)` | L25100 | setKeyframeFrequency(self: depthai.node.VideoEncoder, freq: int) -> None |
| `def setLossless(self, arg0: bool) -> None` | `(self, arg0: bool)` | L25113 | setLossless(self: depthai.node.VideoEncoder, arg0: bool) -> None |
| `def setMaxOutputFrameSize(self, maxFrameSize: int) -> None` | `(self, maxFrameSize: int)` | L25121 | setMaxOutputFrameSize(self: depthai.node.VideoEncoder, maxFrameSize: int) -> None |
| `def setNumBFrames(self, numBFrames: int) -> None` | `(self, numBFrames: int)` | L25126 | setNumBFrames(self: depthai.node.VideoEncoder, numBFrames: int) -> None |
| `def setNumFramesPool(self, frames: int) -> None` | `(self, frames: int)` | L25131 | setNumFramesPool(self: depthai.node.VideoEncoder, frames: int) -> None |
| `def setProfile(self, profile: depthai.VideoEncoderProperties.Profile) -> None` | `(self, profile: depthai.VideoEncoderProperties.Profile)` | L25139 | setProfile(self: depthai.node.VideoEncoder, profile: depthai.VideoEncoderProperties.Profile) -> None |
| `def setQuality(self, quality: int) -> None` | `(self, quality: int)` | L25144 | setQuality(self: depthai.node.VideoEncoder, quality: int) -> None |
| `def setRateControlMode(self, mode: depthai.VideoEncoderProperties.RateControlMode) -> None` | `(self, mode: depthai.VideoEncoderProperties.RateControlMode)` | L25152 | setRateControlMode(self: depthai.node.VideoEncoder, mode: depthai.VideoEncoderProperties.RateControlMode) -> None |

<a id="class-vpp"></a>
### class `Vpp(depthai.DeviceNode)`  — L25175

> Vpp node. Apply Virtual Projection Pattern algorithm to stereo images based on
disparity.

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.VppProperties]]` | `...` | L25178 |
| `initialConfig` | `depthai.VppConfig` | — | L25179 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L25180 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (8):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def confidence(self) -> depthai.Node.Input` | `(self)` | L25185 | (arg0: depthai.node.Vpp) -> depthai.Node.Input |
| `@property` `def disparity(self) -> depthai.Node.Input` | `(self)` | L25188 | (arg0: depthai.node.Vpp) -> depthai.Node.Input |
| `@property` `def inputConfig(self) -> depthai.Node.Input` | `(self)` | L25191 | (self: depthai.node.Vpp) -> depthai.Node.Input |
| `@property` `def left(self) -> depthai.Node.Input` | `(self)` | L25194 | (arg0: depthai.node.Vpp) -> depthai.Node.Input |
| `@property` `def leftOut(self) -> depthai.Node.Output` | `(self)` | L25197 | Output ImgFrame message that carries the processed left image with virtual |
| `@property` `def right(self) -> depthai.Node.Input` | `(self)` | L25203 | (arg0: depthai.node.Vpp) -> depthai.Node.Input |
| `@property` `def rightOut(self) -> depthai.Node.Output` | `(self)` | L25206 | Output ImgFrame message that carries the processed right image with virtual |
| `@property` `def syncedInputs(self) -> depthai.Node.Input` | `(self)` | L25212 | "Synchronised Left Img, Right Img, Dispatiy and confidence input." |

**🔹 Public Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def build(self, leftInput: depthai.Node.Output, rightInput: depthai.Node.Output, disparity: depthai.Node.Output, confidence: depthai.Node.Output) -> Vpp` | `(self, leftInput: depthai.Node.Output, rightInput: depthai.Node.Output, disparity: depthai.Node.Output, confidence: depthai.Node.Output)` | L25182 | build(self: depthai.node.Vpp, leftInput: depthai.Node.Output, rightInput: depthai.Node.Output, disparity: depthai.Node.Output, confidence: depthai.Node.Output) -> depthai.node.Vpp |

<a id="class-warp"></a>
### class `Warp(depthai.DeviceNode)`  — L25217

> Warp node. Capability to crop, resize, warp, ... incoming image frames

**Class Variables:**

| Name | Type | Value | Line |
|------|------|-------|------|
| `Properties` | `ClassVar[type[depthai.WarpProperties]]` | `...` | L25219 |

**🔧 Dunder Methods (1):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def __init__(self, *args, **kwargs) -> None` | `(self, *args, **kwargs)` | L25220 | Initialize self.  See help(type(self)) for accurate signature. |

**📌 Properties (2):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `@property` `def inputImage(self) -> depthai.Node.Input` | `(self)` | L25311 | Input image to be modified Default queue is blocking with size 8 |
| `@property` `def out(self) -> depthai.Node.Output` | `(self)` | L25316 | Outputs ImgFrame message that carries warped image. |

**🔹 Public Methods (10):**

| Method | Signature | Line | Docstring |
|--------|-----------|------|-----------|
| `def getHwIds(self) -> list[int]` | `(self)` | L25222 | getHwIds(self: depthai.node.Warp) -> list[int] |
| `def getInterpolation(self) -> depthai.Interpolation` | `(self)` | L25227 | getInterpolation(self: depthai.node.Warp) -> depthai.Interpolation |
| `def setHwIds(self, arg0: list[int]) -> None` | `(self, arg0: list[int])` | L25232 | setHwIds(self: depthai.node.Warp, arg0: list[int]) -> None |
| `def setInterpolation(self, arg0: depthai.Interpolation) -> None` | `(self, arg0: depthai.Interpolation)` | L25240 | setInterpolation(self: depthai.node.Warp, arg0: depthai.Interpolation) -> None |
| `def setMaxOutputFrameSize(self, arg0: int) -> None` | `(self, arg0: int)` | L25248 | setMaxOutputFrameSize(self: depthai.node.Warp, arg0: int) -> None |
| `def setNumFramesPool(self, arg0: int) -> None` | `(self, arg0: int)` | L25256 | setNumFramesPool(self: depthai.node.Warp, arg0: int) -> None |
| `@overload` `def setOutputSize(self, arg0: int, arg1: int) -> None` | `(self, arg0: int, arg1: int)` | L25265 | setOutputSize(*args, **kwargs) |
| `@overload` `def setOutputSize(self, arg0: tuple[int, int]) -> None` | `(self, arg0: tuple[int, int])` | L25279 | setOutputSize(*args, **kwargs) |
| `@overload` `def setWarpMesh(self, arg0: depthai.VectorPoint2f, arg1: int, arg2: int) -> None` | `(self, arg0: depthai.VectorPoint2f, arg1: int, arg2: int)` | L25293 | setWarpMesh(*args, **kwargs) |
| `@overload` `def setWarpMesh(self, arg0: list[tuple[float, float]], arg1: int, arg2: int) -> None` | `(self, arg0: list[tuple[float, float]], arg1: int, arg2: int)` | L25302 | setWarpMesh(*args, **kwargs) |

---
## Summary

| Metric | Count |
|--------|-------|
| Imports | 18 |
| Global Variables | 53 |
| Functions | 6 |
| Classes | 261 |
| Total Methods | 2152 |
| Total Lines | 25319 |
