from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent
OFFERINGS_CSV = DATA_DIR / "offerings.csv"
OFFERING_COLUMNS = "Infernal Offering"

def load_offerings() -> list[str]:
    df = pd.read_csv(OFFERINGS_CSV)
    if OFFERING_COLUMNS not in df.columns:
        raise KeyError(
            f"No offering column found in {OFFERINGS_CSV}. "
            f"Expected column {OFFERING_COLUMNS}, found {tuple(df.columns)}."
        )
    return df[OFFERING_COLUMNS].dropna().astype(str).tolist()

def is_offering(offering: str) -> bool:
    return offering in load_offerings()