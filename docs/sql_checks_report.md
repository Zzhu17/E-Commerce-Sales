# SQL Checks Report

## dim_date (sql/checks/20_dim_date_checks.sql)

- duplicate_dates: 0
- date range: 2016-09-04 to 2018-10-17
- total_days: 774

## fact_orders (sql/checks/10_fact_orders_checks.sql)

- duplicate_order_id_rows: 0
- count vs distinct diff: 0
- payment_null_rate: 0.0000100562
- items_cnt_null_rate: 0.0000000000
- min_payment: 0.00
- max_payment: 13664.08
- avg_payment: 160.9902667

## fact_order_items (sql/checks/11_fact_order_items_checks.sql)

- duplicate_item_rows: 0
- count vs distinct diff: 0
- negative_gmv_rows: 0
- null_gmv_rows: 0
- min_item_gmv: 6.08
- max_item_gmv: 6929.31
- avg_item_gmv: 140.6440589
- items_without_orders: 0
- items_without_products: 0
- total_items: 112650
- products_without_translation: 623
- total_products: 32951
