import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/olist.db")
q = lambda sql: pd.read_sql(sql, engine)

print("=== 1. Top 5 categories by revenue ===")
cat = q("SELECT * FROM mart_category ORDER BY revenue DESC LIMIT 5")
print(cat)
total = q("SELECT SUM(revenue) AS t FROM mart_category").t[0]
print("Share of total revenue from these 5:", round(cat.revenue.sum() / total * 100, 1), "%")

print()
print("=== 2. Review score: late vs on-time orders ===")
late = q("""
SELECT CASE WHEN is_late = 1 THEN 'Late' ELSE 'On time' END AS delivery,
       ROUND(AVG(review_score), 2) AS avg_review,
       COUNT(DISTINCT order_id) AS orders
FROM fact_sales
GROUP BY is_late
""")
print(late)

print()
print("=== 3. Slowest 5 states for delivery ===")
print(q("SELECT * FROM mart_state ORDER BY avg_delivery_days DESC LIMIT 5"))

print()
print("=== 4. Customer value ===")
cust = q("SELECT * FROM mart_customers ORDER BY total_spent DESC")
top10 = cust.head(int(len(cust) * 0.1)).total_spent.sum()
print("Unique customers:", len(cust))
print("Top 10% of customers' share of revenue:", round(top10 / cust.total_spent.sum() * 100, 1), "%")
print("Customers with more than 1 order:", round((cust.orders > 1).mean() * 100, 1), "%")