# 💳 Financial Transaction Data Pipeline

An end-to-end **ETL and data quality pipeline** built using **Python, Pandas, and MySQL** to process synthetic bank and card transaction data.

The pipeline extracts transaction data from multiple sources, cleans and standardizes the records, performs automated data-quality validation, enriches the transactions with analytical fields, separates valid and invalid records, stores the cleaned data in MySQL, and provides SQL queries for financial transaction analysis.

This project demonstrates a complete data engineering workflow from **raw data ingestion to analytics-ready data**.

---

## 📌 Project Overview

Financial transaction data is often collected from multiple systems and may contain inconsistent formats, missing values, duplicate records, invalid currencies, incorrect categories, or unusual transaction amounts.

Loading such raw data directly into a database can result in unreliable analytics and poor data quality.

This project solves that problem by creating an automated pipeline that:

- Extracts data from multiple transaction sources
- Combines bank and card transaction data
- Standardizes different column formats
- Cleans and transforms raw records
- Converts transaction amounts into USD
- Creates additional analytical fields
- Performs automated data-quality checks
- Identifies invalid transactions
- Keeps invalid records out of the main database table
- Generates a detailed data-quality report
- Loads only valid records into MySQL
- Tracks pipeline execution
- Provides SQL analytics for business analysis
- Includes automated tests using pytest

The project uses **synthetic financial data**, so no real customer, banking, or payment information is involved.

---

# 🎯 Problem Statement

Raw financial transaction data can come from different systems such as:

- Bank transaction systems
- Credit/debit card systems
- Currency exchange-rate sources

Each source may have different formats and may contain data-quality problems.

For example, a transaction may contain:

- Missing transaction amount
- Duplicate transaction ID
- Unsupported currency
- Invalid category
- Invalid status
- Out-of-range transaction amount
- Unexpected date
- Missing values
- Potential anomalies

If these records are directly inserted into a database, they can affect downstream reports and business decisions.

### Solution

This project introduces an automated ETL pipeline that validates the data before it reaches the database.

