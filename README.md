# E-Commerce-Sales

## Status

- Data engineering + KPI-ready layer complete (~90%)
- Tableau dashboard build in progress (screenshots will be added by me)

## Project Goal

Build an end-to-end ecommerce analytics project with clean grains, KPI-ready facts, and Tableau-ready data sources.

## Data Model

- `fact_orders` (order grain)
- `fact_order_items` (item grain)
- `dim_date` (daily grain)

## Tableau Data Sources

- Data Source A (Order-level): `fact_orders` + `dim_date`
  - Join: `fact_orders.order_purchase_date = dim_date.date_id`
- Data Source B (Item-level): `fact_order_items` + `dim_date`
  - Join: `fact_order_items.order_date = dim_date.date_id`

Rules:
- Order KPIs only from `fact_orders`.
- Product contribution only from `fact_order_items`.

## Outputs (CSV)

- `data/mart/fact_orders.csv`
- `data/mart/fact_order_items.csv`
- `data/mart/dim_date.csv`

## Postgres (Materialized)

Tables:
- `fact_orders`, `fact_order_items`, `dim_date`, plus `raw_*`

## How to Reproduce (Python)

- Build order fact: `python src/transform.py`
- Build item fact: `python src/transform_items.py`
- Build date dim: `python src/build_dim_date.py`

## SQL (Postgres)

- DDL: `sql/ddl/*.sql`
- Transforms: `sql/transform/*.sql`
- Checks: `sql/checks/*.sql`

## Docs

- Data quality: `docs/data_quality_report.md`
- SQL checks: `docs/sql_checks_report.md`
- Metrics dictionary: `docs/metrics_dictionary.md`
- Dashboard walkthrough: `docs/dashboard_walkthrough.md`
- Tableau notes: `tableau/data_source_notes.md`

## Insights

- Revenue is highly concentrated in a small number of states, with São Paulo (SP), Rio de Janeiro (RJ), and Minas Gerais (MG) contributing the majority of total revenue, indicating strong regional dependency. Average Order Value (AOV) remains stable at approximately 155, and the on-time delivery rate exceeds 92%, suggesting mature pricing and fulfillment operations. The cancellation rate is low at 0.65%, but given the large order volume, it still represents non-trivial revenue loss. Monthly revenue trends show clear volatility and seasonality rather than consistent growth, highlighting periods of demand fluctuation across the year.

## Opportunity Sizing

- Given the stable AOV, revenue growth is primarily driven by order volume expansion rather than price increases. A modest increase in order count or targeted growth in mid-performing states could generate meaningful incremental revenue. Additionally, small reductions in cancellation rates would recover lost revenue at scale, while improved seasonal planning and demand smoothing could mitigate revenue dips during low-demand months and improve overall revenue stability without significant operational changes.

## Dashboard

- `tableau/olist_dashboard.twbx`
- Screenshots will be added
