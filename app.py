import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/dashboard.db")
q = lambda t: pd.read_sql(f"SELECT * FROM {t}", engine)

st.set_page_config(page_title="Olist Dashboard", layout="wide")
st.title("Olist E-commerce Dashboard")

monthly = q("mart_monthly").sort_values("order_month")
cat = q("mart_category")
state = q("mart_state")

c1, c2, c3 = st.columns(3)
c1.metric("Total revenue", f"{monthly.revenue.sum():,.0f}")
c2.metric("Orders", f"{monthly.orders.sum():,}")
c3.metric("Avg % late (across states)", f"{state.pct_late.mean():.1f}%")

st.plotly_chart(px.line(monthly, x="order_month", y="revenue", title="Monthly revenue"),
                width="stretch")


left, right = st.columns(2)

bar = px.bar(cat.nlargest(10, "revenue"), x="revenue", y="category",
             orientation="h", title="Top 10 categories by revenue")
bar.update_layout(yaxis={"categoryorder": "total ascending"})
left.plotly_chart(bar, width="stretch")

scatter = px.scatter(state, x="pct_late", y="avg_review", text="customer_state",
                     title="Late deliveries vs review score, by state")
scatter.update_traces(textposition="top center", marker=dict(size=8))
right.plotly_chart(scatter, width="stretch")