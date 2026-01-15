# Tableau Data Source Notes

## Data Source A: Order-Level

Tables:
- fact_orders
- dim_date (join on `order_purchase_date = date_id`)

Grain:
- One row per `order_id`

KPI fields:
- `revenue_order`, `orders_cnt`, `is_canceled`, `on_time_flag`, `delivered_days`, `is_new_customer`

Do not:
- Join item-level tables into this data source.

## Data Source B: Item-Level

Tables:
- fact_order_items
- dim_date (join on `order_date = date_id`)

Grain:
- One row per (`order_id`, `order_item_id`)

Contribution fields:
- `item_gmv`, `item_cnt`, `product_category_name`, `product_category_en`

Do not:
- Compute AOV or order-level KPIs here.
