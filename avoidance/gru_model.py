"""
ObstacleAvoidanceGRU — 1-layer GRU temporal head for reactive obstacle avoidance.

Runs on RPi5 via ONNX Runtime (NOT on MyriadX — GRU/LayerNorm unsupported on VPU).

Input vector composition (80-D per timestep):
    depth_feat  [64]  — CNN encoder output from MyriadX VPU
    imu_delta   [6]   — BMI270 accel (3) + gyro (3), standardized
    velocity    [3]   — LOCAL_POSITION_NED vx/vy/vz, divided by 10 m/s
    attitude    [4]   — quaternion [w,x,y,z] from ArduCopter ATTITUDE message
    goal_offset [3]   — NED vector to current sub-goal, divided by 50 m

Output:
    correction  [1, 3]   — NED correction vector in body frame, scaled to ±MAX_CORRECTION
    h_new       [1,1,128] — updated hidden state for next control cycle
"""

import torch
import torch.nn as nn


class ObstacleAvoidanceGRU(nn.Module):
    """1-layer GRU + LayerNorm + MLP head for single-step obstacle correction."""

    MAX_CORRECTION = 3.0  # meters — Tanh output scaled to ±this value

    def __init__(self):
        super().__init__()
        # GRU: input=80 (64+6+3+4+3), hidden=128, batch_first=False
        # batch_first=False → tensors are [seq, batch, features]
        self.gru = nn.GRU(
            input_size=80,
            hidden_size=128,
            num_layers=1,
            batch_first=False,
        )
        # LayerNorm on hidden output stabilises training (~50% faster convergence)
        self.layer_norm = nn.LayerNorm(128)

        # MLP output head: 128 → 64 → 3, bounded by Tanh
        self.mlp = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(inplace=True),
            nn.Linear(64, 3),
            nn.Tanh(),
        )

    def forward(
        self, x: torch.Tensor, h: torch.Tensor
    ):
        """
        Single-step inference (one control cycle).

        Args:
            x: [seq=1, batch=1, input=80]
            h: [num_layers=1, batch=1, hidden=128]

        Returns:
            correction: [batch=1, 3]   NED body-frame correction in [-MAX_CORRECTION, MAX_CORRECTION]
            h_new:      [1, batch=1, 128]  hidden state for next cycle
        """
        out, h_new = self.gru(x, h)              # out: [1, 1, 128]
        out = self.layer_norm(out[0])             # [1, 128]  (squeeze seq dim)
        correction = self.mlp(out) * self.MAX_CORRECTION  # [1, 3]
        return correction, h_new
