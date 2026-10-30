# Music Recommendation System

## Overview
This project recommends songs based on user preferences.

## Technologies Used
- Python
- Pandas
- Scikit-learn

## How to Run
1. Install dependencies.
2. Run app.py.

- 610 of 32,951 products have no category; these are labelled "unknown" rather than dropped, so their sales still count.
- Category names are in Portuguese; mapped to English using the provided translation table.
- Source data contains a typo ("lenght") in two column names; these columns are not used.

- After filtering, 96,470 orders remain. Average delivery time is 12.1 days (median 10); 8.1% of orders arrived later than the estimated date.
- Delivery times have extreme outliers (max 209 days), so median is reported alongside the average.

- Joined orders, items, customers, products and reviews into one fact table of 110,189 rows (one row per item sold).
- 827 rows have no review score (customers who did not leave a review); left empty rather than imputed.
- Some orders have multiple reviews; scores were averaged so each order has one score and joins do not create duplicate rows.

- Automated quality checks (no negative prices, no duplicate order items, no negative delivery times) all pass.
- Final cleaned table: 110,189 rows x 13 columns, saved for loading into the database.

- Cleaned table loaded into a SQLite database (fact_sales, 110,189 rows) using SQLAlchemy.

## Key insights (so far)
- Monthly revenue grew from ~127K (Jan 2017) to ~1.15M (Nov 2017), with orders jumping ~63% in November 2017 versus October (Black Friday).
- Growth plateaued in 2018, with revenue holding at roughly 1.0-1.1M per month.

## Key insights
- Late deliveries cut review scores sharply: 4.21 average for on-time orders vs 2.55 for late orders (-1.66 points). About 8% of orders arrived late.
- Top 5 categories (health_beauty, watches_gifts, bed_bath_table, sports_leisure, computers_accessories) generate 39.3% of revenue.
- Remote states (AP, RR, AM) have the longest delivery times (26-28 days) but low late rates, while Alagoas (AL) has the highest late rate at 24.1%, suggesting delivery estimates there are too optimistic.
- Only 3.0% of customers placed more than one order; the top 10% of customers generate 38.3% of revenue, pointing to retention as the main growth opportunity.