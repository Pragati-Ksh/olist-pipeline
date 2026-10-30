import pandas as pd
from sqlalchemy import create_engine

# Read the cleaned table saved by clean.py
fact = pd.read_pickle("data/fact.pkl")

# Create (or open) a database file and write the table into it
engine = create_engine("sqlite:///data/olist.db")
fact.to_sql("fact_sales", engine, if_exists="replace", index=False)

print("Loaded", len(fact), "rows into table fact_sales")