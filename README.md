# Financial Transaction Data Pipeline

A small, local-only ETL pipeline for synthetic bank and card transactions. It extracts CSV and JSON sources, standardizes and enriches transactions, runs data-quality checks, writes analytics-ready files, and can load them into MySQL 8+.

## Setup

Requires Python 3.11+. Create an environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set MySQL credentials only when using a database load.

## Run

The autonomous dry run generates fresh synthetic input, processes it, writes `data/processed/transactions.csv` and `data/reports/data_quality_report.json`, and does not contact MySQL:

```powershell
python scripts/run_pipeline.py --dry-run
```

Run with MySQL after creating the database and tables from `sql/schema.sql`:

```powershell
mysql -u root -p < sql/schema.sql
python scripts/run_pipeline.py
```

Analytics queries are in `sql/analytics.sql`. Logs are written to `logs/pipeline.log`.

The quality report contains eight required validation checks from the pipeline specification: nulls, duplicate IDs, schema, amount range, anomalies/outliers, date range, category, and status. It also includes a ninth, useful source-integrity check for supported currencies because FX conversion depends on known currency codes.

## Project layout

- `config/`: environment-backed settings
- `data/raw/`: generated source extracts
- `data/processed/`: standardized transaction output
- `data/reports/`: JSON quality reports
- `src/`: generator, extraction, transformation, validation, loading, and orchestration
- `sql/`: MySQL schema and analytics
- `tests/`: pytest coverage for extraction, transformation, edge cases, and all quality checks
