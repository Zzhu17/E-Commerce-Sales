-- Build fact_order_items from raw tables (Postgres).
-- Assumes raw tables exist:
--   raw_orders, raw_order_items, raw_customers, raw_products, raw_category_translation

INSERT INTO fact_order_items (
    order_id,
    order_item_id,
    product_id,
    seller_id,
    customer_id,
    customer_unique_id,
    order_purchase_ts,
    order_date,
    order_status,
    customer_city,
    customer_state,
    product_category_name,
    product_category_en,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm,
    item_price,
    freight_value,
    item_gmv,
    item_cnt
)
SELECT
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    o.customer_id,
    c.customer_unique_id,
    CAST(o.order_purchase_timestamp AS TIMESTAMP) AS order_purchase_ts,
    CAST(o.order_purchase_timestamp AS DATE) AS order_date,
    o.order_status,
    c.customer_city,
    c.customer_state,
    p.product_category_name,
    ct.product_category_name_english AS product_category_en,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm,
    oi.price AS item_price,
    oi.freight_value,
    (oi.price + oi.freight_value) AS item_gmv,
    1 AS item_cnt
FROM raw_order_items oi
LEFT JOIN raw_orders o
    ON oi.order_id = o.order_id
LEFT JOIN raw_customers c
    ON o.customer_id = c.customer_id
LEFT JOIN raw_products p
    ON oi.product_id = p.product_id
LEFT JOIN raw_category_translation ct
    ON p.product_category_name = ct.product_category_name;
