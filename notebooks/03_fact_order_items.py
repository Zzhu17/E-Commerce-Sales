#!/usr/bin/env python3
"""
Build fact_order_items at item grain (notebook-equivalent script).

Usage:
  python notebooks/03_fact_order_items.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
MART_DIR = ROOT / "data" / "mart"


def main() -> None:
    orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
    items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")
    customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")
    products = pd.read_csv(RAW_DIR / "olist_products_dataset.csv")
    category_translation = pd.read_csv(
        RAW_DIR / "product_category_name_translation.csv"
    )

    fact_order_items = (
        items.merge(
            orders[
                [
                    "order_id",
                    "customer_id",
                    "order_status",
                    "order_purchase_timestamp",
                ]
            ],
            on="order_id",
            how="left",
        )
        .merge(customers, on="customer_id", how="left")
        .merge(products, on="product_id", how="left")
        .merge(category_translation, on="product_category_name", how="left")
    )

    fact_order_items["order_purchase_ts"] = pd.to_datetime(
        fact_order_items["order_purchase_timestamp"]
    )
    fact_order_items["order_date"] = fact_order_items["order_purchase_ts"].dt.date
    fact_order_items["item_price"] = fact_order_items["price"]
    fact_order_items["item_gmv"] = (
        fact_order_items["item_price"] + fact_order_items["freight_value"]
    )
    fact_order_items["item_cnt"] = 1

    # Checks
    dupes = fact_order_items.duplicated(["order_id", "order_item_id"]).sum()
    assert dupes == 0
    assert (fact_order_items["item_gmv"] >= 0).all()

    print("Item GMV describe:")
    print(fact_order_items["item_gmv"].describe())

    missing_orders = fact_order_items["customer_id"].isna().sum()
    missing_products = fact_order_items["product_id"].isna().sum()
    missing_translation = fact_order_items["product_category_name_english"].isna().sum()
    print("\nJoin coverage (missing rows):")
    print(
        {
            "items_without_orders": missing_orders,
            "items_without_products": missing_products,
            "items_without_translation": missing_translation,
            "total_items": len(fact_order_items),
        }
    )

    # Output
    MART_DIR.mkdir(parents=True, exist_ok=True)
    out_path = MART_DIR / "fact_order_items.csv"
    fact_order_items = fact_order_items.rename(
        columns={"product_category_name_english": "product_category_en"}
    )
    fact_order_items.to_csv(out_path, index=False)
    print(f"\nWrote {len(fact_order_items)} rows -> {out_path}")


if __name__ == "__main__":
    main()
