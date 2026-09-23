import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Page setup
st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    layout="wide"
)


# Title
st.title("Supermarket Sales Dashboard")
st.write("A simple dashboard to understand sales performance.")


# Load dataset
data = pd.read_csv("supermarket.csv")


# Remove extra spaces from column names
data.columns = data.columns.str.strip()


# Convert Order Date to date format
data["Order Date"] = pd.to_datetime(
    data["Order Date"],
    errors="coerce"
)


# Convert Sales to numeric
data["Sales"] = pd.to_numeric(
    data["Sales"],
    errors="coerce"
)


# Remove rows with missing important values
data = data.dropna(
    subset=[
        "Order ID",
        "Order Date",
        "Customer Name",
        "Category",
        "Region",
        "Sales"
    ]
)



# KEY BUSINESS METRICS


total_sales = data["Sales"].sum()

total_orders = data["Order ID"].nunique()

total_customers = data["Customer ID"].nunique()

average_order = data.groupby("Order ID")["Sales"].sum().mean()


st.subheader("Key Business Metrics")


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Sales",
    f"${total_sales:,.2f}"
)


col2.metric(
    "Total Orders",
    f"{total_orders:,}"
)


col3.metric(
    "Total Customers",
    f"{total_customers:,}"
)


col4.metric(
    "Average Order Value",
    f"${average_order:,.2f}"
)


st.divider()



# SALES TREND


st.subheader("Sales Trend Over Time")


monthly_sales = (
    data.groupby(
        data["Order Date"].dt.to_period("M")
    )["Sales"]
    .sum()
)


monthly_sales.index = monthly_sales.index.astype(str)


fig1, ax1 = plt.subplots(figsize=(10, 5))


monthly_sales.plot(
    ax=ax1,
    marker="o"
)


ax1.set_title("Monthly Sales Trend")
ax1.set_xlabel("Month")
ax1.set_ylabel("Sales")


plt.xticks(rotation=45)

st.pyplot(fig1)


st.divider()



# SALES BY REGION


st.subheader("Sales by Region")


region_sales = (
    data.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)


fig2, ax2 = plt.subplots(figsize=(8, 5))


region_sales.plot(
    kind="bar",
    ax=ax2
)


ax2.set_title("Sales by Region")
ax2.set_xlabel("Region")
ax2.set_ylabel("Sales")


plt.xticks(rotation=0)

st.pyplot(fig2)



# SALES BY CATEGORY


st.subheader("Sales by Category")


category_sales = (
    data.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)


fig3, ax3 = plt.subplots(figsize=(8, 5))


category_sales.plot(
    kind="bar",
    ax=ax3
)


ax3.set_title("Sales by Product Category")
ax3.set_xlabel("Category")
ax3.set_ylabel("Sales")


plt.xticks(rotation=0)

st.pyplot(fig3)



# TOP CUSTOMERS


st.subheader("Top 10 Customers")


customer_sales = (
    data.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)


fig4, ax4 = plt.subplots(figsize=(10, 5))


customer_sales.sort_values().plot(
    kind="barh",
    ax=ax4
)


ax4.set_title("Top 10 Customers by Sales")
ax4.set_xlabel("Sales")
ax4.set_ylabel("Customer")


st.pyplot(fig4)



# KEY FINDINGS


st.divider()

st.subheader("Key Findings")


top_region = region_sales.index[0]

top_region_sales = region_sales.iloc[0]


top_category = category_sales.index[0]

top_category_sales = category_sales.iloc[0]


top_customer = customer_sales.index[0]

top_customer_sales = customer_sales.iloc[0]


highest_sales_month = monthly_sales.idxmax()

highest_month_sales = monthly_sales.max()


st.write(
    f"""
    The supermarket generated total sales of ${total_sales:,.2f}
    from {total_orders:,} orders.

    The average order value was ${average_order:,.2f},
    and the dataset contains {total_customers:,} unique customers.

    The region with the highest sales was {top_region},
    with total sales of ${top_region_sales:,.2f}.

    The best performing product category was {top_category},
    with sales of ${top_category_sales:,.2f}.

    The customer with the highest total sales was
    {top_customer}, with sales of ${top_customer_sales:,.2f}.

    The highest monthly sales were recorded in
    {highest_sales_month}, with sales of ${highest_month_sales:,.2f}.
    """
)



# DATA PREVIEW


with st.expander("View Dataset"):

    st.write("Number of rows:", len(data))

    st.write("Number of columns:", len(data.columns))

    st.dataframe(data.head(20))