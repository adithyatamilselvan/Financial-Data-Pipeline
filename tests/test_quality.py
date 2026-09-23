import json

import pandas as pd
import pytest

from src.quality import validate, write_report


CHECK_NAMES = {
    "null_check",
    "duplicate_transaction_check",
    "schema_check",
    "amount_range_check",
    "anomaly_outlier_check",
    "date_range_check",
    "category_check",
    "status_check",
    "currency_check",
}


def valid_frame():
    return pd.DataFrame([
        {"transaction_id": "TX-1", "account_id": "ACC-1", "transaction_date": "2025-01-01",
            "amount": 100.0, "currency": "USD", "category": "Dining", "status": "completed"},
        {"transaction_id": "TX-2", "account_id": "ACC-2", "transaction_date": "2025-02-01",
            "amount": 200.0, "currency": "EUR", "category": "Travel", "status": "pending"},
    ])


def check(report, name):
    return next(item for item in report["checks"] if item["check"] == name)


def test_all_required_quality_checks_pass_for_valid_data():
    report = validate(valid_frame())

    assert report["passed"] is True
    assert {item["check"] for item in report["checks"]} == CHECK_NAMES
    assert len(report["checks"]) == 9


@pytest.mark.parametrize(("column", "check_name"), [
    ("amount", "null_check"),
    ("category", "null_check"),
    ("status", "status_check"),
    ("currency", "currency_check"),
])
def test_quality_detects_missing_values(column, check_name):
    frame = valid_frame()
    frame.loc[0, column] = None

    report = validate(frame)

    assert report["passed"] is False
    assert check(report, check_name)["passed"] is False


@pytest.mark.parametrize(("mutator", "check_name"), [
    (lambda frame: frame.__setitem__("transaction_id",
     ["TX-1", "TX-1"]), "duplicate_transaction_check"),
    (lambda frame: frame.__setitem__(
        "amount", [-1.0, 200.0]), "amount_range_check"),
    (lambda frame: frame.__setitem__("amount",
     [100.0, 200000.0]), "amount_range_check"),
    (lambda frame: frame.__setitem__(
        "amount", [1.0, None]), "anomaly_outlier_check"),
    (lambda frame: frame.__setitem__("transaction_date",
     ["2019-12-31", "2025-02-01"]), "date_range_check"),
    (lambda frame: frame.__setitem__("category", [
     "Uncategorized", "Travel"]), "category_check"),
    (lambda frame: frame.__setitem__("status",
     ["unknown", "pending"]), "status_check"),
    (lambda frame: frame.__setitem__(
        "currency", ["ZZZ", "EUR"]), "currency_check"),
])
def test_quality_detects_invalid_values(mutator, check_name):
    frame = valid_frame()
    mutator(frame)

    assert check(validate(frame), check_name)["passed"] is False


def test_schema_check_reports_missing_columns_without_crashing():
    frame = valid_frame().drop(columns=["status"])

    report = validate(frame)

    assert report["passed"] is False
    assert check(report, "schema_check")["failure_count"] == 1


def test_quality_report_is_written_as_structured_json(tmp_path):
    output = tmp_path / "report.json"
    write_report(validate(valid_frame()), output)

    saved = json.loads(output.read_text(encoding="utf-8"))
    assert saved["row_count"] == 2
    assert saved["passed"] is True
