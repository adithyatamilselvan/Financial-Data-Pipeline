import json

import pandas as pd

from config.settings import Settings
from src.generator import generate_sources
from src.quality import validate
from src.transform import transform
from src.extract import extract_csv, extract_fx
from src import pipeline


def test_generated_sources_transform_and_validate(tmp_path):
    paths = generate_sources(tmp_path)
    frame = transform(extract_csv(paths["bank"]), extract_csv(
        paths["card"]), extract_fx(paths["fx"]))
    assert len(frame) == 30
    assert frame["transaction_id"].is_unique
    assert {"amount_usd", "is_international",
            "transaction_month"}.issubset(frame.columns)
    report = validate(frame)
    assert len(report["checks"]) == 9
    assert any(check["check"] == "currency_check" and not check["passed"]
               for check in report["checks"])
    assert report["row_count"] == 30
    assert report["valid_row_count"] == 27
    assert report["invalid_row_count"] == 3
    assert report["invalid_transaction_ids"] == ["TX-0003", "TX-0006", "TX-0021"]


def test_dry_run_writes_only_valid_rows(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    reports_dir = tmp_path / "reports"
    logs_dir = tmp_path / "logs"
    temp_settings = Settings(
        root_dir=tmp_path,
        raw_dir=raw_dir,
        processed_dir=processed_dir,
        reports_dir=reports_dir,
        logs_dir=logs_dir,
        bank_file=raw_dir / "transactions_bank.csv",
        card_file=raw_dir / "transactions_card.csv",
        fx_file=raw_dir / "fx_rates.json",
        processed_file=processed_dir / "transactions.csv",
        dq_report_file=reports_dir / "data_quality_report.json",
        log_file=logs_dir / "pipeline.log",
    )
    monkeypatch.setattr(pipeline, "settings", temp_settings)

    summary = pipeline.run(dry_run=True)

    assert summary["rows_processed"] == 30
    assert summary["valid_rows"] == 27
    assert summary["invalid_rows"] == 3
    assert summary["rows_loaded"] == 0
    assert len(pd.read_csv(temp_settings.processed_file)) == 27
    report = json.loads(temp_settings.dq_report_file.read_text(encoding="utf-8"))
    assert report["invalid_transaction_ids"] == ["TX-0003", "TX-0006", "TX-0021"]


def test_quality_report_is_json_serializable(tmp_path):
    frame = pd.DataFrame({"transaction_id": ["TX-1"], "account_id": ["ACC-1"], "transaction_date": [
                         "2025-01-01"], "amount": [10], "currency": ["USD"], "category": ["Dining"], "status": ["completed"]})
    report = validate(frame)
    json.dumps(report)
    assert report["passed"]
