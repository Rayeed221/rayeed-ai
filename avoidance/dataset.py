"""
Dataset utilities for GRU obstacle avoidance training.

Source: Agile Autonomy dataset (Loquercio et al., Zenodo 5517791)
        https://zenodo.org/records/5517791
        58.5 GB of collision-free trajectory demonstrations at 7 m/s.

Each rollout directory must contain:
    depth.npy        [T, H, W]  float32 — simulated stereo depth in meters
    imu.npy          [T, 6]     float32 — accel(3) + gyro(3) per timestep
    vel.npy          [T, 3]     float32 — body-frame velocity (x,y,z) m/s
    attitude.npy     [T, 4]     float32 — quaternion [w,x,y,z]
    goal_offset.npy  [T, 3]     float32 — NED vector to current waypoint goal
    correction.npy   [T, 3]     float32 — expert correction labels (NED, meters)

Windows never cross rollout boundaries. Reset GRU hidden state between rollouts.
"""

import os
from typing import List, Tuple

import numpy as np
import torch
from torch.utils.data import Dataset


def preprocess_depth_for_oakd(depth_sim: np.ndarray) -> np.ndarray:
    """
    Adapt simulated depth to match OAK-D Lite SGM stereo characteristics.

    Args:
        depth_sim: H×W float32 depth in meters (arbitrary resolution)

    Returns:
        128×128 float32 in [0, 1]  (clipped to [0.2, 12.0] m effective range)
    """
    from PIL import Image
    import scipy.ndimage as ndi

    # 1. Resize to CNN input resolution
    img = Image.fromarray(depth_sim.astype(np.float32), mode="F")
    img = img.resize((128, 128), Image.BILINEAR)
    d = np.array(img, dtype=np.float32)

    # 2. Clip to OAK-D Lite stereo valid range
    d = np.clip(d, 0.2, 12.0)

    # 3. Quadratic SGM noise: sigma ∝ depth² (stereo depth noise model)
    sigma = 0.005 * d ** 2
    d = d + np.random.normal(0, sigma).astype(np.float32)
    d = np.clip(d, 0.2, 12.0)

    # 4. Random pixel dropout (3%) — simulates stereo matching failures
    dropout_mask = np.random.random(d.shape) < 0.03
    d[dropout_mask] = 12.0  # failed pixels → max range

    # 5. Edge erosion near far-range regions — stereo occlusion border artifacts
    far_mask = (d > 10.0)
    eroded = ndi.binary_dilation(far_mask, iterations=1)
    d[eroded] = 12.0

    # 6. Normalize to [0, 1]
    d = (d - 0.2) / (12.0 - 0.2)

    return d.astype(np.float32)


def generate_gru_sequences(
    dataset_root: str,
    N: int = 5,
    stride: int = 1,
) -> List[Tuple[np.ndarray, ...]]:
    """
    Sliding-window extraction over Agile Autonomy rollout directories.

    Windows do NOT cross rollout boundaries. GRU hidden state is reset
    between rollouts during training (h_0 = zeros at each window start).

    Args:
        dataset_root: path containing rollout_* subdirectories
        N:            window length (number of timesteps per sequence)
        stride:       step between windows (default 1 = fully overlapping)

    Returns:
        List of tuples: (depths, imus, vels, atts, goals, targets)
        Each array has shape [N, ...] matching the field dimensions above.
    """
    sequences: List[Tuple[np.ndarray, ...]] = []

    rollout_dirs = sorted([
        os.path.join(dataset_root, d)
        for d in os.listdir(dataset_root)
        if os.path.isdir(os.path.join(dataset_root, d))
    ])

    required_files = [
        "depth.npy", "imu.npy", "vel.npy",
        "attitude.npy", "goal_offset.npy", "correction.npy",
    ]

    for rollout_dir in rollout_dirs:
        if not all(
            os.path.exists(os.path.join(rollout_dir, f))
            for f in required_files
        ):
            continue

        depths   = np.load(os.path.join(rollout_dir, "depth.npy"))
        imus     = np.load(os.path.join(rollout_dir, "imu.npy"))
        vels     = np.load(os.path.join(rollout_dir, "vel.npy"))
        atts     = np.load(os.path.join(rollout_dir, "attitude.npy"))
        goals    = np.load(os.path.join(rollout_dir, "goal_offset.npy"))
        targets  = np.load(os.path.join(rollout_dir, "correction.npy"))

        T = len(depths)
        if T < N:
            continue

        # Sliding window — last window starts at T-N, never goes beyond T
        for start in range(0, T - N + 1, stride):
            end = start + N
            sequences.append((
                depths[start:end],    # [N, H, W]
                imus[start:end],      # [N, 6]
                vels[start:end],      # [N, 3]
                atts[start:end],      # [N, 4]
                goals[start:end],     # [N, 3]
                targets[start:end],   # [N, 3]
            ))

    return sequences


class AgileAutonomyDataset(Dataset):
    """
    PyTorch Dataset wrapping Agile Autonomy GRU training sequences.

    Each item is a dict of tensors matching the GRU trainer's expected input format.
    Depth preprocessing (resize, noise, dropout, normalization) is applied per frame.
    """

    def __init__(
        self,
        dataset_root: str,
        N: int = 5,
        stride: int = 1,
    ):
        self.sequences = generate_gru_sequences(dataset_root, N=N, stride=stride)

    def __len__(self) -> int:
        return len(self.sequences)

    def __getitem__(self, idx: int) -> dict:
        depths, imus, vels, atts, goals, targets = self.sequences[idx]

        # Apply OAK-D sim-to-real preprocessing to each depth frame in the window
        processed = np.stack([
            preprocess_depth_for_oakd(depths[i]) for i in range(len(depths))
        ])  # [N, 128, 128]

        return {
            # [N, 1, 128, 128] — channel dim added for CNN encoder
            "depths":  torch.from_numpy(processed).unsqueeze(1).float(),
            "imus":    torch.from_numpy(imus).float(),    # [N, 6]
            "vels":    torch.from_numpy(vels).float(),    # [N, 3]
            "atts":    torch.from_numpy(atts).float(),    # [N, 4]
            "goals":   torch.from_numpy(goals).float(),   # [N, 3]
            "targets": torch.from_numpy(targets).float(), # [N, 3]
        }
