import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state
if 'start_date' not in st.session_state:
    st.session_state.start_date = pd.to_datetime("2015-01-01")
if 'end_date' not in st.session_state:
    st.session_state.end_date = pd.to_datetime("today")
if 'tickers' not in st.session_state:
    st.session_state.tickers = ["VOO"]

# Page title
st.title("Stock Price Comparison")

# Sidebar controls
ticker_input = st.sidebar.text_input("Add Stock Ticker")
if st.sidebar.button("Add Ticker"):
    if ticker_input and ticker_input.upper() not in [t.upper() for t in st.session_state.tickers]:
        st.session_state.tickers.append(ticker_input.upper())
        st.rerun()

selected_tickers = st.sidebar.multiselect("Selected Tickers", st.session_state.tickers, default=st.session_state.tickers)
st.session_state.tickers = selected_tickers

start_date_input = st.sidebar.date_input("Start Date", st.session_state.start_date)
end_date_input = st.sidebar.date_input("End Date", st.session_state.end_date)

if st.sidebar.button("Apply"):
    st.session_state.start_date = start_date_input
    st.session_state.end_date = end_date_input
    st.rerun()

# Download data
@st.cache_data
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end, auto_adjust=True)
    return data

data = {}
for ticker in st.session_state.tickers:
    df = load_data(ticker, st.session_state.start_date, st.session_state.end_date)
    if df.empty or df["Close"].empty:
        st.warning(f"No data available for {ticker}. Skipping.")
    else:
        data[ticker] = df

if not data:
    st.error("No valid data for any selected tickers.")
    st.stop()

# Plot normalized prices
fig, ax = plt.subplots()
for ticker, df in data.items():
    close_price = df["Close"][ticker]
    normalized = (close_price / close_price.iloc[0]) * 100
    ax.plot(normalized.index, normalized.values, label=ticker)

ax.set_xlabel("Date")
ax.set_ylabel("Normalized Price (Base 100)")
ax.set_title("Stock Price Comparison (Normalized)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# Show data table
st.subheader("Normalized Close Price Data")
df_list = []
for ticker, df in data.items():
    close_price = df["Close"][ticker]
    norm = (close_price / close_price.iloc[0]) * 100
    df_norm = pd.DataFrame({f"{ticker}": norm})
    df_list.append(df_norm)

combined = pd.concat(df_list, axis=1)
st.dataframe(combined.reset_index())
st.dataframe(close_price.reset_index())