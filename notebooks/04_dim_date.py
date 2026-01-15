#!/usr/bin/env python3
"""
Build dim_date (notebook-equivalent script).

Usage:
  python notebooks/04_dim_date.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
MART_DIR = ROOT / "data" / "mart"


def main() -> None:
    orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
    purchase_ts = pd.to_datetime(orders["order_purchase_timestamp"])
    start_date = purchase_ts.min().normalize()
    end_date = purchase_ts.max().normalize()

    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    dim_date = pd.DataFrame({"date_id": dates})

    dim_date["year"] = dim_date["date_id"].dt.year
    dim_date["quarter"] = dim_date["date_id"].dt.quarter
    dim_date["month_num"] = dim_date["date_id"].dt.month
    dim_date["month_name"] = dim_date["date_id"].dt.strftime("%B")
    dim_date["year_month"] = dim_date["date_id"].dt.strftime("%Y-%m")
    dim_date["week_of_year"] = dim_date["date_id"].dt.isocalendar().week.astype(int)
    dim_date["day_of_week"] = dim_date["date_id"].dt.isocalendar().day.astype(int)
    dim_date["day_name"] = dim_date["date_id"].dt.strftime("%A")
    dim_date["is_weekend"] = dim_date["day_of_week"].isin([6, 7]).astype(int)
    dim_date["is_month_start"] = dim_date["date_id"].dt.is_month_start.astype(int)
    dim_date["is_month_end"] = dim_date["date_id"].dt.is_month_end.astype(int)

    MART_DIR.mkdir(parents=True, exist_ok=True)
    out_path = MART_DIR / "dim_date.csv"
    dim_date.to_csv(out_path, index=False)
    print(f"Wrote {len(dim_date)} rows -> {out_path}")


if __name__ == "__main__":
    main()
