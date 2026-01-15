# Data Quality Report (Step 1: Data Audit + Grain Lock)

## Data Audit Summary

### Table Coverage & Grain
- orders: 1 row per `order_id` = yes (0 duplicate `order_id`)
- order_items: 1 row per (`order_id`, `order_item_id`) = yes (0 duplicate PKs)
- payments: multiple rows per `order_id` = yes (mean 1.04, max 29) -> must aggregate
- customers: `customer_unique_id` represents unique shopper = yes (96,096 unique vs 99,441 `customer_id`)

### Missing & Anomalies
- `order_delivered_customer_date` missing in ~2.98% orders (likely canceled/unavailable)
- no negative prices/payments; high-end outliers exist (price max 6,735; payment max 13,664)

### Join Considerations
- payments join rule: aggregate payments to `order_id` before joining to items/orders
- fact_orders grain: `order_id`

### Initial Metric Decisions
- Revenue (Order): SUM(`payment_value_total`) = locked
- Item-level GMV proxy: `price + freight_value` = locked

## 1) Raw File Inventory

Expected files (drop into `data/raw/`):

- olist_orders_dataset.csv
- olist_order_items_dataset.csv
- olist_order_payments_dataset.csv
- olist_customers_dataset.csv
- olist_products_dataset.csv
- product_category_name_translation.csv

Optional:

- olist_order_reviews_dataset.csv
- olist_sellers_dataset.csv
- olist_geolocation_dataset.csv

Status: all expected files present; optional files present.

## 2) Grain Confirmation

- orders: 1 row = 1 `order_id`
- order_items: 1 row = 1 (`order_id`, `order_item_id`)
- payments: 1 row = 1 payment record (aggregate to `order_id` before join)
- customers: 1 row = 1 `customer_id` (note: `customer_unique_id` is the person)
- products: 1 row = 1 `product_id`

## 3) Data Quality Checks

Fill in after audit:

### 3.1 Primary Key Uniqueness

- orders: % duplicate `order_id` = 0 (0.00%)
- order_items: % duplicate (`order_id`, `order_item_id`) = 0 (0.00%)
- customers: % duplicate `customer_id` = 0 (0.00%)
- products: % duplicate `product_id` = 0 (0.00%)

### 3.2 Missing Critical Timestamps

- `order_purchase_timestamp` missing % = 0 (0.00%)
- `order_delivered_customer_date` missing % = 2.98%
- `order_estimated_delivery_date` missing % = 0 (0.00%)

### 3.3 Status Distribution

- order_status counts:
  - delivered: 96,478 (97.02%)
  - shipped: 1,107 (1.11%)
  - canceled: 625 (0.63%)
  - unavailable: 609 (0.61%)
  - invoiced: 314 (0.32%)
  - processing: 301 (0.30%)
  - created: 5 (0.01%)
  - approved: 2 (0.00%)

### 3.4 Join Coverage

- orders ↔ order_items: % of orders with >=1 item = 99.22%
- order_items ↔ products: % of items with product match = 100.00%
- orders ↔ payments: % of orders with >=1 payment row = 99.999% (1 order missing payment row)

### 3.5 Price/Payment Ranges

- order_items.price min/max/p99 = 0.85 / 6,735.00 / 890.00
- order_items.freight_value min/max/p99 = 0.00 / 409.68 / 84.52
- payments.payment_value min/max/p99 = 0.00 / 13,664.08 / 1,039.92

### 3.6 Time Logic

- delivered before purchase (% of orders) = 0 (0.00%)
- delivered after estimated (% of orders) = 7.87%

## 4) Metric Definitions (Locked Early)

- Revenue (orders): sum of aggregated payments per `order_id`
- GMV proxy (items): sum of `price + freight_value`

## 5) Notes / Decisions

- Canceled + unavailable orders are ~1.24%; decide later whether to exclude from KPI.

## Step 3 Join Coverage Notes (fact_order_items)

- items -> orders: 0 missing (all items match orders)
- items -> products: 0 missing (all items match products)
- products -> category translation: 623 missing (1.89%), likely blank category_name
- items -> category translation: 1,627 missing (1.45%)

## SQL Checks Summary

- dim_date: 0 duplicate dates; range 2016-09-04 to 2018-10-17 (774 days)
- fact_orders: 0 duplicate order_id; payment_null_rate ~0.00001; avg payment 160.99
- fact_order_items: 0 duplicate (order_id, order_item_id); no negative/null GMV; 623 products missing translation
