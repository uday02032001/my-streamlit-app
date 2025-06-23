import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Sales Dashboard")

url = "https://drive.google.com/file/d/1Pe-2bCluotRrwVlpsoRNHS_-bfYme5ZF/view?usp=sharing"
sales = pd.read_csv(url)


# Set page config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Title
st.title("📊 Sales Data Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

# Date range filter
min_date = pd.to_datetime(sales['Order_Date']).min().date()
max_date = pd.to_datetime(sales['Order_Date']).max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# City filter
cities = st.sidebar.multiselect(
    "Select Cities",
    options=sales['City'].unique(),
    default=sales['City'].unique()
)

# Product filter
products = st.sidebar.multiselect(
    "Select Products",
    options=sales['Product'].unique(),
    default=sales['Product'].unique()
)

# Apply filters
filtered_sales = sales[
    (sales['City'].isin(cities)) &
    (sales['Product'].isin(products))
]

if len(date_range) == 2:
    filtered_sales = filtered_sales[
        (pd.to_datetime(filtered_sales['Order_Date']).dt.date >= date_range[0]) &
        (pd.to_datetime(filtered_sales['Order_Date']).dt.date <= date_range[1])
]

# Metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Sales", f"${filtered_sales['Sales'].sum():,.2f}")
with col2:
    st.metric("Total Orders", filtered_sales['Order_ID'].nunique())
with col3:
    avg_order = filtered_sales['Sales'].mean() if len(filtered_sales) > 0 else 0
    st.metric("Avg Order Value", f"${avg_order:,.2f}")
with col4:
    top_product = filtered_sales['Product'].value_counts().idxmax() if len(filtered_sales) > 0 else "N/A"
    st.metric("Top Product", top_product)

# Charts - first row
col1, col2 = st.columns(2)

with col1:
    # Sales trend
    daily_sales = filtered_sales.groupby(pd.to_datetime(filtered_sales['Order_Date']).dt.date)['Sales'].sum().reset_index()
    fig = px.line(daily_sales, x='Order_Date', y='Sales', title='Daily Sales Trend')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Product performance
    product_sales = filtered_sales.groupby('Product')['Sales'].sum().reset_index()
    fig = px.bar(product_sales, x='Product', y='Sales', title='Product Performance')
    st.plotly_chart(fig, use_container_width=True)

# Charts - second row
col1, col2 = st.columns(2)

with col1:
    # City performance
    city_sales = filtered_sales.groupby('City')['Sales'].sum().reset_index()
    fig = px.pie(city_sales, names='City', values='Sales', title='Sales by City')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Hourly sales
    hourly_sales = filtered_sales.groupby('Hour')['Sales'].sum().reset_index()
    fig = px.bar(hourly_sales, x='Hour', y='Sales', title='Hourly Sales Pattern')
    st.plotly_chart(fig, use_container_width=True)

# Show filtered data (optional)
if st.checkbox("Show Filtered Data"):
    st.dataframe(filtered_sales)
