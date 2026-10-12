import torch
import torch.nn as nn


class SimpleNN(nn.Module):
    """
    Expected input is the features in SimpleDataset.
    - Difficulty
    - RunID
    - RoundID
    - Choice

    Expected output is the total aether as an integer.
    """

    def __init__(self, input_features: int = 4):
        super().__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_features, 16),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(16, 1),
        )

    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits
