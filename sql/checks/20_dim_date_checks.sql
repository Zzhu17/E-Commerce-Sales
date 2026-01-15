-- dim_date validation checks (Postgres)

-- 1) Unique date_id (should return 0)
SELECT COUNT(*) AS duplicate_dates
FROM (
    SELECT date_id, COUNT(*) AS cnt
    FROM dim_date
    GROUP BY date_id
    HAVING COUNT(*) > 1
) d;

-- 2) Range sanity
SELECT
    MIN(date_id) AS min_date,
    MAX(date_id) AS max_date,
    COUNT(*) AS total_days
FROM dim_date;
