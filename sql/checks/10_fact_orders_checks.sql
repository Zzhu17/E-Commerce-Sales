-- fact_orders validation checks (Postgres)

-- 1) Grain check (should return 0)
SELECT COUNT(*) AS duplicate_order_id_rows
FROM (
    SELECT order_id, COUNT(*) AS cnt
    FROM fact_orders
    GROUP BY order_id
    HAVING COUNT(*) > 1
) d;

-- 1b) Count vs distinct key (should be 0)
SELECT
    COUNT(*) - COUNT(DISTINCT order_id) AS diff_count
FROM fact_orders;

-- 2) Missing payment / items rates
SELECT
    AVG(CASE WHEN payment_value_total IS NULL THEN 1 ELSE 0 END) AS payment_null_rate,
    AVG(CASE WHEN items_cnt IS NULL THEN 1 ELSE 0 END) AS items_cnt_null_rate
FROM fact_orders;

-- 3) AOV sanity (distribution)
SELECT
    MIN(payment_value_total) AS min_payment,
    MAX(payment_value_total) AS max_payment,
    AVG(payment_value_total) AS avg_payment
FROM fact_orders;
