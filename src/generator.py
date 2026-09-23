import json
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


CATEGORIES = ["Groceries", "Dining", "Transport",
              "Utilities", "Shopping", "Travel"]


def generate_sources(raw_dir: Path, seed: int = 42) -> dict[str, Path]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    start = date(2025, 1, 1)
    for index in range(1, 31):
        currency = ["USD", "EUR", "GBP", "CAD"][index % 4]
        rows.append({
            "transaction_id": f"TX-{index:04d}",
            "account_id": f"ACC-{(index % 5) + 1:03d}",
            "transaction_date": (start + timedelta(days=index * 4)).isoformat(),
            "amount": round(18.25 + index * 11.73, 2),
            "currency": currency,
            "merchant": ["North Market", "Metro Rail", "Cloud Utilities", "Harbor Cafe"][index % 4],
            "category": CATEGORIES[index % len(CATEGORIES)],
            "status": ["completed", "COMPLETED", "settled", "pending"][index % 4],
            "source": "bank",
        })
    bank = pd.DataFrame(rows[:18]).rename(
        columns={"transaction_id": "bank_txn_id", "account_id": "account_number"})
    card = pd.DataFrame(rows[18:]).rename(columns={
        "transaction_id": "card_txn_id", "account_id": "card_account", "transaction_date": "posted_date", "merchant": "merchant_name"})
    card["card_account"] = card["card_account"].str.replace(
        "ACC-", "", regex=False).map(lambda value: f"CARD-{value}")
    card["source"] = "card"

    # Deliberate quality issues: a duplicate, missing category, invalid currency, and malformed amount.
    duplicate = bank.iloc[[3]].copy()
    bank = pd.concat([bank, duplicate], ignore_index=True)
    bank.loc[2, "category"] = None
    bank.loc[5, "currency"] = "ZZZ"
    card["amount"] = card["amount"].astype(object)
    card.loc[2, "amount"] = "not-a-number"
    card.loc[4, "status"] = "reversed"

    bank_file = raw_dir / "transactions_bank.csv"
    card_file = raw_dir / "transactions_card.csv"
    bank.to_csv(bank_file, index=False)
    card.to_csv(card_file, index=False)
    fx_file = raw_dir / "fx_rates.json"
    fx_file.write_text(json.dumps({"base_currency": "USD", "rates": {
                       "USD": 1.0, "EUR": 1.09, "GBP": 1.27, "CAD": 0.74}}, indent=2), encoding="utf-8")
    return {"bank": bank_file, "card": card_file, "fx": fx_file}
