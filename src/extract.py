import json
from pathlib import Path

import pandas as pd


def extract_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def extract_fx(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
