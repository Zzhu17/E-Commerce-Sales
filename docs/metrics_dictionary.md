# Metrics Dictionary

## Order-Level (fact_orders)

### Revenue (Order)
- **Definition**: Sum of `payment_value_total` at order grain.
- **Source**: `olist_order_payments_dataset.csv` aggregated by `order_id`.
- **Notes**: Payments must be aggregated before any join to avoid duplication.

### Orders
- **Definition**: Count of distinct `order_id`.
- **Notes**: Include all statuses unless explicitly filtered.

### Orders Count (Row-Level)
- **Definition**: `orders_cnt = 1` per row for fast aggregation.
- **Usage**: Use `SUM(orders_cnt)` as Orders.

### New Customer Flag
- **Definition**: `is_new_customer = 1` when `order_purchase_ts` is the first order for `customer_unique_id`.
- **Notes**: NULL when `customer_unique_id` is missing.

### AOV (Average Order Value)
- **Definition**: `Revenue (Order)` / `Orders`.
- **Recommended Filter**: Exclude canceled/unavailable if reporting fulfilled revenue.

### Cancel Rate
- **Definition**: Sum of `is_canceled` / `Orders`.
- **Source**: `order_status == "canceled"`.

### On-Time Rate
- **Definition**: Average of `on_time_flag` among delivered orders.
- **Notes**: Only valid when `order_delivered_ts` and `order_estimated_ts` are present.

### Delivery Time (Days)
- **Definition**: `delivered_days` = `order_delivered_ts` - `order_purchase_ts`.
- **Notes**: Missing for non-delivered orders.

### Estimated Delivery Gap (Days)
- **Definition**: `estimated_gap_days` = `order_delivered_ts` - `order_estimated_ts`.
- **Interpretation**: Positive means late, negative means early.

## Item-Level (fact_order_items)

### Item GMV (Proxy)
- **Definition**: `item_gmv` = `item_price + freight_value`.
- **Usage**: Product/category contribution analysis, Pareto (80/20), Top-N.
- **Notes**: Not used for order-level KPIs (AOV/Orders/Revenue).

### Item Count (Row-Level)
- **Definition**: `item_cnt = 1` per item row.
- **Usage**: Use `SUM(item_cnt)` for item counts at any slice.

## Date Dimension (dim_date)

### Date Grain
- **Definition**: 1 row per calendar date.
- **Source Range**: From min to max `order_purchase_ts`.

### Date Fields
- **year**: Calendar year.
- **quarter**: 1-4.
- **month_num**: 1-12 (sorting).
- **month_name**: Full month name.
- **year_month**: `YYYY-MM`.
- **week_of_year**: ISO week number.
- **day_of_week**: 1 (Mon) - 7 (Sun).
- **day_name**: Weekday name.
- **is_weekend**: Saturday/Sunday.
- **is_month_start** / **is_month_end**: Month boundary flags.
