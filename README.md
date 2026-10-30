# Olist E-commerce Analytics Pipeline

An end-to-end analytics project on the Olist Brazilian e-commerce dataset (Kaggle): raw CSVs are cleaned with Python, loaded into a SQL database, summarised with SQL, and shown in an interactive Streamlit dashboard.

**Live dashboard:** (https://olist-pipeline-db.streamlit.app)

## Pipeline

CSV files -> pandas cleaning -> SQLite database -> SQL summary tables -> Streamlit dashboard

## Tools
Python (pandas, SQLAlchemy), SQL (SQLite), Plotly, Streamlit, Git/GitHub

## Data quality issues found
- 99,441 orders in total; 97% (96,478) have status "delivered".
- 2,965 orders have no customer delivery date (mostly canceled, unavailable or in-transit orders).
- 160 orders have no approval timestamp; 1,783 have no carrier handover date.
- Decision: analysis is limited to delivered orders with a recorded delivery date, since delivery time and lateness cannot be measured otherwise.
- 610 of 32,951 products have no category; these are labelled "unknown" rather than dropped, so their sales still count.
- Category names are in Portuguese; mapped to English using the provided translation table.
- Source data contains a typo ("lenght") in two column names; these columns are not used.

## Cleaning and modelling
- After filtering, 96,470 orders remain. Average delivery time is 12.1 days (median 10); 8.1% of orders arrived later than the estimated date.
- Delivery times have extreme outliers (max 209 days), so the median is reported alongside the average.
- Joined orders, items, customers, products and reviews into one fact table of 110,189 rows (one row per item sold).
- 827 rows have no review score (customers who did not leave a review); left empty rather than imputed.
- Some orders have multiple reviews; scores were averaged so each order has one score and joins do not create duplicate rows.
- Automated quality checks (no negative prices, no duplicate order items, no negative delivery times) all pass.
- Loaded into SQLite (fact_sales) and summarised in four SQL tables: monthly, category, state and customer.

## Key insights
- Late deliveries cut review scores sharply: 4.21 average for on-time orders vs 2.55 for late orders (-1.66 points). About 8% of orders arrived late.
- Monthly revenue grew from ~127K (Jan 2017) to ~1.15M (Nov 2017), with orders up ~63% in November 2017 vs October (Black Friday). Growth plateaued in 2018.
- Top 5 categories (health_beauty, watches_gifts, bed_bath_table, sports_leisure, computers_accessories) generate 39.3% of revenue.
- Remote states (AP, RR, AM) have the longest delivery times (26-28 days) but low late rates, while Alagoas (AL) has the highest late rate at 24.1%, suggesting delivery estimates there are too optimistic.
- Only 3.0% of customers placed more than one order; the top 10% of customers generate 38.3% of revenue, pointing to retention as the main opportunity.
- Note: these findings show association, not proven cause.

## How to run
1. Download the dataset from Kaggle (Olist Brazilian E-Commerce) and put the CSVs in `data/raw/`.
2. Create a virtual environment and run `pip install -r requirements.txt`.
3. Run in order: `python src/clean.py`, `python src/load.py`, `python src/marts.py`, `python src/make_dashboard_db.py`.
4. Start the dashboard: `streamlit run app.py`
