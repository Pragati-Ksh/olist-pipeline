import pandas as pd

orders = pd.read_csv("data/raw/olist_orders_dataset.csv")

print("Rows and columns:", orders.shape)
print()
print("First 5 rows:")
print(orders.head())
print()
print("Missing values per column:")
print(orders.isna().sum())
print()
print("Order status counts:")
print(orders.order_status.value_counts())