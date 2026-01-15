#!/usr/bin/env python3
"""
Load Olist raw CSVs into Postgres raw_* tables using SQLAlchemy.

Example:
  PG_PASSWORD=your_password python src/load_postgres.py
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Dict

import pandas as pd
from sqlalchemy import create_engine


RAW_DIR = Path("data/raw")

TABLE_FILES: Dict[str, str] = {
    "raw_orders": "olist_orders_dataset.csv",
    "raw_order_items": "olist_order_items_dataset.csv",
    "raw_order_payments": "olist_order_payments_dataset.csv",
    "raw_customers": "olist_customers_dataset.csv",
    "raw_products": "olist_products_dataset.csv",
    "raw_category_translation": "product_category_name_translation.csv",
    "raw_sellers": "olist_sellers_dataset.csv",
    "raw_geolocation": "olist_geolocation_dataset.csv",
    "raw_reviews": "olist_order_reviews_dataset.csv",
}


def build_engine(user: str, password: str, host: str, port: int, database: str):
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    return create_engine(url, future=True)


def load_table(engine, table_name: str, file_path: Path, if_exists: str) -> None:
    df = pd.read_csv(file_path, low_memory=False)
    df.to_sql(
        table_name,
        con=engine,
        if_exists=if_exists,
        index=False,
        method="multi",
        chunksize=10_000,
    )
    print(f"Loaded {len(df)} rows -> {table_name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=5432)
    parser.add_argument("--user", default="postgres")
    parser.add_argument("--db", default="olist_analytics")
    parser.add_argument(
        "--if-exists",
        default="replace",
        choices=["replace", "append", "fail"],
        help="Behavior if table exists (default: replace)",
    )
    args = parser.parse_args()

    password = os.getenv("PG_PASSWORD")
    if not password:
        raise SystemExit("PG_PASSWORD env var is required.")

    engine = build_engine(args.user, password, args.host, args.port, args.db)

    with engine.connect() as conn:
        conn.exec_driver_sql("SELECT 1")

    for table_name, filename in TABLE_FILES.items():
        file_path = RAW_DIR / filename
        if not file_path.exists():
            print(f"Skip missing file: {file_path}")
            continue
        load_table(engine, table_name, file_path, args.if_exists)


if __name__ == "__main__":
    main()
