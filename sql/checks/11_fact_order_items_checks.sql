-- fact_order_items validation checks (Postgres)

-- 1) Grain check (should return 0)
SELECT COUNT(*) AS duplicate_item_rows
FROM (
    SELECT order_id, order_item_id, COUNT(*) AS cnt
    FROM fact_order_items
    GROUP BY order_id, order_item_id
    HAVING COUNT(*) > 1
) d;

-- 1b) Count vs distinct key (should be 0)
SELECT
    COUNT(*) - COUNT(DISTINCT (order_id, order_item_id)) AS diff_count
FROM fact_order_items;

-- 2) Negative or null GMV check
SELECT
    SUM(CASE WHEN item_gmv < 0 THEN 1 ELSE 0 END) AS negative_gmv_rows,
    SUM(CASE WHEN item_gmv IS NULL THEN 1 ELSE 0 END) AS null_gmv_rows
FROM fact_order_items;

-- 3) GMV sanity (distribution)
SELECT
    MIN(item_gmv) AS min_item_gmv,
    MAX(item_gmv) AS max_item_gmv,
    AVG(item_gmv) AS avg_item_gmv
FROM fact_order_items;

-- 4) Join coverage (raw tables)
SELECT
    SUM(CASE WHEN o.order_id IS NULL THEN 1 ELSE 0 END) AS items_without_orders,
    SUM(CASE WHEN p.product_id IS NULL THEN 1 ELSE 0 END) AS items_without_products,
    COUNT(*) AS total_items
FROM raw_order_items oi
LEFT JOIN raw_orders o ON oi.order_id = o.order_id
LEFT JOIN raw_products p ON oi.product_id = p.product_id;

SELECT
    SUM(CASE WHEN ct.product_category_name_english IS NULL THEN 1 ELSE 0 END) AS products_without_translation,
    COUNT(*) AS total_products
FROM raw_products p
LEFT JOIN raw_category_translation ct
    ON p.product_category_name = ct.product_category_name;
