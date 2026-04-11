"""
Model export utilities: PyTorch → ONNX → MyriadX blob.

Encoder pipeline:
    DepthEncoder (PyTorch) → encoder.onnx → encoder.blob (MyriadX, FP16)

GRU pipeline:
    ObstacleAvoidanceGRU (PyTorch) → gru_avoidance.onnx (ONNX Runtime on RPi5)
    Note: GRU is NOT compiled to a blob — MyriadX does not support GRU/LayerNorm.

OpenVINO version constraint:
    blobconverter MUST use version="2022.1" or "2022.3".
    OpenVINO 2023+ removed the MYRIAD plugin entirely.

Usage:
    from avoidance.depth_encoder import DepthEncoder
    from avoidance.gru_model import ObstacleAvoidanceGRU
    from avoidance.export import export_encoder_onnx, export_gru_onnx, compile_encoder_blob

    enc = DepthEncoder()
    export_encoder_onnx(enc, "models/encoder.onnx")
    compile_encoder_blob("models/encoder.onnx", "models/encoder.blob", shaves=6)

    gru = ObstacleAvoidanceGRU()
    export_gru_onnx(gru, "models/gru_avoidance.onnx")
"""

import torch

from avoidance.depth_encoder import DepthEncoder
from avoidance.gru_model import ObstacleAvoidanceGRU


def export_encoder_onnx(model: DepthEncoder, path: str) -> None:
    """
    Export DepthEncoder to ONNX for MyriadX compilation.

    Args:
        model: trained DepthEncoder instance
        path:  output path for .onnx file
    """
    model.eval()
    dummy = torch.zeros(1, 1, 128, 128, dtype=torch.float32)

    torch.onnx.export(
        model,
        dummy,
        path,
        export_params=True,
        opset_version=12,
        do_constant_folding=True,
        input_names=["depth_image"],
        output_names=["depth_feat"],
        dynamic_axes={
            "depth_image": {0: "batch"},
            "depth_feat":  {0: "batch"},
        },
    )
    print(f"[EXPORT] Encoder ONNX: {path}")


def export_gru_onnx(model: ObstacleAvoidanceGRU, path: str) -> None:
    """
    Export ObstacleAvoidanceGRU to ONNX for ONNX Runtime on RPi5.

    Static shapes (no dynamic axes) for deterministic inference latency.

    Input names:  x [1, 1, 80], h_in [1, 1, 128]
    Output names: correction [1, 3], h_out [1, 1, 128]

    Args:
        model: trained ObstacleAvoidanceGRU instance
        path:  output path for .onnx file
    """
    model.eval()
    dummy_x = torch.zeros(1, 1, 80,  dtype=torch.float32)
    dummy_h = torch.zeros(1, 1, 128, dtype=torch.float32)

    torch.onnx.export(
        model,
        (dummy_x, dummy_h),
        path,
        export_params=True,
        opset_version=12,
        do_constant_folding=True,
        input_names=["x", "h_in"],
        output_names=["correction", "h_out"],
        dynamic_axes=None,  # static shapes → deterministic latency on RPi5
    )
    print(f"[EXPORT] GRU ONNX: {path}")


def compile_encoder_blob(
    onnx_path: str,
    output_path: str = None,
    shaves: int = 6,
) -> str:
    """
    Compile encoder ONNX to MyriadX .blob via blobconverter.

    CRITICAL: pins OpenVINO to version="2022.1" — the last stable release with
    full MyriadX (MYRIAD plugin) support. OpenVINO 2023.0+ removed MyriadX entirely.

    Args:
        onnx_path:   path to encoder.onnx
        output_path: where to copy the blob (optional; blobconverter returns cache path)
        shaves:      number of SHAVE cores (1–6 for OAK-D Lite; 6 = default)

    Returns:
        path to compiled .blob file
    """
    import blobconverter

    blob_path = blobconverter.from_onnx(
        model=onnx_path,
        data_type="FP16",
        shaves=shaves,
        use_cache=False,
        version="2022.1",  # MUST be ≤2022.3 for MyriadX
    )

    if output_path and output_path != blob_path:
        import shutil
        shutil.copy2(blob_path, output_path)
        blob_path = output_path

    print(f"[EXPORT] Encoder blob ({shaves} SHAVEs): {blob_path}")
    return blob_path
