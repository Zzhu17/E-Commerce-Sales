-- fact_orders (order grain) - Postgres
CREATE TABLE IF NOT EXISTS fact_orders (
    order_id VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50),
    customer_unique_id VARCHAR(50),
    order_status VARCHAR(32),
    order_purchase_ts TIMESTAMP,
    order_purchase_date DATE,
    order_delivered_ts TIMESTAMP,
    order_estimated_ts TIMESTAMP,
    customer_city VARCHAR(64),
    customer_state VARCHAR(8),
    payment_value_total NUMERIC(12,2),
    orders_cnt SMALLINT,
    items_cnt INT,
    revenue_order NUMERIC(12,2),
    delivered_days INT,
    estimated_gap_days INT,
    on_time_flag SMALLINT,
    is_canceled SMALLINT NOT NULL DEFAULT 0,
    is_new_customer SMALLINT,
    PRIMARY KEY (order_id),
    CONSTRAINT chk_on_time_flag CHECK (on_time_flag IN (0, 1) OR on_time_flag IS NULL),
    CONSTRAINT chk_is_canceled CHECK (is_canceled IN (0, 1)),
    CONSTRAINT chk_is_new_customer CHECK (is_new_customer IN (0, 1) OR is_new_customer IS NULL)
);

CREATE INDEX IF NOT EXISTS idx_fact_orders_customer_id
    ON fact_orders (customer_id);
CREATE INDEX IF NOT EXISTS idx_fact_orders_customer_unique_id
    ON fact_orders (customer_unique_id);
CREATE INDEX IF NOT EXISTS idx_fact_orders_purchase_ts
    ON fact_orders (order_purchase_ts);
