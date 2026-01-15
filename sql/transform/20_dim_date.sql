-- Build dim_date using generate_series (Postgres).
-- Range based on min/max order_purchase_timestamp in raw_orders.

INSERT INTO dim_date (
    date_id,
    year,
    quarter,
    month_num,
    month_name,
    year_month,
    week_of_year,
    day_of_week,
    day_name,
    is_weekend,
    is_month_start,
    is_month_end
)
SELECT
    d::date AS date_id,
    EXTRACT(YEAR FROM d)::int AS year,
    EXTRACT(QUARTER FROM d)::int AS quarter,
    EXTRACT(MONTH FROM d)::int AS month_num,
    TO_CHAR(d, 'FMMonth')::varchar(16) AS month_name,
    TO_CHAR(d, 'YYYY-MM') AS year_month,
    EXTRACT(WEEK FROM d)::int AS week_of_year,
    EXTRACT(ISODOW FROM d)::int AS day_of_week,
    TO_CHAR(d, 'FMDay')::varchar(16) AS day_name,
    CASE WHEN EXTRACT(ISODOW FROM d) IN (6, 7) THEN 1 ELSE 0 END AS is_weekend,
    CASE WHEN d = DATE_TRUNC('month', d)::date THEN 1 ELSE 0 END AS is_month_start,
    CASE WHEN d = (DATE_TRUNC('month', d) + INTERVAL '1 month - 1 day')::date THEN 1 ELSE 0 END AS is_month_end
FROM generate_series(
    (SELECT MIN(CAST(order_purchase_timestamp AS DATE)) FROM raw_orders),
    (SELECT MAX(CAST(order_purchase_timestamp AS DATE)) FROM raw_orders),
    INTERVAL '1 day'
) AS d;
