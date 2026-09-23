from datetime import datetime, timezone

from config.settings import settings
from src.extract import extract_csv, extract_fx
from src.generator import generate_sources
from src.quality import validate, write_report
from src.transform import transform


def run(dry_run: bool = False, generate: bool = True, logger=None) -> dict:
    settings.ensure_directories()
    if generate or not (settings.bank_file.exists() and settings.card_file.exists() and settings.fx_file.exists()):
        generate_sources(settings.raw_dir)
    if logger:
        logger.info("Extracting synthetic bank, card, and FX sources")
    frame = transform(extract_csv(settings.bank_file), extract_csv(
        settings.card_file), extract_fx(settings.fx_file))
    report = validate(frame)
    invalid_ids = set(report["invalid_transaction_ids"])
    valid_frame = frame[
        ~frame["transaction_id"].isin(invalid_ids)
    ].copy()
    valid_frame.to_csv(settings.processed_file, index=False)
    write_report(report, settings.dq_report_file)
    loaded = 0
    if not dry_run:
        from src.loader import load_to_mysql
        loaded = load_to_mysql(
            valid_frame, settings, quality_passed=report["passed"])
    summary = {"run_at": datetime.now(timezone.utc).isoformat(), "dry_run": dry_run, "rows_processed": len(
        frame), "valid_rows": len(valid_frame), "invalid_rows": report["invalid_row_count"], "rows_loaded": loaded, "quality_passed": report["passed"], "output_file": str(settings.processed_file), "report_file": str(settings.dq_report_file)}
    if logger:
        logger.info("Processed %d rows; %d valid, %d invalid; quality_passed=%s",
                    len(frame), len(valid_frame), report["invalid_row_count"], report["passed"])
    return summary
