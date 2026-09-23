from pathlib import Path

import pandas as pd

SCHEMA_SQL = Path(__file__).resolve().parents[1] / "sql" / "schema.sql"


def load_to_mysql(frame: pd.DataFrame, settings, quality_passed: bool = True) -> int:
    try:
        import mysql.connector
    except ImportError as error:
        raise RuntimeError(
            "mysql-connector-python is required for MySQL loads") from error
    connection = mysql.connector.connect(host=settings.mysql_host, port=settings.mysql_port,
                                         user=settings.mysql_user, password=settings.mysql_password, database=settings.mysql_database)
    cursor = connection.cursor()
    columns = ["transaction_id", "account_id", "transaction_date", "amount", "currency", "amount_usd", "merchant",
               "category", "status", "source", "is_international", "transaction_month", "day_of_week", "transaction_type"]
    query = "INSERT INTO transactions (" + ",".join(columns) + ") VALUES (" + ",".join(
        ["%s"] * len(columns)) + ") ON DUPLICATE KEY UPDATE transaction_id=VALUES(transaction_id)"
    values = []
    for row in frame[columns].itertuples(index=False, name=None):
        values.append(tuple(None if pd.isna(value) else value.to_pydatetime() if hasattr(
            value, "to_pydatetime") else value.item() if hasattr(value, "item") else value for value in row))
    cursor.executemany(query, values)
    cursor.execute(
        "INSERT INTO pipeline_runs (started_at, completed_at, rows_processed, rows_loaded, quality_passed, status) "
        "VALUES (UTC_TIMESTAMP(), UTC_TIMESTAMP(), %s, %s, %s, %s)",
        (len(frame), len(values), quality_passed, "completed"),
    )
    connection.commit()
    cursor.close()
    connection.close()
    return len(values)
