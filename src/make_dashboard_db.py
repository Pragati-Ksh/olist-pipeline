import pandas as pd
from sqlalchemy import create_engine

src = create_engine("sqlite:///data/olist.db")
dst = create_engine("sqlite:///data/dashboard.db")

for t in ["mart_monthly", "mart_category", "mart_state", "mart_customers"]:
    pd.read_sql(f"SELECT * FROM {t}", src).to_sql(t, dst, if_exists="replace", index=False)


print("dashboard.db created")
overall = pd.read_sql("""
    SELECT ROUND(100.0 * SUM(is_late) / COUNT(*), 1) AS pct_late
    FROM (SELECT order_id, MAX(is_late) AS is_late FROM fact_sales GROUP BY order_id)
""", src)
overall.to_sql("mart_overall", dst, if_exists="replace", index=False)