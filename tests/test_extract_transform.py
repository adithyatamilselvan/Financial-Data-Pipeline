import json

import pandas as pd
import pytest

from src.extract import extract_csv, extract_fx
from src.generator import generate_sources
from src.transform import transform


def test_extract_csv_and_fx_read_generated_sources(tmp_path):
    paths = generate_sources(tmp_path)

    bank = extract_csv(paths["bank"])
    fx = extract_fx(paths["fx"])

    assert len(bank) == 19
    assert bank.loc[0, "bank_txn_id"] == "TX-0001"
    assert fx["base_currency"] == "USD"
    assert fx["rates"]["EUR"] == 1.09


def test_extract_missing_files_raise_clear_standard_errors(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_csv(tmp_path / "missing.csv")
    with pytest.raises(FileNotFoundError):
        extract_fx(tmp_path / "missing.json")


def test_transform_deduplicates_converts_and_enriches(tmp_path):
    paths = generate_sources(tmp_path)
    result = transform(extract_csv(paths["bank"]), extract_csv(
        paths["card"]), extract_fx(paths["fx"]))

    assert len(result) == 30
    assert result["transaction_id"].is_unique
    assert pd.api.types.is_datetime64_any_dtype(result["transaction_date"])
    assert pd.api.types.is_float_dtype(result["amount"])
    assert result.loc[result["transaction_id"] == "TX-0001",
                      "amount_usd"].iloc[0] == pytest.approx(32.6782)
    assert bool(result.loc[result["transaction_id"] ==
                "TX-0001", "is_international"].iloc[0]) is True
    assert result.loc[result["transaction_id"] ==
                      "TX-0001", "category"].iloc[0] == "Dining"
    assert result.loc[result["transaction_id"] ==
                      "TX-0002", "status"].iloc[0] == "completed"


def test_transform_preserves_missing_values_for_quality_checks():
    bank = pd.DataFrame([{
        "bank_txn_id": "TX-1", "account_number": None, "transaction_date": "2025-01-01",
        "amount": "bad", "currency": None, "merchant": None, "category": None,
        "status": "unknown", "source": "bank",
    }])
    card = pd.DataFrame(columns=["card_txn_id", "card_account", "posted_date",
                        "amount", "currency", "merchant_name", "category", "status", "source"])
    result = transform(
        bank, card, {"base_currency": "USD", "rates": {"USD": 1.0}})

    row = result.iloc[0]
    assert pd.isna(row["account_id"])
    assert pd.isna(row["amount"])
    assert pd.isna(row["currency"])
    assert row["merchant"] == "Unknown merchant"
    assert row["category"] == "Uncategorized"
    assert row["status"] == "unknown"
