#!/usr/bin/env python3
"""
Build fact_order_items at item grain from raw Olist CSVs.

Usage:
  python src/transform_items.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


RAW_DIR = Path("data/raw")
MART_DIR = Path("data/mart")


def load_raw() -> dict:
    return {
        "orders": pd.read_csv(RAW_DIR / "olist_orders_dataset.csv"),
        "items": pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv"),
        "customers": pd.read_csv(RAW_DIR / "olist_customers_dataset.csv"),
        "products": pd.read_csv(RAW_DIR / "olist_products_dataset.csv"),
        "category_translation": pd.read_csv(
            RAW_DIR / "product_category_name_translation.csv"
        ),
    }


def build_fact_order_items(raw: dict) -> pd.DataFrame:
    orders = raw["orders"]
    items = raw["items"]
    customers = raw["customers"]
    products = raw["products"]
    category_translation = raw["category_translation"]

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

    cols = [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "customer_id",
        "customer_unique_id",
        "order_purchase_ts",
        "order_date",
        "order_status",
        "customer_city",
        "customer_state",
        "product_category_name",
        "product_category_name_english",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
        "item_price",
        "freight_value",
        "item_gmv",
        "item_cnt",
    ]

    fact_order_items = fact_order_items[cols].rename(
        columns={"product_category_name_english": "product_category_en"}
    )

    return fact_order_items


def run_checks(fact_order_items: pd.DataFrame) -> None:
    dupes = fact_order_items.duplicated(["order_id", "order_item_id"]).sum()
    assert dupes == 0, "Duplicate (order_id, order_item_id) found"

    if (fact_order_items["item_gmv"] < 0).any():
        raise ValueError("Negative item_gmv values detected")

    print("Item GMV describe:")
    print(fact_order_items["item_gmv"].describe())

    missing_orders = fact_order_items["customer_id"].isna().sum()
    missing_products = fact_order_items["product_id"].isna().sum()
    missing_translation = fact_order_items["product_category_en"].isna().sum()
    total = len(fact_order_items)
    print("\nJoin coverage (missing rows):")
    print(
        {
            "items_without_orders": missing_orders,
            "items_without_products": missing_products,
            "items_without_translation": missing_translation,
            "total_items": total,
        }
    )


def main() -> None:
    MART_DIR.mkdir(parents=True, exist_ok=True)
    raw = load_raw()
    fact_order_items = build_fact_order_items(raw)
    run_checks(fact_order_items)

    out_path = MART_DIR / "fact_order_items.csv"
    fact_order_items.to_csv(out_path, index=False)
    print(f"\nWrote {len(fact_order_items)} rows -> {out_path}")


if __name__ == "__main__":
    main()
