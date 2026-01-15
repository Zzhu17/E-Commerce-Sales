-- fact_order_items (item grain) - Postgres
CREATE TABLE IF NOT EXISTS fact_order_items (
    order_id VARCHAR(50) NOT NULL,
    order_item_id INT NOT NULL,
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    customer_id VARCHAR(50),
    customer_unique_id VARCHAR(50),
    order_purchase_ts TIMESTAMP,
    order_date DATE,
    order_status VARCHAR(32),
    customer_city VARCHAR(64),
    customer_state VARCHAR(8),
    product_category_name VARCHAR(128),
    product_category_en VARCHAR(128),
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT,
    item_price NUMERIC(12,2),
    freight_value NUMERIC(12,2),
    item_gmv NUMERIC(12,2),
    item_cnt SMALLINT,
    PRIMARY KEY (order_id, order_item_id)
);

CREATE INDEX IF NOT EXISTS idx_fact_order_items_product_id
    ON fact_order_items (product_id);
CREATE INDEX IF NOT EXISTS idx_fact_order_items_seller_id
    ON fact_order_items (seller_id);
CREATE INDEX IF NOT EXISTS idx_fact_order_items_category_en
    ON fact_order_items (product_category_en);
CREATE INDEX IF NOT EXISTS idx_fact_order_items_purchase_ts
    ON fact_order_items (order_purchase_ts);
