# Financial Transaction Data Pipeline

## 1. Project Objective

Build a portfolio-quality financial transaction data pipeline using Python and SQL.

The project simulates a small fintech company's process for collecting transaction data from multiple sources, cleaning and transforming the data, validating data quality, loading analytics-ready data into MySQL, and running SQL analytics.

The project must be simple enough for an AI coding agent to implement, run, test, debug, and verify with minimal human intervention.

Use synthetic data only. Do not use real financial or banking data.

---

## 2. Core Technologies

Use these technologies:

- Python 3.11+
- pandas
- MySQL 8+
- pytest

Supporting libraries may be used when genuinely necessary, such as:

- mysql-connector-python
- python-dotenv
- Faker
- numpy

Do NOT add unnecessary technologies.

Do NOT use:

- React
- Node.js
- Java
- Spark
- Kafka
- Airflow
- Kubernetes
- Redis
- Docker
- AWS or other cloud infrastructure
- multiple databases
- payment gateways
- real banking APIs
- Metabase
- Tableau
- Grafana
- microservices

The project should remain a single manageable Python application with MySQL as the only database.

---

## 3. Business Scenario

A fictional fintech company receives financial transaction data from two systems:

1. A bank system that exports transaction data as CSV.
2. A card-processing system that exports transaction data as CSV.

The two sources may have:

- different column names
- different account ID formats
- different currency codes
- duplicate transactions
- missing values
- invalid values
- inconsistent categories
- inconsistent status values

The finance team needs clean and standardized transaction data for reporting and analysis.

The pipeline should automate this process.

---

## 4. Overall Pipeline

The application should follow this flow:

Data Sources
↓
Extract
↓
Transform
↓
Validate
↓
Load
↓
MySQL
↓
SQL Analytics

The implementation should keep these stages logically separated.

---

# 5. Data Sources

Create synthetic data locally.

The project must contain:

### Bank transaction CSV

```text
data/raw/transactions_bank.csv
```
