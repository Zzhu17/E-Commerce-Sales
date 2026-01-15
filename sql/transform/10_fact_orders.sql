-- Build fact_orders from raw tables (Postgres).
-- Assumes raw tables exist:
--   raw_orders, raw_order_items, raw_order_payments, raw_customers

INSERT INTO fact_orders (
    order_id,
    customer_id,
    customer_unique_id,
    order_status,
    order_purchase_ts,
    order_purchase_date,
    order_delivered_ts,
    order_estimated_ts,
    customer_city,
    customer_state,
    payment_value_total,
    orders_cnt,
    items_cnt,
    revenue_order,
    delivered_days,
    estimated_gap_days,
    on_time_flag,
    is_canceled,
    is_new_customer
)
SELECT
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    o.order_status,
    CAST(o.order_purchase_timestamp AS TIMESTAMP) AS order_purchase_ts,
    CAST(o.order_purchase_timestamp AS DATE) AS order_purchase_date,
    CAST(o.order_delivered_customer_date AS TIMESTAMP) AS order_delivered_ts,
    CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS order_estimated_ts,
    c.customer_city,
    c.customer_state,
    p.payment_value_total,
    1 AS orders_cnt,
    COALESCE(i.items_cnt, 0) AS items_cnt,
    p.payment_value_total AS revenue_order,
    CASE
        WHEN o.order_delivered_customer_date IS NULL
          OR o.order_purchase_timestamp IS NULL
        THEN NULL
        ELSE EXTRACT(
            DAY FROM (
                CAST(o.order_delivered_customer_date AS TIMESTAMP)
                - CAST(o.order_purchase_timestamp AS TIMESTAMP)
            )
        )
    END AS delivered_days,
    CASE
        WHEN o.order_delivered_customer_date IS NULL
          OR o.order_estimated_delivery_date IS NULL
        THEN NULL
        ELSE EXTRACT(
            DAY FROM (
                CAST(o.order_delivered_customer_date AS TIMESTAMP)
                - CAST(o.order_estimated_delivery_date AS TIMESTAMP)
            )
        )
    END AS estimated_gap_days,
    CASE
        WHEN o.order_delivered_customer_date IS NULL
          OR o.order_estimated_delivery_date IS NULL
        THEN NULL
        WHEN CAST(o.order_delivered_customer_date AS TIMESTAMP)
          <= CAST(o.order_estimated_delivery_date AS TIMESTAMP)
        THEN 1
        ELSE 0
    END AS on_time_flag,
    CASE WHEN o.order_status = 'canceled' THEN 1 ELSE 0 END AS is_canceled,
    CASE
        WHEN c.customer_unique_id IS NULL THEN NULL
        WHEN CAST(o.order_purchase_timestamp AS TIMESTAMP)
          = MIN(CAST(o.order_purchase_timestamp AS TIMESTAMP))
            OVER (PARTITION BY c.customer_unique_id)
        THEN 1
        ELSE 0
    END AS is_new_customer
FROM raw_orders o
LEFT JOIN raw_customers c
    ON o.customer_id = c.customer_id
LEFT JOIN (
    SELECT order_id, SUM(payment_value) AS payment_value_total
    FROM raw_order_payments
    GROUP BY order_id
) p
    ON o.order_id = p.order_id
LEFT JOIN (
    SELECT order_id, COUNT(*) AS items_cnt
    FROM raw_order_items
    GROUP BY order_id
) i
    ON o.order_id = i.order_id;
