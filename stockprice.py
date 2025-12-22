import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state
if 'start_date' not in st.session_state:
    st.session_state.start_date = pd.to_datetime("2015-01-01")
if 'end_date' not in st.session_state:
    st.session_state.end_date = pd.to_datetime("today")
if 'ticker' not in st.session_state:
    st.session_state.ticker = "VOO"

# Page title
st.title(f"{st.session_state.ticker} Close Price vs Time")

# Sidebar controls
ticker_input = st.sidebar.text_input("Stock Ticker", st.session_state.ticker)
start_date_input = st.sidebar.date_input("Start Date", st.session_state.start_date)
end_date_input = st.sidebar.date_input("End Date", st.session_state.end_date)

if st.sidebar.button("Apply"):
    st.session_state.ticker = ticker_input
    st.session_state.start_date = start_date_input
    st.session_state.end_date = end_date_input
    st.rerun()

# Download data
@st.cache_data
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end, auto_adjust=True)
    return data

data = load_data(st.session_state.ticker, st.session_state.start_date, st.session_state.end_date)

# Check if data is valid
if data.empty or data["Close"].empty:
    st.error("Invalid ticker or no data available for the selected ticker and date range.")
    st.stop()

# Extract Close price
close_price = data["Close"].iloc[:, 0]

# Plot
fig, ax = plt.subplots()
ax.plot(close_price.index, close_price.values)
ax.set_xlabel("Date")
ax.set_ylabel("Close Price (USD)")
ax.set_title(f"{st.session_state.ticker} Close Price Over Time")
ax.grid(True)

st.pyplot(fig)

# Show data table
st.subheader(f"{st.session_state.ticker} Close Price Data")
st.dataframe(close_price.reset_index())