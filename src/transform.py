import pandas as pd


CATEGORY_MAP = {"food": "Dining", "dining": "Dining", "groceries": "Groceries",
                "transport": "Transport", "utilities": "Utilities", "shopping": "Shopping", "travel": "Travel"}
STATUS_MAP = {"completed": "completed", "settled": "completed",
              "pending": "pending", "failed": "failed", "reversed": "reversed"}
REQUIRED_CURRENCIES = {"USD", "EUR", "GBP", "CAD"}


def _standardize_bank(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.rename(columns={"bank_txn_id": "transaction_id", "account_number": "account_id"})


def _standardize_card(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.rename(columns={"card_txn_id": "transaction_id", "card_account": "account_id",
                          "posted_date": "transaction_date", "merchant_name": "merchant"})
    result["account_id"] = result["account_id"].str.replace(
        "CARD-", "ACC-", regex=False)
    return result


def transform(bank: pd.DataFrame, card: pd.DataFrame, fx_data: dict) -> pd.DataFrame:
    combined = pd.concat(
        [_standardize_bank(bank), _standardize_card(card)], ignore_index=True)
    combined["transaction_id"] = combined["transaction_id"].astype(
        "string").str.strip().str.upper()
    combined["account_id"] = combined["account_id"].astype(
        "string").str.strip().str.upper()
    combined["transaction_date"] = pd.to_datetime(
        combined["transaction_date"], errors="coerce")
    combined["amount"] = pd.to_numeric(combined["amount"], errors="coerce")
    combined["currency"] = combined["currency"].astype(
        "string").str.strip().str.upper()
    combined["category"] = combined["category"].astype(
        "string").str.strip().str.lower().map(CATEGORY_MAP).fillna("Uncategorized")
    combined["status"] = combined["status"].astype(
        "string").str.strip().str.lower().map(STATUS_MAP).fillna("unknown")
    combined["merchant"] = combined["merchant"].fillna(
        "Unknown merchant").astype(str).str.strip()
    combined["amount_usd"] = combined["amount"] * \
        combined["currency"].map(fx_data["rates"])
    combined["is_international"] = combined["currency"] != fx_data["base_currency"]
    combined["transaction_month"] = combined["transaction_date"].dt.to_period(
        "M").astype("string")
    combined["day_of_week"] = combined["transaction_date"].dt.day_name()
    combined["transaction_type"] = combined["amount"].apply(
        lambda value: "debit" if pd.notna(value) and value >= 0 else "credit")
    combined = combined.drop_duplicates(
        subset=["transaction_id"], keep="first")
    return combined[["transaction_id", "account_id", "transaction_date", "amount", "currency", "amount_usd", "merchant", "category", "status", "source", "is_international", "transaction_month", "day_of_week", "transaction_type"]]
