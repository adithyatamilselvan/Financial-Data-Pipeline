# Data Dictionary

The processed transaction file contains one row per unique `transaction_id`.

| Field             | Meaning                                                  |
| ----------------- | -------------------------------------------------------- |
| transaction_id    | Stable synthetic source transaction key                  |
| account_id        | Standardized account identifier                          |
| transaction_date  | Parsed transaction date                                  |
| amount            | Original transaction amount                              |
| currency          | ISO-like source currency code                            |
| amount_usd        | Amount converted using the synthetic FX snapshot         |
| merchant          | Normalized merchant name                                 |
| category          | Canonical spending category                              |
| status            | Canonical transaction status                             |
| source            | `bank` or `card`                                         |
| is_international  | Whether currency differs from USD                        |
| transaction_month | YYYY-MM reporting period                                 |
| day_of_week       | Calendar day name                                        |
| transaction_type  | Debit for non-negative synthetic spend, credit otherwise |
