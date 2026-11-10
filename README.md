# Retail Analytics & Sales Forecasting System

## Project Overview

The **Retail Analytics & AI-Powered Sales Forecasting System** is a data analytics project developed using Python and Streamlit. It analyzes retail sales data to identify sales patterns, understand business performance, segment stores, and forecast future revenue.

The project presents the analysis through an interactive dashboard, helping users explore sales trends and make data-driven business decisions.

## Objectives

- Analyze sales performance across stores, product categories, and regions.
- Identify sales trends, patterns, and seasonality.
- Forecast future revenue using time-series forecasting.
- Segment stores based on their sales performance.
- Present insights through an interactive dashboard.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data analysis and model development |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical operations |
| Plotly | Interactive charts and visualizations |
| Streamlit | Interactive dashboard development |
| Scikit-learn | Machine learning and store clustering |

## Project Structure

```text
Retail_Analysis/
│
├── app.py
├── requirements.txt
├── Retail_Analysis_.ipynb
│
├── cleaned_sales.csv
├── forecast.csv
├── model_results.csv
├── store_clusters.csv
│
└── README.md
```

## Dashboard Features

### 1. Overview
- Total revenue
- Total orders
- Average order value
- Units sold
- Monthly revenue trends

### 2. Sales Patterns
- Revenue by product category
- Regional sales analysis
- Average sales by weekday
- Promotion vs. non-promotion analysis
- Discount and revenue relationship

### 3. Revenue Forecasting
- Future revenue prediction
- Actual vs. forecast revenue comparison
- Forecast performance metrics
- Model comparison

### 4. Store Segmentation
- K-Means clustering
- Revenue analysis by store
- Store performance comparison
- Store segment profiles

## Installation and Setup

**Step 1: Clone the repository**

```bash
git clone https://github.com/goutami-rs04/Retail_Analysis.git
```

**Step 2: Navigate to the project folder**

```bash
cd Retail_Analysis
```

**Step 3: Install the required libraries**

```bash
pip install -r requirements.txt
```

**Step 4: Run the Streamlit application**

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## Live Dashboard

[Click here to view the deployed Retail Analytics Dashboard]
(https://retailanalysis-w7sapp6bobfqvf9dmcvfbtd.streamlit.app/)

## Project Workflow

1. Load the original retail sales dataset.
2. Perform data cleaning and preprocessing.
3. Conduct exploratory data analysis (EDA).
4. Analyze sales trends and patterns.
5. Build revenue forecasting models.
6. Apply K-Means clustering for store segmentation.
7. Save the processed datasets and model outputs.
8. Develop an interactive dashboard using Streamlit.
9. Deploy the application online.

## Future Enhancements

- Integrate additional forecasting techniques.
- Improve prediction accuracy through model tuning.
- Add real-time sales data integration.
- Include more advanced business performance indicators.

## Author

**Goutami RS**

Information Science and Engineering

GitHub: [goutami-rs04](https://github.com/goutami-rs04)
