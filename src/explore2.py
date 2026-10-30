import pandas as pd

products = pd.read_csv("data/raw/olist_products_dataset.csv")
trans = pd.read_csv("data/raw/product_category_name_translation.csv")

print("Products shape:", products.shape)
print()
print("Missing values:")
print(products.isna().sum())
print()
print("Top 5 categories (Portuguese):")
print(products.product_category_name.value_counts().head())
print()
print("Translation table shape:", trans.shape)
print(trans.head())