from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    root_dir: Path = ROOT_DIR
    raw_dir: Path = ROOT_DIR / "data" / "raw"
    processed_dir: Path = ROOT_DIR / "data" / "processed"
    reports_dir: Path = ROOT_DIR / "data" / "reports"
    logs_dir: Path = ROOT_DIR / "logs"
    bank_file: Path = ROOT_DIR / "data" / "raw" / "transactions_bank.csv"
    card_file: Path = ROOT_DIR / "data" / "raw" / "transactions_card.csv"
    fx_file: Path = ROOT_DIR / "data" / "raw" / "fx_rates.json"
    processed_file: Path = ROOT_DIR / "data" / "processed" / "transactions.csv"
    dq_report_file: Path = ROOT_DIR / "data" / \
        "reports" / "data_quality_report.json"
    log_file: Path = ROOT_DIR / "logs" / "pipeline.log"
    mysql_host: str = os.getenv("MYSQL_HOST", "localhost")
    mysql_port: int = int(os.getenv("MYSQL_PORT", "3306"))
    mysql_database: str = os.getenv("MYSQL_DATABASE", "financial_pipeline")
    mysql_user: str = os.getenv("MYSQL_USER", "pipeline_user")
    mysql_password: str = os.getenv("MYSQL_PASSWORD", "")

    def ensure_directories(self) -> None:
        for directory in (self.raw_dir, self.processed_dir, self.reports_dir, self.logs_dir):
            directory.mkdir(parents=True, exist_ok=True)


settings = Settings()
