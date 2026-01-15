#!/usr/bin/env python3
"""
Build fact_orders at order grain (notebook-equivalent script).

Usage:
  python notebooks/02_fact_orders.py
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
    payments = pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv")
    customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")

    # Pre-aggregate to order grain to avoid double counting.
    payments_agg = (
        payments.groupby("order_id", as_index=False)["payment_value"]
        .sum()
        .rename(columns={"payment_value": "payment_value_total"})
    )

    items_agg = (
        items.groupby("order_id", as_index=False)
        .agg(items_cnt=("order_item_id", "count"))
    )

    fact_orders = (
        orders.merge(customers, on="customer_id", how="left")
        .merge(payments_agg, on="order_id", how="left")
        .merge(items_agg, on="order_id", how="left")
    )

    fact_orders["order_purchase_ts"] = pd.to_datetime(
        fact_orders["order_purchase_timestamp"]
    )
    fact_orders["order_purchase_date"] = fact_orders["order_purchase_ts"].dt.date
    fact_orders["order_delivered_ts"] = pd.to_datetime(
        fact_orders["order_delivered_customer_date"]
    )
    fact_orders["order_estimated_ts"] = pd.to_datetime(
        fact_orders["order_estimated_delivery_date"]
    )

    fact_orders["delivered_days"] = (
        fact_orders["order_delivered_ts"] - fact_orders["order_purchase_ts"]
    ).dt.days

    fact_orders["estimated_gap_days"] = (
        fact_orders["order_delivered_ts"] - fact_orders["order_estimated_ts"]
    ).dt.days

    mask = fact_orders["order_delivered_ts"].notna() & fact_orders[
        "order_estimated_ts"
    ].notna()
    fact_orders["on_time_flag"] = pd.NA
    fact_orders.loc[mask, "on_time_flag"] = (
        fact_orders.loc[mask, "order_delivered_ts"]
        <= fact_orders.loc[mask, "order_estimated_ts"]
    ).astype(int)
    fact_orders["on_time_flag"] = fact_orders["on_time_flag"].astype("Int64")

    fact_orders["is_canceled"] = (fact_orders["order_status"] == "canceled").astype(
        int
    )
    fact_orders["revenue_order"] = fact_orders["payment_value_total"]
    fact_orders["items_cnt"] = fact_orders["items_cnt"].fillna(0).astype("Int64")
    fact_orders["orders_cnt"] = 1

    first_purchase = fact_orders.groupby("customer_unique_id")[
        "order_purchase_ts"
    ].transform("min")
    is_new_mask = fact_orders["order_purchase_ts"] == first_purchase
    fact_orders["is_new_customer"] = pd.NA
    fact_orders.loc[is_new_mask, "is_new_customer"] = 1
    fact_orders.loc[~is_new_mask, "is_new_customer"] = 0
    fact_orders.loc[fact_orders["customer_unique_id"].isna(), "is_new_customer"] = pd.NA
    fact_orders["is_new_customer"] = fact_orders["is_new_customer"].astype("Int64")

    # Checks
    assert fact_orders["order_id"].is_unique, "order_id is not unique in fact_orders"
    print("Missing rates (payment_value_total, items_cnt):")
    print(fact_orders[["payment_value_total", "items_cnt"]].isna().mean())
    print("\nAOV sanity (payment_value_total describe):")
    print(fact_orders["payment_value_total"].describe())

    # Output
    MART_DIR.mkdir(parents=True, exist_ok=True)
    out_path = MART_DIR / "fact_orders.csv"
    fact_orders.to_csv(out_path, index=False)
    print(f"\nWrote {len(fact_orders)} rows -> {out_path}")


if __name__ == "__main__":
    main()
