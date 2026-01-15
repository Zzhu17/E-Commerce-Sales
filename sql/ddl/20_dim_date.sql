-- dim_date (daily grain) - Postgres
CREATE TABLE IF NOT EXISTS dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    quarter INT,
    month_num INT,
    month_name VARCHAR(16),
    year_month VARCHAR(7),
    week_of_year INT,
    day_of_week INT,
    day_name VARCHAR(16),
    is_weekend SMALLINT,
    is_month_start SMALLINT,
    is_month_end SMALLINT
);
