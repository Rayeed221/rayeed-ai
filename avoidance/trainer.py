"""
AvoidanceTrainer — joint training pipeline for DepthEncoder + ObstacleAvoidanceGRU.

Training strategy:
  Phase 1: Behaviour cloning on Agile Autonomy offline dataset (MSE loss, ~150 epochs)
  Phase 2: DAgger in simulation (β-decay rollouts, privileged expert re-labelling)
  Phase 3: Fine-tune on real OAK-D Lite depth from target environments

Loss: MSE on single-mode NED correction (not R-WTA — single output head, no hypothesis collapse risk).
Optimizer: AdamW with weight decay for better generalisation on sim-to-real transfer.
Scheduler: CosineAnnealingLR — smooth LR decay across the training horizon.
Grad clip: max_norm=1.0 — critical for RNN stability.
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from avoidance.depth_encoder import DepthEncoder
from avoidance.gru_model import ObstacleAvoidanceGRU


class AvoidanceTrainer:
    """
    Trains DepthEncoder and ObstacleAvoidanceGRU jointly on sliding-window sequences.

    The GRU is unrolled step-by-step over N timesteps per batch. MSE is accumulated
    at each step and averaged — this ensures the model learns from all intermediate
    corrections, not just the final one.
    """

    def __init__(
        self,
        encoder: DepthEncoder,
        gru: ObstacleAvoidanceGRU,
        lr: float = 1e-3,
        device: str = "cpu",
    ):
        self.encoder = encoder.to(device)
        self.gru     = gru.to(device)
        self.device  = device

        self.optimizer = torch.optim.AdamW(
            list(encoder.parameters()) + list(gru.parameters()),
            lr=lr,
            weight_decay=1e-4,
        )
        self.criterion = nn.MSELoss()
        # T_max should be set to total epochs — default 50 for convenience
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=50, eta_min=1e-5
        )
        self._grad_clip = 1.0

    def train_epoch(self, dataloader: DataLoader) -> float:
        """
        Run one training epoch over all batches.

        Each batch contains N-step sequences. The GRU is unrolled step-by-step;
        MSE is computed at each step against the expert label and averaged.

        Args:
            dataloader: yields dicts with keys depths/imus/vels/atts/goals/targets

        Returns:
            average MSE loss over the epoch
        """
        self.encoder.train()
        self.gru.train()

        total_loss = 0.0
        n_batches  = 0

        for batch in dataloader:
            depths  = batch["depths"].to(self.device)   # [B, N, 1, 128, 128]
            imus    = batch["imus"].to(self.device)      # [B, N, 6]
            vels    = batch["vels"].to(self.device)      # [B, N, 3]
            atts    = batch["atts"].to(self.device)      # [B, N, 4]
            goals   = batch["goals"].to(self.device)     # [B, N, 3]
            targets = batch["targets"].to(self.device)   # [B, N, 3]

            B, N = depths.shape[:2]

            # Initialize hidden state fresh per batch (matches inference reset on new goal)
            h = torch.zeros(1, B, 128, device=self.device)

            self.optimizer.zero_grad()
            batch_loss = torch.zeros(1, device=self.device)

            # Unroll GRU across N timesteps
            for t in range(N):
                # Encode depth frame t: [B, 1, 128, 128] → [B, 64]
                depth_feat = self.encoder(depths[:, t])

                # Assemble 80-D state vector: 64+6+3+4+3 = 80
                state_t = torch.cat([
                    depth_feat,      # [B, 64]
                    imus[:, t],      # [B, 6]
                    vels[:, t],      # [B, 3]
                    atts[:, t],      # [B, 4]
                    goals[:, t],     # [B, 3]
                ], dim=-1)           # [B, 80]

                # GRU expects [seq=1, batch=B, features=80]
                x = state_t.unsqueeze(0)   # [1, B, 80]
                correction, h = self.gru(x, h)  # correction: [B, 3]

                # Accumulate MSE against expert label at this timestep
                batch_loss = batch_loss + self.criterion(correction, targets[:, t])

            # Average over unrolled steps
            batch_loss = batch_loss / N
            batch_loss.backward()

            nn.utils.clip_grad_norm_(
                list(self.encoder.parameters()) + list(self.gru.parameters()),
                max_norm=self._grad_clip,
            )
            self.optimizer.step()

            total_loss += batch_loss.item()
            n_batches  += 1

        self.scheduler.step()
        return total_loss / max(n_batches, 1)
