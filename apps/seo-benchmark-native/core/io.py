from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict

import pandas as pd


def read_csv_strict(path: Path) -> pd.DataFrame:
    """Read CSV as strings to preserve raw values and avoid type coercion drift."""
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(col).strip() for col in out.columns]
    return out


def ensure_output_dir(base_output_root: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = base_output_root / ts
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def load_input_frames(input_paths: Dict[str, Path]) -> Dict[str, pd.DataFrame]:
    frames: Dict[str, pd.DataFrame] = {}
    for key, path in input_paths.items():
        frames[key] = normalize_columns(read_csv_strict(path))
    return frames


def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
