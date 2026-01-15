# Dashboard Walkthrough (Step 5)

## Data Sources (Tableau)

### Data Source A: Order-Level

Tables:
- fact_orders
- dim_date (join on `order_purchase_date = date_id`)

Use for:
- Revenue, Orders, AOV
- Cancel rate, on-time rate, delivery days
- New vs returning (via `is_new_customer`)

Rule:
- Never join item grain into this data source.

### Data Source B: Item-Level

Tables:
- fact_order_items
- dim_date (join on `order_date = date_id`)

Use for:
- Category / product contribution (GMV proxy)
- Pareto (80/20) and product portfolio

Rule:
- Never compute order KPIs from item grain.

## Global Interactions

### A) Date Range
- Use `dim_date.date_id` as the global filter (relative/slider).

### B) KPI Parameter (KPI Select)
Parameter values:
- Revenue
- Orders
- AOV
- Cancel Rate
- On-time Rate

Recommended calculated fields:
- `KPI Value`:
  - CASE [KPI Select]
    - "Revenue": SUM([revenue_order])
    - "Orders": SUM([orders_cnt])
    - "AOV": SUM([revenue_order]) / SUM([orders_cnt])
    - "Cancel Rate": SUM([is_canceled]) / SUM([orders_cnt])
    - "On-time Rate": AVG([on_time_flag])
  - END

### C) Drill-down / Highlight
- Action: click state or category to filter linked charts.
- Tooltip: show brief "why/so what" guidance (1-2 sentences).

## Page 1: Executive Overview

Question:
- Is the business healthy? What changed recently?

Primary visuals:
- KPI cards: Revenue, Orders, AOV, Cancel Rate, On-time Rate
- Monthly revenue trend with YoY comparison
- State revenue map or bar
- Top 5 categories (contribution via item_gmv, Data Source B)

Advanced:
- Anomaly alert: highlight when Cancel Rate rises above threshold.

Decision output:
- Call out top risk (cancel/late delivery spike) and best growth driver.

## Page 2: Drivers & Decomposition

Question:
- Is revenue change driven by Orders or AOV?

Primary visuals:
- Waterfall: current vs prior period revenue (Orders x AOV decomposition)
- Dual-axis: Orders vs AOV trend
- Contribution bar: Top/Bottom states or categories

Advanced:
- Parameter to switch dimension (State / Category / Seller).
- Show both share and absolute delta.

Decision output:
- Identify top driver and dragger and recommended actions.

## Page 3: Customer Segmentation (RFM)

Question:
- Who drives revenue and who is at risk?

Primary visuals:
- Segment size and revenue share
- Segment KPI table (Revenue, AOV, Orders per customer, Avg Recency)
- New vs returning trend

Advanced:
- Action: click segment to show top categories or states below.
- Opportunity sizing: "Recall 5% of At Risk" estimate in tooltip.

Decision output:
- Which segments to retain vs reactivate.

## Page 4: Fulfillment & Funnel

Question:
- Where do we lose orders and why?

Primary visuals:
- Fulfillment funnel: Purchase -> Approved -> Shipped -> Delivered (canceled/unavailable drop)
- Delivery days distribution
- On-time rate by state/category
- Cancel rate by delay bucket (0-3, 4-7, 8-14, 14+ days)

Advanced:
- Delay bucket parameter with colored thresholds.

Decision output:
- Logistics focus areas and expected impact on cancel rate.

## Page 5: Product Portfolio

Question:
- Which categories/products to invest in or fix?

Primary visuals:
- Pareto curve (cumulative item_gmv)
- Growth vs size matrix (revenue share vs YoY growth)
- Top/Bottom products with category drilldown

Advanced:
- Price band breakdown and tooltip strategy guidance.

Decision output:
- Invest/Maintain/Fix/Exit recommendations by category.
