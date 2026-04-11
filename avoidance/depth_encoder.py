"""
DepthEncoder — MobileNetV3-Small modified for single-channel depth input.

Runs on OAK-D Lite MyriadX VPU as a compiled .blob (FP16, 6 SHAVEs).
Input:  [1, 1, 128, 128]  — U8/FP16 depth normalized to [0, 1]
Output: [1, 64]           — FP16 spatial feature vector

Compilation:
    export_encoder_onnx(model, "encoder.onnx")
    compile_encoder_blob("encoder.onnx", shaves=6)  # → encoder.blob

Note: OpenVINO must be ≤2022.3 for MyriadX (MYRIAD plugin removed in 2023+).
"""

import torch
import torch.nn as nn
import torchvision.models as models


class DepthEncoder(nn.Module):
    """MobileNetV3-Small modified for 1-channel depth → 64-D feature vector."""

    def __init__(self):
        super().__init__()
        backbone = models.mobilenet_v3_small(
            weights=models.MobileNet_V3_Small_Weights.DEFAULT
        )

        # Patch first conv: 3-channel RGB → 1-channel depth
        # Average the RGB weights so pretrained filters are preserved
        orig_conv = backbone.features[0][0]  # Conv2d(3, 16, k=3, s=2, p=1)
        new_conv = nn.Conv2d(
            1, orig_conv.out_channels,
            kernel_size=orig_conv.kernel_size,
            stride=orig_conv.stride,
            padding=orig_conv.padding,
            bias=orig_conv.bias is not None,
        )
        with torch.no_grad():
            new_conv.weight.copy_(orig_conv.weight.mean(dim=1, keepdim=True))
        backbone.features[0][0] = new_conv

        # Feature extraction backbone (12 InvertedResidual blocks → 576ch @ 4×4)
        self.features = backbone.features
        # AdaptiveAvgPool2d(1) → [B, 576, 1, 1]
        self.pool = backbone.avgpool

        # Projection head: 576 → 256 → 64
        self.proj = nn.Sequential(
            nn.Flatten(),
            nn.Linear(576, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, 64),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: [B, 1, 128, 128] depth image, float32 in [0, 1]
        Returns:
            [B, 64] feature vector
        """
        x = self.features(x)   # [B, 576, 4, 4]  (for 128×128 input)
        x = self.pool(x)       # [B, 576, 1, 1]
        x = self.proj(x)       # [B, 64]
        return x
