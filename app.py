import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

@st.cache_data
def load_data():
    sales = pd.read_csv("data/cleaned_sales.csv", parse_dates=["Date"])
    forecast = pd.read_csv("data/forecast.csv", parse_dates=["Date"])
    results = pd.read_csv("data/model_results.csv")
    stores = pd.read_csv("data/store_clusters.csv")
    return sales, forecast, results, stores

sales, forecast, results, stores = load_data()

st.title("Retail Analytics & AI-Powered Sales Forecasting")

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")
min_d, max_d = sales["Date"].min().date(), sales["Date"].max().date()
date_range = st.sidebar.date_input("Date range", (min_d, max_d), min_value=min_d, max_value=max_d)
all_stores = sorted(sales["Store_ID"].unique())
all_cats = sorted(sales["Product_Category"].unique())
store_sel = st.sidebar.multiselect("Store", all_stores, default=all_stores)
cat_sel = st.sidebar.multiselect("Category", all_cats, default=all_cats)

if len(date_range) == 2:
    start, end = date_range
else:
    start, end = min_d, max_d

filtered = sales[
    (sales["Date"] >= pd.Timestamp(start)) & (sales["Date"] <= pd.Timestamp(end))
    & (sales["Store_ID"].isin(store_sel)) & (sales["Product_Category"].isin(cat_sel))
]

if filtered.empty:
    st.warning("No data for these filters. Please widen your selection.")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Sales Patterns", "Forecast", "Store Segments"])

# ---------- Tab 1: Overview ----------
with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"₹{filtered['Revenue'].sum() / 1e7:,.0f} Cr")
    c2.metric("Orders", f"{len(filtered):,}")
    c3.metric("Avg Order Value", f"₹{filtered['Revenue'].mean():,.0f}")
    c4.metric("Units Sold", f"{filtered['Units_Sold'].sum():,}")

    monthly = (filtered.groupby(filtered["Date"].dt.to_period("M").dt.to_timestamp())["Revenue"]
               .sum().reset_index())
    fig = px.line(monthly, x="Date", y="Revenue", markers=True, title="Monthly Revenue")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Revenue stays within a narrow band, so the business is stable with no strong trend.")
# ---------- Tab 2: Sales Patterns ----------
with tab2:
    col1, col2 = st.columns(2)

    cat = (filtered.groupby("Product_Category")["Revenue"].sum()
           .sort_values(ascending=False).reset_index())
    col1.plotly_chart(
        px.bar(cat, x="Product_Category", y="Revenue", title="Revenue by Category"),
        use_container_width=True)
    col1.caption("All categories earn almost the same, so no single category drives sales.")

    reg = (filtered.groupby("Region")["Revenue"].sum()
           .sort_values(ascending=False).reset_index())
    col2.plotly_chart(
        px.bar(reg, x="Region", y="Revenue", title="Revenue by Region"),
        use_container_width=True)
    col2.caption("South and West earn more, likely because they have more stores.")

    col3, col4 = st.columns(2)

    daily = filtered.groupby("Date")["Revenue"].sum().reset_index()
    daily["Weekday"] = daily["Date"].dt.day_name()
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    wd = daily.groupby("Weekday")["Revenue"].mean().reindex(order).reset_index()
    col3.plotly_chart(
        px.bar(wd, x="Weekday", y="Revenue", title="Average Daily Revenue by Weekday"),
        use_container_width=True)
    col3.caption("Every weekday is about the same, so there is no weekly pattern.")

    promo = (filtered.groupby("Promotion_Applied")
             .agg(Avg_Order_Value=("Revenue", "mean"), Orders=("Revenue", "count"))
             .reset_index())
    col4.plotly_chart(
        px.bar(promo, x="Promotion_Applied", y="Avg_Order_Value",
               title="Average Order Value: Promotion vs No Promotion"),
        use_container_width=True)
    col4.caption("Promotions did not make orders bigger.")

    # Discount level
    disc = (filtered.groupby("Discount_Percentage")
            .agg(Avg_Revenue=("Revenue", "mean"), Avg_Units=("Units_Sold", "mean"))
            .reset_index())
    st.plotly_chart(
        px.bar(disc, x="Discount_Percentage", y="Avg_Revenue",
               title="Average Revenue per Order by Discount %"),
        use_container_width=True)
    st.caption("Revenue per order falls as the discount rises, and units sold stay about the same.")

