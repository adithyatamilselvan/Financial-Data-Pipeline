import json
from pathlib import Path

import pandas as pd

from src.transform import REQUIRED_CURRENCIES


def _check(name: str, passed: bool, failures: int, details: str) -> dict:
    return {"check": name, "passed": bool(passed), "failure_count": int(failures), "details": details}


def validate(frame: pd.DataFrame) -> dict:
    required = {"transaction_id", "account_id", "transaction_date",
                "amount", "currency", "category", "status"}
    schema_failures = len(required - set(frame.columns))
    available_required = list(required.intersection(frame.columns))
    nulls = int(frame[available_required].isna().any(
        axis=1).sum()) if available_required else 0
    duplicates = int(frame["transaction_id"].duplicated(
    ).sum()) if "transaction_id" in frame else 0
    amounts = pd.to_numeric(frame.get("amount", pd.Series(
        index=frame.index, dtype="float64")), errors="coerce")
    dates = pd.to_datetime(frame.get("transaction_date", pd.Series(
        index=frame.index, dtype="object")), errors="coerce")
    valid_statuses = {"completed", "pending", "failed", "reversed"}
    categories = frame.get("category", pd.Series(
        index=frame.index, dtype="object"))
    statuses = frame.get("status", pd.Series(
        index=frame.index, dtype="object"))
    currencies = frame.get("currency", pd.Series(
        index=frame.index, dtype="object"))
    amount_limit = amounts.quantile(0.99) * 3
    invalid_rows = {
        "null_check": frame[available_required].isna().any(axis=1) if available_required else pd.Series(True, index=frame.index),
        "duplicate_transaction_check": frame["transaction_id"].duplicated(keep=False) if "transaction_id" in frame else pd.Series(True, index=frame.index),
        "schema_check": pd.Series(schema_failures > 0, index=frame.index),
        "amount_range_check": amounts.isna() | (amounts < 0) | (amounts > 100000),
        "anomaly_outlier_check": amounts.isna() | (amounts > amount_limit),
        "date_range_check": dates.isna() | ~dates.between("2020-01-01", "2030-12-31"),
        "category_check": categories.isna() | (categories == "Uncategorized"),
        "status_check": ~statuses.isin(valid_statuses),
        "currency_check": ~currencies.isin(REQUIRED_CURRENCIES),
    }
    checks = [
        _check("null_check", nulls == 0, nulls,
               "Required fields must be populated"),
        _check("duplicate_transaction_check", duplicates == 0,
               duplicates, "Transaction IDs must be unique"),
        _check("schema_check", schema_failures == 0,
               schema_failures, "Required columns are present"),
        _check("amount_range_check", bool(amounts.notna().all() and (amounts >= 0).all() and (amounts <= 100000).all()), int(
            amounts.isna().sum() + (amounts < 0).sum() + (amounts > 100000).sum()), "Amounts must be between 0 and 100000"),
        _check("anomaly_outlier_check", bool(amounts.notna().all() and (amounts <= amounts.quantile(0.99) * 3).all()),
               int(amounts.isna().sum() + (amounts > amounts.quantile(0.99) * 3).sum()), "Flags missing or extreme amounts"),
        _check("date_range_check", bool(dates.notna().all() and dates.between(
            "2020-01-01", "2030-12-31").all()), int(dates.isna().sum()), "Dates must be valid and within expected range"),
        _check("category_check", bool("category" in frame and frame["category"].notna().all() and (frame["category"] != "Uncategorized").all()), int(frame.get(
            "category", pd.Series(index=frame.index)).isna().sum() + (frame.get("category", pd.Series(index=frame.index)) == "Uncategorized").sum()), "Categories must be normalized"),
        _check("status_check", bool("status" in frame and frame["status"].isin({"completed", "pending", "failed", "reversed"}).all()), int(
            (~frame.get("status", pd.Series(index=frame.index)).isin({"completed", "pending", "failed", "reversed"})).sum()), "Statuses must be normalized"),
    ]
    invalid_currency = int((~frame.get("currency", pd.Series(
        index=frame.index)).isin(REQUIRED_CURRENCIES)).sum())
    checks.append(_check("currency_check", invalid_currency == 0,
                  invalid_currency, "Currencies must be supported"))
    invalid_mask = pd.DataFrame(invalid_rows, index=frame.index).any(axis=1)
    invalid_ids = frame.loc[invalid_mask, "transaction_id"].dropna().astype(str).tolist() if "transaction_id" in frame else []
    return {
        "row_count": len(frame),
        "passed": all(item["passed"] for item in checks),
        "valid_row_count": int((~invalid_mask).sum()),
        "invalid_row_count": int(invalid_mask.sum()),
        "invalid_transaction_ids": invalid_ids,
        "checks": checks,
    }


def write_report(report: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2,
                    default=str), encoding="utf-8")
