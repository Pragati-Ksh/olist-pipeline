import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/olist.db")

query = """
SELECT order_month,
       ROUND(SUM(revenue), 2) AS revenue,
       COUNT(DISTINCT order_id) AS orders
FROM fact_sales
GROUP BY order_month
ORDER BY order_month
"""

result = pd.read_sql(query, engine)
print(result)