# ---------- Tab 3: Forecast ----------
with tab3:
    st.subheader("90-Day Revenue Forecast (Jan to Mar 2025)")

    daily_all = sales.groupby("Date")["Revenue"].sum().reset_index()
    recent = daily_all.tail(180)

    lr_row = results[results["Model"] == "Linear Regression"].iloc[0]
    band = float(lr_row["RMSE"])
    mape = float(lr_row["MAPE (%)"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=recent["Date"], y=recent["Revenue"],
                             name="Actual (last 180 days)", mode="lines"))
    fig.add_trace(go.Scatter(x=forecast["Date"], y=forecast["Forecasted_Revenue"],
                             name="Forecast", mode="lines", line=dict(color="red")))
    fig.add_trace(go.Scatter(x=forecast["Date"], y=forecast["Forecasted_Revenue"] + band,
                             mode="lines", line=dict(width=0),
                             showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=forecast["Date"], y=forecast["Forecasted_Revenue"] - band,
                             mode="lines", line=dict(width=0), fill="tonexty",
                             fillcolor="rgba(255,0,0,0.15)",
                             name="Likely range (±1 RMSE)", hoverinfo="skip"))
    fig.update_layout(title="Actual vs Forecast Daily Revenue",
                      xaxis_title="Date", yaxis_title="Revenue")
    st.plotly_chart(fig, use_container_width=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("Avg forecast per day", f"₹{forecast['Forecasted_Revenue'].mean() / 1e6:,.1f}M")
    m2.metric("Total forecast (90 days)", f"₹{forecast['Forecasted_Revenue'].sum() / 1e7:,.0f} Cr")
    m3.metric("Typical error (MAPE)", f"{mape:.1f}%")

    st.caption("Daily revenue is very noisy, so treat the line as the expected level, "
               "not an exact value for each day.")

    st.subheader("Monthly Forecast Total")
    fm = (forecast.groupby(forecast["Date"].dt.to_period("M").astype(str))["Forecasted_Revenue"]
          .sum().div(1e7).round(0).reset_index())
    fm.columns = ["Month", "Forecast (₹ Cr)"]
    st.dataframe(fm, use_container_width=True, hide_index=True)

    st.subheader("Model Comparison")
    st.dataframe(results.round(2), use_container_width=True, hide_index=True)
    st.caption("No model clearly beat the simple baseline, so Linear Regression was chosen "
               "for the forecast because it is simple and explainable.")

# ---------- Tab 4: Store Segments ----------
with tab4:
    st.subheader("Store Segments (K-Means, 3 clusters)")

    stores_sorted = stores.sort_values("Total_Revenue", ascending=False)
    fig = px.bar(stores_sorted, x="Store_Location", y="Total_Revenue",
                 color="Segment", title="Total Revenue by Store and Segment")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(stores, x="Orders", y="Avg_Order_Value", color="Segment",
                      size="Total_Revenue", text="Store_Location",
                      title="Orders vs Average Order Value")
    fig2.update_traces(textposition="top center")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Store Details")
    show = stores_sorted[["Store_ID", "Store_Location", "Total_Revenue", "Orders",
                          "Avg_Order_Value", "Avg_Rating", "Avg_Discount", "Segment"]].copy()
    show["Total_Revenue"] = (show["Total_Revenue"] / 1e7).round(1)
    show = show.rename(columns={"Total_Revenue": "Revenue (₹ Cr)"})
    st.dataframe(show.round(2), use_container_width=True, hide_index=True)

    st.subheader("Segment Profile (averages)")
    prof = (stores.groupby("Segment")[["Total_Revenue", "Avg_Order_Value", "Orders",
                                       "Avg_Rating", "Avg_Discount"]].mean().round(2))
    st.dataframe(prof, use_container_width=True)

    st.caption("All stores perform within about 4% of each other, so the segments show small "
               "relative differences. Pune stands apart because it has the most orders but the "
               "lowest average order value.")    
