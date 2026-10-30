import pandas as pd

# Load the tables we need
orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
items = pd.read_csv("data/raw/olist_order_items_dataset.csv")
customers = pd.read_csv("data/raw/olist_customers_dataset.csv")
products = pd.read_csv("data/raw/olist_products_dataset.csv")
trans = pd.read_csv("data/raw/product_category_name_translation.csv")
reviews = pd.read_csv("data/raw/olist_order_reviews_dataset.csv")

# Clean the orders table
date_cols = ["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]
for c in date_cols:
    orders[c] = pd.to_datetime(orders[c])

print("Orders before filtering:", len(orders))
orders = orders[orders.order_status == "delivered"]
orders = orders.dropna(subset=["order_delivered_customer_date"])
print("Orders after filtering:", len(orders))

orders["delivery_days"] = (orders.order_delivered_customer_date - orders.order_purchase_timestamp).dt.days
orders["is_late"] = (orders.order_delivered_customer_date > orders.order_estimated_delivery_date).astype(int)

print(orders[["delivery_days", "is_late"]].describe())
# Products: add English category names
products = products.merge(trans, on="product_category_name", how="left")
products["category"] = products["product_category_name_english"].fillna("unknown")

# Reviews: one score per order (some orders have more than one review)
reviews = reviews.groupby("order_id", as_index=False)["review_score"].mean()

# Join everything into one table
fact = items.merge(orders, on="order_id")
fact = fact.merge(customers[["customer_id", "customer_unique_id", "customer_state"]], on="customer_id")
fact = fact.merge(products[["product_id", "category"]], on="product_id", how="left")
fact = fact.merge(reviews, on="order_id", how="left")

# New columns
fact["revenue"] = fact["price"] + fact["freight_value"]
fact["order_month"] = fact["order_purchase_timestamp"].dt.to_period("M").astype(str)

print()
print("Joined table shape:", fact.shape)
print(fact[["order_id", "customer_state", "category", "revenue", "delivery_days", "review_score"]].head())
print("Missing review scores:", fact["review_score"].isna().sum())

# Data quality checks (the script stops with an error if any check fails)
assert (fact["price"] >= 0).all(), "Negative prices found"
assert fact.duplicated(["order_id", "order_item_id"]).sum() == 0, "Duplicate rows found"
assert fact["delivery_days"].min() >= 0, "Negative delivery days found"
print()
print("All quality checks passed")

# Keep only the columns we need
fact = fact[[
    "order_id", "order_item_id", "customer_unique_id", "customer_state", "category",
    "price", "freight_value", "revenue", "order_month", "order_purchase_timestamp",
    "delivery_days", "is_late", "review_score"
]]

# Save the cleaned table
fact.to_pickle("data/fact.pkl")
print("Saved cleaned table with", fact.shape[0], "rows and", fact.shape[1], "columns")