```text
Raw Transaction Data
        ↓
     Extract
        ↓
     Transform
        ↓
   Data Quality
    Validation
        ↓
 ┌──────┴──────┐
 ↓             ↓
Valid         Invalid
Records       Records
 ↓             ↓
MySQL       DQ Report
 ↓
SQL Analytics

🏗️ Pipeline Architecture
                    ┌─────────────────────┐
                    │  Bank Transactions  │
                    │      CSV            │
                    └──────────┬──────────┘
                               │
                               │
                    ┌──────────▼──────────┐
                    │  Card Transactions  │
                    │       CSV           │
                    └──────────┬──────────┘
                               │
                               │
                    ┌──────────▼──────────┐
                    │   Exchange Rates    │
                    │       JSON          │
                    └──────────┬──────────┘
                               │
                               ▼
                       ┌──────────────┐
                       │   EXTRACT    │
                       └──────┬───────┘
                              │
                              ▼
                       ┌──────────────┐
                       │  TRANSFORM   │
                       │   & CLEAN    │
                       └──────┬───────┘
                              │
                              ▼
                       ┌──────────────┐
                       │  VALIDATE    │
                       │ DATA QUALITY │
                       └──────┬───────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
              Valid Records       Invalid Records
                    │                   │
                    ▼                   ▼
             Processed CSV       Quality Report
                    │
                    ▼
                 MySQL
                    │
                    ▼
              SQL Analytics

🔄 Complete Working Process
1. Data Generation & Extraction

The project works with synthetic transaction sources representing different financial systems.

Input sources

data/raw/
├── transactions_bank.csv
├── transactions_card.csv
└── exchange_rates.json

The pipeline extracts:

Bank transactions
Card transactions
Currency exchange rates

The exchange-rate data is used to convert supported transaction currencies into USD.

2. Data Standardization

Since transaction data can originate from different sources, the pipeline first standardizes the records.

The transformation process includes:

Standardizing column names
Standardizing transaction IDs
Standardizing account IDs
Normalizing currency codes
Converting transaction dates to the correct date format
Converting transaction amounts to numeric values
Normalizing categories
Normalizing transaction status values
Handling missing values
Removing duplicate transaction IDs

The goal is to create a consistent transaction structure regardless of the original source.

3. Data Transformation & Enrichment

After cleaning the raw records, the pipeline generates additional fields that are useful for analytics.

Important derived fields

| Field               | Purpose                                          |
| ------------------- | ------------------------------------------------ |
| `amount_usd`        | Standardizes supported currencies into USD       |
| `is_international`  | Identifies international transactions            |
| `transaction_month` | Supports monthly spending analysis               |
| `day_of_week`       | Supports weekday/weekend spending analysis       |
| `transaction_type`  | Identifies transaction type such as debit/credit |

For example:
Original Amount:     8500 INR
Exchange Rate:       INR → USD
        ↓
amount_usd:          Converted USD value

Original Amount:     8500 INR
Exchange Rate:       INR → USD
        ↓
amount_usd:          Converted USD value

🔍 Data Quality Validation

Data validation is one of the major components of this project.

Before records are loaded into MySQL, the pipeline checks whether they satisfy the defined data-quality rules.

Validation checks include:
Null value validation
Duplicate transaction ID validation
Schema validation
Transaction amount range validation
Anomaly / outlier validation
Transaction date range validation
Category validation
Status validation
Supported currency validation

The supported-currency check is important because currency conversion depends on the availability of a valid exchange rate.

🚦 Valid & Invalid Record Handling

The pipeline does not simply fail when it finds bad data.

Instead, it separates valid and invalid records.

              30 Input Records
                     │
                     ▼
              Data Validation
                     │
              ┌──────┴──────┐
              │             │
              ▼             ▼
        27 Valid Rows    3 Invalid Rows
              │             │
              ▼             ▼
     Processed CSV       DQ Report
              │
              ▼
          MySQL Load

Current pipeline result
Rows processed : 30
Valid rows     : 27
Invalid rows   : 3
Rows loaded    : 27

The invalid records in the current synthetic dataset include examples such as:

An unsupported currency (ZZZ)
A missing transaction amount
An invalid transaction category

The invalid records are excluded from the main transaction load so that the database contains only valid transaction records.

📋 Data Quality Report

The pipeline generates:

data/reports/data_quality_report.json

The report provides an audit-friendly summary of the pipeline's validation results.

Example:

{
    "rows_processed": 30,
    "valid_rows": 27,
    "invalid_rows": 3,
    "quality_passed": false
}

quality_passed: false means that data-quality issues were detected in the input data.

It does not mean that the pipeline execution failed.

The pipeline can successfully complete while identifying and excluding invalid records.

📁 Pipeline Outputs

The pipeline produces several useful outputs.

1. Processed Transaction Dataset
data/processed/transactions.csv

Contains the cleaned, standardized, validated and enriched transaction records.

Important columns include:

transaction_id
account_id
transaction_date
amount
currency
amount_usd
merchant
category
status
source
is_international
transaction_month
day_of_week
transaction_type
2. Data Quality Report
data/reports/data_quality_report.json

Contains:

Total rows processed
Valid row count
Invalid row count
Validation results
Invalid transaction IDs
Quality status
Pipeline execution information
3. Pipeline Log
logs/pipeline.log

The log records pipeline execution details such as:

Data extraction
Transformation
Validation
Valid/invalid record counts
Database loading
Pipeline execution status
🗄️ MySQL Database

Validated records can be loaded into:

financial_pipeline

The database contains three main tables.

financial_pipeline
│
├── transactions
├── pipeline_runs
└── transaction_anomalies
transactions

Stores the final validated transaction records used for analysis.

pipeline_runs

Tracks each pipeline execution, including:

Start time
Completion time
Rows processed
Rows loaded
Quality status
Pipeline status
Error information
transaction_anomalies

Stores detected transaction anomalies and their associated details.

📊 SQL Analytics

The project includes SQL analytics queries in:

sql/analytics.sql

The processed transaction data can be used to answer questions such as:

How does spending change month by month?
Which categories have the highest spending?
Which merchants receive the most transactions?
How much spending is international vs domestic?
Which accounts have higher transaction volumes?
How does debit spending compare with credit spending?
What is the distribution of transaction statuses?
Which days of the week have higher spending?
Which currencies are present in the dataset?
What is the rolling 3-month spending average?

This demonstrates how the cleaned pipeline output can move from data engineering → database → business analytics.

🧪 Testing

The project uses pytest for automated testing.

Tests cover areas such as:

Data extraction
Data transformation
Data validation
Duplicate handling
Missing values
Invalid records
Currency validation
Edge cases
Pipeline behavior

Current test result:

22 passed

The tests help ensure that changes to the pipeline do not break existing functionality.

🚀 Setup
Requirements
Python 3.11+
MySQL 8+
Git
VS Code or another Python IDE
1. Clone the repository
git clone https://github.com/adithyatamilselvan/Financial-Data-Pipeline.git
cd Financial-Data-Pipeline
2. Create a virtual environment
python -m venv .venv

Activate it:

.\.venv\Scripts\Activate.ps1
3. Install dependencies
python -m pip install -r requirements.txt
▶️ Running the Pipeline
Dry Run

The dry run processes the data without loading records into MySQL.

python scripts/run_pipeline.py --dry-run

The dry run produces:

Processed transaction CSV
Data quality report
Pipeline logs

and does not perform the database load.

Full Pipeline

Configure the MySQL credentials in the environment configuration and create the database/tables using:

sql/schema.sql

Then run:

python scripts/run_pipeline.py

The pipeline will:

Generate / Extract Data
        ↓
Transform & Clean
        ↓
Validate
        ↓
Separate Valid / Invalid Records
        ↓
Write Processed CSV
        ↓
Generate Quality Report
        ↓
Load Valid Records into MySQL
        ↓
Record Pipeline Run
📈 Example Pipeline Result

A successful execution of the current synthetic dataset produces:

Rows processed : 30
Valid rows     : 27
Invalid rows   : 3
Rows loaded    : 27
Quality passed : False
```
