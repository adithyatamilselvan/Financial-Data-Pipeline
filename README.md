# 💳 Financial Transaction Data Pipeline

An end-to-end **ETL and data quality pipeline** built using **Python, Pandas, NumPy, and MySQL** to process synthetic bank and card transaction data.

The pipeline extracts transaction data from multiple sources, standardizes and cleans the records, performs automated data-quality validation, enriches transactions with analytical fields, separates valid and invalid records, stores validated data in MySQL, and provides SQL queries for financial transaction analysis.

This project demonstrates a complete workflow from **raw transaction data → data cleaning → validation → processed data → database → analytics**.

> **Note:** This project uses synthetic financial data. No real customer, banking, or payment information is used.

---

## 📌 Project Overview

Financial transaction data can come from multiple systems such as banking platforms, card systems, and currency-related sources. Because these systems may use different formats and contain incomplete or invalid records, raw data cannot always be loaded directly into a database.

Common data-quality problems include:

- Missing transaction amounts
- Duplicate transaction IDs
- Unsupported currencies
- Invalid transaction categories
- Invalid transaction statuses
- Incorrect date formats
- Missing values
- Unusual or out-of-range transaction amounts
- Potential transaction anomalies

This project solves these problems by building an automated ETL pipeline that:

- Extracts transaction data from multiple sources
- Combines bank and card transaction data
- Standardizes different column formats
- Cleans and transforms raw records
- Converts supported currencies into USD
- Creates additional analytical fields
- Performs automated data-quality validation
- Separates valid and invalid transactions
- Generates a data-quality report
- Writes processed transaction data to CSV
- Loads validated records into MySQL
- Tracks pipeline execution
- Provides SQL analytics queries
- Includes automated tests using `pytest`

---

# 🎯 Problem Statement

Raw financial transaction data can originate from different systems, including:

- Bank transaction systems
- Credit/debit card systems
- Currency exchange-rate sources

Each source may have a different structure and may contain inconsistent or invalid information.

For example, a transaction could contain:

- Missing amount
- Duplicate transaction ID
- Unsupported currency such as `ZZZ`
- Invalid category
- Invalid status
- Out-of-range amount
- Unexpected date
- Missing fields
- Potential anomalies

Loading such records directly into a database can result in unreliable data and inaccurate downstream analysis.

### 💡 Solution

This project introduces an automated ETL pipeline that validates transaction data before loading it into the main database.

```text
Raw Transaction Data
        │
        ▼
     Extract
        │
        ▼
 Transform & Clean
        │
        ▼
 Data Quality Validation
        │
        ├───────────────┐
        ▼               ▼
     Valid           Invalid
    Records           Records
        │               │
        ▼               ▼
   Processed CSV    DQ Report
        │
        ▼
      MySQL
        │
        ▼
  SQL Analytics
```

---

# 🏗️ Pipeline Architecture

```text
 ┌─────────────────────┐
 │  Bank Transactions  │
 │        CSV          │
 └──────────┬──────────┘
            │
            │
 ┌──────────▼──────────┐
 │  Card Transactions  │
 │        CSV          │
 └──────────┬──────────┘
            │
            │
 ┌──────────▼──────────┐
 │   Exchange Rates    │
 │        JSON         │
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
     │  DATA QUALITY│
     │  VALIDATION  │
     └──────┬───────┘
            │
       ┌────┴────┐
       │         │
       ▼         ▼
    Valid     Invalid
   Records     Records
       │         │
       ▼         ▼
Processed CSV  DQ Report
       │
       ▼
     MySQL
       │
       ▼
 SQL Analytics
```

---

# 🔄 Complete Working Process

## 1. Data Generation & Extraction

The project works with **synthetic transaction data** representing different financial systems.

### Input Sources

```text
data/raw/
├── transactions_bank.csv
├── transactions_card.csv
└── exchange_rates.json
```

The pipeline extracts:

- Bank transactions
- Card transactions
- Currency exchange rates

The exchange-rate data is used to convert supported transaction currencies into USD.

---

## 2. Data Standardization

Since transaction data comes from multiple sources, the pipeline first creates a consistent structure.

The transformation process includes:

- Standardizing column names
- Standardizing transaction IDs
- Standardizing account IDs
- Normalizing currency codes
- Converting transaction dates into the required date format
- Converting transaction amounts into numeric values
- Normalizing transaction categories
- Normalizing transaction status values
- Handling missing values
- Removing duplicate transaction IDs

The goal is to ensure that transactions from different sources follow the same structure before validation and loading.

---

