#!/usr/bin/env python3
"""
Quick data audit for the Olist raw CSVs (Step 1: Data Audit + Grain Lock).

Usage:
  python notebooks/01_data_audit.py
  python notebooks/01_data_audit.py --write-report docs/data_quality_report.md
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Optional

import pandas as pd


RAW_DIR = Path("data/raw")
EXPECTED_FILES = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}


def pct(n: int, d: int) -> float:
    return (n / d * 100.0) if d else 0.0


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def safe_dt(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce", utc=False)


def audit() -> Dict[str, object]:
    missing = [name for name, fn in EXPECTED_FILES.items() if not (RAW_DIR / fn).exists()]
    if missing:
        missing_files = [EXPECTED_FILES[name] for name in missing]
        raise FileNotFoundError(
            "Missing raw files in data/raw/: " + ", ".join(missing_files)
        )

    orders = load_csv(RAW_DIR / EXPECTED_FILES["orders"])
    order_items = load_csv(RAW_DIR / EXPECTED_FILES["order_items"])
    payments = load_csv(RAW_DIR / EXPECTED_FILES["payments"])
    customers = load_csv(RAW_DIR / EXPECTED_FILES["customers"])
    products = load_csv(RAW_DIR / EXPECTED_FILES["products"])

    # PK uniqueness
    dup_orders = orders.duplicated(subset=["order_id"]).sum()
    dup_order_items = order_items.duplicated(subset=["order_id", "order_item_id"]).sum()
    dup_customers = customers.duplicated(subset=["customer_id"]).sum()
    dup_products = products.duplicated(subset=["product_id"]).sum()

    # Missing timestamps
    missing_purchase = orders["order_purchase_timestamp"].isna().sum()
    missing_delivered = orders["order_delivered_customer_date"].isna().sum()
    missing_estimated = orders["order_estimated_delivery_date"].isna().sum()

    # Status distribution
    status_counts = orders["order_status"].value_counts(dropna=False)

    # Join coverage
    orders_with_items = orders["order_id"].isin(order_items["order_id"]).sum()
    items_with_products = order_items["product_id"].isin(products["product_id"]).sum()
    orders_with_payments = orders["order_id"].isin(payments["order_id"]).sum()

    # Price / payment ranges
    price_stats = order_items["price"].describe(percentiles=[0.99])
    freight_stats = order_items["freight_value"].describe(percentiles=[0.99])
    payment_stats = payments["payment_value"].describe(percentiles=[0.99])

    # Time logic checks
    purchase_ts = safe_dt(orders["order_purchase_timestamp"])
    delivered_ts = safe_dt(orders["order_delivered_customer_date"])
    estimated_ts = safe_dt(orders["order_estimated_delivery_date"])

    delivered_before_purchase = (delivered_ts < purchase_ts).sum()
    delivered_after_estimated = (delivered_ts > estimated_ts).sum()

    return {
        "counts": {
            "orders": len(orders),
            "order_items": len(order_items),
            "payments": len(payments),
            "customers": len(customers),
            "products": len(products),
        },
        "pk_dupes": {
            "orders": (dup_orders, pct(dup_orders, len(orders))),
            "order_items": (dup_order_items, pct(dup_order_items, len(order_items))),
            "customers": (dup_customers, pct(dup_customers, len(customers))),
            "products": (dup_products, pct(dup_products, len(products))),
        },
        "missing_ts": {
            "purchase": (missing_purchase, pct(missing_purchase, len(orders))),
            "delivered": (missing_delivered, pct(missing_delivered, len(orders))),
            "estimated": (missing_estimated, pct(missing_estimated, len(orders))),
        },
        "status_counts": status_counts,
        "join_coverage": {
            "orders_with_items": (orders_with_items, pct(orders_with_items, len(orders))),
            "items_with_products": (
                items_with_products,
                pct(items_with_products, len(order_items)),
            ),
            "orders_with_payments": (
                orders_with_payments,
                pct(orders_with_payments, len(orders)),
            ),
        },
        "price_stats": price_stats,
        "freight_stats": freight_stats,
        "payment_stats": payment_stats,
        "time_logic": {
            "delivered_before_purchase": (
                delivered_before_purchase,
                pct(delivered_before_purchase, len(orders)),
            ),
            "delivered_after_estimated": (
                delivered_after_estimated,
                pct(delivered_after_estimated, len(orders)),
            ),
        },
    }


def format_report(result: Dict[str, object]) -> str:
    counts = result["counts"]
    pk_dupes = result["pk_dupes"]
    missing_ts = result["missing_ts"]
    join_coverage = result["join_coverage"]
    time_logic = result["time_logic"]

    def fmt_pair(pair: tuple) -> str:
        return f"{pair[0]} ({pair[1]:.2f}%)"

    status_counts = result["status_counts"].to_string()

    return f"""# Data Quality Report (Step 1: Data Audit + Grain Lock)

## 0) Row Counts

- orders: {counts["orders"]}
- order_items: {counts["order_items"]}
- payments: {counts["payments"]}
- customers: {counts["customers"]}
- products: {counts["products"]}

## 1) Primary Key Uniqueness

- orders: {fmt_pair(pk_dupes["orders"])}
- order_items: {fmt_pair(pk_dupes["order_items"])}
- customers: {fmt_pair(pk_dupes["customers"])}
- products: {fmt_pair(pk_dupes["products"])}

## 2) Missing Critical Timestamps

- order_purchase_timestamp: {fmt_pair(missing_ts["purchase"])}
- order_delivered_customer_date: {fmt_pair(missing_ts["delivered"])}
- order_estimated_delivery_date: {fmt_pair(missing_ts["estimated"])}

## 3) Status Distribution

{status_counts}

## 4) Join Coverage

- orders with >=1 item: {fmt_pair(join_coverage["orders_with_items"])}
- items with product match: {fmt_pair(join_coverage["items_with_products"])}
- orders with >=1 payment row: {fmt_pair(join_coverage["orders_with_payments"])}

## 5) Price / Payment Ranges

price (pandas describe):
{result["price_stats"].to_string()}

freight_value (pandas describe):
{result["freight_stats"].to_string()}

payment_value (pandas describe):
{result["payment_stats"].to_string()}

## 6) Time Logic

- delivered before purchase: {fmt_pair(time_logic["delivered_before_purchase"])}
- delivered after estimated: {fmt_pair(time_logic["delivered_after_estimated"])}
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-report",
        dest="write_report",
        default=None,
        help="Write markdown report to this path",
    )
    args = parser.parse_args()

    result = audit()
    report = format_report(result)

    if args.write_report:
        Path(args.write_report).write_text(report, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()
