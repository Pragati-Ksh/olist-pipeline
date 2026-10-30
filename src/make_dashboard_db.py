import pandas as pd
from sqlalchemy import create_engine

src = create_engine("sqlite:///data/olist.db")
dst = create_engine("sqlite:///data/dashboard.db")

for t in ["mart_monthly", "mart_category", "mart_state", "mart_customers"]:
    pd.read_sql(f"SELECT * FROM {t}", src).to_sql(t, dst, if_exists="replace", index=False)

print("dashboard.db created")