## 3. Data Transformation & Enrichment

After the raw records are cleaned and standardized, the pipeline creates additional fields that are useful for analysis.

### Important Derived Fields

| Field               | Purpose                                          |
| ------------------- | ------------------------------------------------ |
| `amount_usd`        | Converts supported currencies into USD           |
| `is_international`  | Identifies international transactions            |
| `transaction_month` | Supports monthly transaction analysis            |
| `day_of_week`       | Supports weekday/weekend analysis                |
| `transaction_type`  | Identifies transaction type such as debit/credit |

### Currency Conversion Example

```text
Original Amount
      │
      ▼
  8500 INR
      │
      ▼
Exchange Rate
   INR → USD
      │
      ▼
  amount_usd
```

The resulting `amount_usd` field allows transactions from supported currencies to be analyzed using a common currency.

---

# 🔍 Data Quality Validation

Data validation is one of the main components of this project.

Before records are loaded into MySQL, the pipeline checks whether they satisfy predefined data-quality rules.

### Validation Checks

1. **Null value validation**
2. **Duplicate transaction ID validation**
3. **Schema validation**
4. **Transaction amount range validation**
5. **Anomaly / outlier validation**
6. **Transaction date range validation**
7. **Category validation**
8. **Status validation**
9. **Supported currency validation**

The supported-currency check is particularly important because currency conversion requires a valid exchange rate.

---

# 🚦 Valid & Invalid Record Handling

The pipeline does not stop simply because invalid data is detected.

Instead, it separates the records into **valid** and **invalid** groups.

```text
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
      Processed CSV     DQ Report
             │
             ▼
           MySQL
```

### Current Synthetic Dataset Result

```text
Rows processed : 30
Valid rows     : 27
Invalid rows   : 3
Rows loaded    : 27
```

The current synthetic dataset contains invalid examples such as:

- Unsupported currency (`ZZZ`)
- Missing transaction amount
- Invalid transaction category

Invalid records are excluded from the main transaction load, ensuring that the primary transaction table contains only validated records.

---

# 📋 Data Quality Report

The pipeline generates a data-quality report at:

```text
data/reports/data_quality_report.json
```

The report provides an audit-friendly summary of the validation results.

### Example

```json
{
  "rows_processed": 30,
  "valid_rows": 27,
  "invalid_rows": 3,
  "quality_passed": false
}
```

### Understanding `quality_passed`

```text
quality_passed: false
```

means that one or more data-quality issues were detected in the input data.

It **does not mean that the pipeline execution failed**.

The pipeline can successfully complete while detecting, reporting, and excluding invalid records.

---

# 📁 Pipeline Outputs

The pipeline produces several important outputs.

## 1. Processed Transaction Dataset

```text
data/processed/transactions.csv
```

This file contains the cleaned, standardized, validated, and enriched transaction records.

### Important Columns

```text
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
```

---

## 2. Data Quality Report

```text
data/reports/data_quality_report.json
```

Contains information such as:

- Total rows processed
- Valid row count
- Invalid row count
- Validation results
- Invalid transaction IDs
- Quality status
- Pipeline execution information

---

## 3. Pipeline Log

```text
logs/pipeline.log
```

The pipeline log records execution details such as:

- Data extraction
- Data transformation
- Data validation
- Valid/invalid record counts
- Database loading
- Pipeline execution status

---

# 🗄️ MySQL Database

Validated transaction records can be loaded into the MySQL database:

```text
financial_pipeline
```

The database contains three main tables:

```text
financial_pipeline
│
├── transactions
├── pipeline_runs
└── transaction_anomalies
```

### `transactions`

Stores the final validated transaction records used for analysis.

### `pipeline_runs`

Tracks individual pipeline executions, including:

- Start time
- Completion time
- Rows processed
- Rows loaded
- Quality status
- Pipeline status
- Error information

### `transaction_anomalies`

Stores detected transaction anomalies and their associated details.

---

# 📊 SQL Analytics

SQL analytics queries are available in:

```text
sql/analytics.sql
```

The processed transaction data can be used to answer business questions such as:

- How does spending change month by month?
- Which categories have the highest spending?
- Which merchants receive the most transactions?
- How much spending is international versus domestic?
- Which accounts have higher transaction volumes?
- How does debit spending compare with credit spending?
- What is the distribution of transaction statuses?
- Which days of the week have higher spending?
- Which currencies are present in the dataset?
- What is the rolling 3-month spending average?

This demonstrates the complete flow from:

