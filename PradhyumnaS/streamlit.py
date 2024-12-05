import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📈 Stock Dashboard")
st.sidebar.header("Filter Options")

def fetch_stock_data(symbol):
    try:
        response = requests.get(f"{API_BASE_URL}/stocks/{symbol}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return None

def filter_stocks(filter_criteria, symbols):
    try:
        response = requests.post(
            f"{API_BASE_URL}/stocks/filter",
            params={"symbols": ",".join(symbols)},
            json=filter_criteria,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error filtering stocks: {e}")
        return None

symbols = st.sidebar.text_input("Enter stock symbols (comma-separated)", "AAPL,GOOGL,MSFT").split(",")
min_price = st.sidebar.number_input("Minimum Price", min_value=0.0, value=0.0)
max_price = st.sidebar.number_input("Maximum Price", min_value=0.0, value=1000.0)
min_volume = st.sidebar.number_input("Minimum Volume", min_value=0, value=0)
max_volume = st.sidebar.number_input("Maximum Volume", min_value=0, value=100000000)

filter_criteria = {
    "min_price": min_price,
    "max_price": max_price,
    "min_volume": min_volume,
    "max_volume": max_volume,
}

st.header("Stock Data")

if st.button("Fetch Latest Stock Data"):
    all_data = []
    for symbol in symbols:
        data = fetch_stock_data(symbol.strip())
        if data:
            all_data.append(data)

    if all_data:
        df = pd.DataFrame(all_data)
        st.write("### Latest Stock Data", df)

        fig = px.line(df, x="date", y="close", color="symbol", title="Stock Closing Prices")
        st.plotly_chart(fig)

if st.button("Filter Stocks"):
    filtered_data = filter_stocks(filter_criteria, symbols)
    if filtered_data:
        df_filtered = pd.DataFrame(filtered_data)
        st.write("### Filtered Stock Data", df_filtered)

        fig_filtered = px.bar(
            df_filtered,
            x="symbol",
            y="close",
            color="symbol",
            title="Filtered Stocks by Closing Price",
            labels={"close": "Closing Price"},
        )
        st.plotly_chart(fig_filtered)
