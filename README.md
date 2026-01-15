# E-Commerce-Sales

## Project Goal

Build an end-to-end ecommerce analytics project with clean grains, KPI-ready facts, and Tableau-ready data sources.

## Data Model

- fact_orders (order grain)
- fact_order_items (item grain)
- dim_date (daily grain)

## Tableau Data Sources

- Data Source A (Order-level): `fact_orders` + `dim_date`
- Data Source B (Item-level): `fact_order_items` + `dim_date`

Notes:
- Order KPIs only from fact_orders.
- Product contribution only from fact_order_items.

## Outputs

- `data/mart/fact_orders.csv`
- `data/mart/fact_order_items.csv`
- `data/mart/dim_date.csv`

## Docs

- Data quality: `docs/data_quality_report.md`
- SQL checks: `docs/sql_checks_report.md`
- Metrics dictionary: `docs/metrics_dictionary.md`
- Dashboard walkthrough: `docs/dashboard_walkthrough.md`
- Tableau notes: `tableau/data_source_notes.md`

## Insights (TODO)

- __

## Opportunity Sizing (TODO)

- __

## Dashboard (TODO)

- `tableau/olist_dashboard.twbx`
- Add screenshots under `docs/`
