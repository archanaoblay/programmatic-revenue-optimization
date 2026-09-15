import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Programmatic Revenue Optimization",
    layout="wide"
)

st.title("🚀 Programmatic Revenue Optimization Engine")

st.write(
    "Interactive analytics dashboard for programmatic advertising performance."
)
# Load advertising data
df = pd.read_csv("data/ad_delivery_data.csv")

st.subheader("📊 Advertising Data")

st.write(f"Total records: {len(df):,}")

st.dataframe(df.head(10), use_container_width=True)
