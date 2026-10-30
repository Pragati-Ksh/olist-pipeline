DROP TABLE IF EXISTS mart_monthly;
CREATE TABLE mart_monthly AS
SELECT order_month,
       ROUND(SUM(revenue), 2) AS revenue,
       COUNT(DISTINCT order_id) AS orders
FROM fact_sales
GROUP BY order_month;

DROP TABLE IF EXISTS mart_category;
CREATE TABLE mart_category AS
SELECT category,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(AVG(review_score), 2) AS avg_review
FROM fact_sales
GROUP BY category;

DROP TABLE IF EXISTS mart_state;
CREATE TABLE mart_state AS
SELECT customer_state,
       ROUND(AVG(delivery_days), 1) AS avg_delivery_days,
       ROUND(100.0 * AVG(is_late), 1) AS pct_late,
       ROUND(AVG(review_score), 2) AS avg_review
FROM fact_sales
GROUP BY customer_state;

DROP TABLE IF EXISTS mart_customers;
CREATE TABLE mart_customers AS
SELECT customer_unique_id,
       COUNT(DISTINCT order_id) AS orders,
       ROUND(SUM(revenue), 2) AS total_spent
FROM fact_sales
GROUP BY customer_unique_id;