```text
Data Engineering
       ↓
   Clean Data
       ↓
     MySQL
       ↓
  SQL Analytics
       ↓
Business Insights
```

---

# 🧪 Testing

The project uses **pytest** for automated testing.

Tests cover areas such as:

- Data extraction
- Data transformation
- Data validation
- Duplicate handling
- Missing values
- Invalid records
- Currency validation
- Edge cases
- Pipeline behavior

### Current Test Result

```text
22 passed
```

Automated tests help ensure that changes to the pipeline do not break existing functionality.

---

# 🛠️ Technology Stack

| Technology                 | Purpose                                 |
| -------------------------- | --------------------------------------- |
| **Python**                 | ETL pipeline development                |
| **Pandas**                 | Data cleaning and transformation        |
| **NumPy**                  | Data processing                         |
| **Faker**                  | Synthetic transaction generation        |
| **JSON**                   | Exchange-rate input and quality reports |
| **MySQL 8+**               | Transaction database                    |
| **SQL**                    | Financial data analysis                 |
| **pytest**                 | Automated testing                       |
| **mysql-connector-python** | Python/MySQL database connection        |
| **python-dotenv**          | Environment configuration               |
| **Git & GitHub**           | Version control and project hosting     |

---

# 📂 Project Structure

```text
Financial-Data-Pipeline/
│
├── config/
│   └── settings.py
│
├── data/
│   ├── raw/
│   │   ├── transactions_bank.csv
│   │   ├── transactions_card.csv
│   │   └── exchange_rates.json
│   │
│   ├── processed/
│   │   └── transactions.csv
│   │
│   └── reports/
│       └── data_quality_report.json
│
├── docs/
│
├── logs/
│   └── pipeline.log
│
├── scripts/
│   └── run_pipeline.py
│
├── sql/
│   ├── schema.sql
│   └── analytics.sql
│
├── src/
│   ├── extract.py
│   ├── generator.py
│   ├── loader.py
│   ├── logging_utils.py
│   ├── pipeline.py
│   ├── quality.py
│   └── transform.py
│
├── tests/
│
├── .env.example
├── PROJECT_SPEC.md
├── requirements.txt
└── README.md
```

---

# 🚀 Setup

## Requirements

Before running the project, install:

- **Python 3.11+**
- **MySQL 8+**
- **Git**
- **VS Code** or another Python IDE

---

## 1. Clone the Repository

```bash
git clone https://github.com/adithyatamilselvan/Financial-Data-Pipeline.git
cd Financial-Data-Pipeline
```

---

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Environment on Windows

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

# ▶️ Running the Pipeline

## Dry Run

The dry-run mode processes the data without loading records into MySQL.

```bash
python scripts/run_pipeline.py --dry-run
```

The dry run produces:

```text
Processed transaction CSV
Data quality report
Pipeline logs
```

It does **not** perform the database load.

---

# 🗄️ Running the Full Pipeline

Configure the MySQL credentials through the environment configuration.

Create the required database and tables using:

```text
sql/schema.sql
```

Then run:

```bash
python scripts/run_pipeline.py
```

The complete pipeline performs the following steps:

```text
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
```

---

# 📈 Example Pipeline Result

A successful execution using the current synthetic dataset produces:

```text
Rows processed : 30
Valid rows     : 27
Invalid rows   : 3
Rows loaded    : 27
Quality passed : False
```

### Result Interpretation

The pipeline successfully processes the dataset and loads the **27 valid records** into the database.

The **3 invalid records** are identified by the data-quality validation process and excluded from the main transaction load.

Therefore:

```text
30 Total Records
       │
       ├── 27 Valid → Processed → MySQL
       │
       └──  3 Invalid → Data Quality Report
```

---

# 🎯 Key Project Highlights

- End-to-end **ETL pipeline**
- Multiple input sources
- CSV and JSON data ingestion
- Data cleaning and standardization
- Currency conversion to USD
- Data enrichment
- Automated data-quality validation
- Valid/invalid record separation
- Data-quality reporting
- MySQL database integration
- Pipeline execution tracking
- Transaction anomaly tracking
- SQL-based analytics
- Automated testing with pytest
- Synthetic financial data generation
- Local and reproducible project setup

---

# 💼 Skills Demonstrated

This project demonstrates practical experience with:

**Python • Pandas • NumPy • SQL • MySQL • ETL • Data Cleaning • Data Validation • Data Quality • Data Transformation • Database Loading • Automated Testing • Git • GitHub**

It also demonstrates the ability to build a data workflow that moves from **raw data ingestion to validated, analytics-ready data**.
