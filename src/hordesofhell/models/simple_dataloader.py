import csv
from pathlib import Path
from typing import Any

import torch
from torch.utils.data import DataLoader, Dataset, Subset

class SimpleDataset(Dataset[tuple[torch.Tensor, torch.Tensor]]):
    """
    Features:
    - Difficulty: one-hot encoded
    - RunID: int
    - RoundID: int
    - Choice: one-hot encoded

    Target:
    - Total Aether: int
    """

    def __init__(self, csv_file: Path):
        if not csv_file.exists() or not csv_file.is_file():
            msg = f"CSV file not found: {csv_file}"
            raise FileNotFoundError(msg)

        with csv_file.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        difficulties = sorted({self._clean_value(row["Difficulty"]) for row in rows})
        choices = sorted({self._clean_choice(row["Choice"]) for row in rows})

        self.difficulty_to_index = {name: idx for idx, name in enumerate(difficulties)}
        self.choice_to_index = {name: idx for idx, name in enumerate(choices)}
        self.index_to_choice = {idx: name for name, idx in self.choice_to_index.items()}

        run_ids = torch.tensor([int(self._clean_value(row["RunID"])) for row in rows], dtype=torch.int32)
        round_ids = torch.tensor([int(self._clean_value(row["RoundID"])) for row in rows], dtype=torch.int32)
        total_aether_raw = torch.tensor(
            [int(self._clean_value(row["Total Aether"])) for row in rows],
            dtype=torch.int32,
        )

        feature_rows: list[torch.Tensor] = []
        targets: list[torch.Tensor] = []

        for idx, row in enumerate(rows):
            difficulty = self._clean_value(row["Difficulty"])
            choice = self._clean_choice(row["Choice"])

            difficulty_vec = torch.zeros(len(self.difficulty_to_index), dtype=torch.float32)
            difficulty_vec[self.difficulty_to_index[difficulty]] = 1.0
            choice_vec = torch.zeros(len(self.choice_to_index), dtype=torch.float32)
            choice_vec[self.choice_to_index[choice]] = 1.0

            numeric_vec = torch.tensor(
                [run_ids[idx].item(), round_ids[idx].item()],
                dtype=torch.float32,
            )

            feature_rows.append(torch.cat((difficulty_vec, numeric_vec, choice_vec), dim=0))
            targets.append(total_aether_raw[idx].unsqueeze(0))

        self.features = torch.stack(feature_rows)
        self.targets = torch.stack(targets)
        self.input_features = self.features.shape[1]
        self.choice_classes = len(self.choice_to_index)

    def __len__(self) -> int:
        return self.features.shape[0]

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.features[index], self.targets[index]

    @staticmethod
    def _clean_value(value: str) -> str:
        return value.strip()

    @staticmethod
    def _clean_choice(value: str) -> str:
        return value.strip().lower()


def create_simple_dataloaders(
    csv_path: Path,
    batch_size: int = 16,
    train_split: float = 0.8,
    seed: int = 42,
) -> tuple[DataLoader[Any], DataLoader[Any], dict[str, Any]]:
    """
    Creates train/validation DataLoaders for simple_output.csv.
    """

    if not 0 < train_split < 1:
        msg = f"train_split must be in (0, 1), got {train_split}"
        raise ValueError(msg)

    dataset = SimpleDataset(csv_path)
    dataset_size = len(dataset)
    train_size = int(dataset_size * train_split)
    val_size = dataset_size - train_size

    generator = torch.Generator().manual_seed(seed)
    permutation = torch.randperm(dataset_size, generator=generator).tolist()
    train_indices = permutation[:train_size]
    val_indices = permutation[train_size:]

    train_subset = Subset(dataset, train_indices)
    val_subset = Subset(dataset, val_indices)

    train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_subset, batch_size=batch_size, shuffle=False)

    metadata = {
        "input_features": dataset.input_features,
        "choice_classes": dataset.choice_classes,
        "choice_to_index": dataset.choice_to_index,
        "index_to_choice": dataset.index_to_choice,
        "difficulty_to_index": dataset.difficulty_to_index,
        "train_size": train_size,
        "val_size": val_size,
    }

    return train_loader, val_loader, metadata