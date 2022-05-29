import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# Simple Stock Price App
This is a simple Streamlit Web App which uses the yfinance library to show the opening, closing, highest, lowest and volume stock prices of Google, Apple and Facebook.

Shown are the stock prices for **Apple**, **Google**, and **Facebook**.
""")

# define the stock symbols
tickerSymbols = ['AAPL', 'GOOG', 'FB']

# get data for each stock
tickerData = yf.Tickers(tickerSymbols)

# get the historical prices for each stock
tickerDf = tickerData.history(period='1d', start='2010-01-01', end='2020-01-01')
st.write("""
## Opening Price
""")
st.line_chart(tickerDf.Open)

st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)

st.write("""
## Highest Price
""")
st.line_chart(tickerDf.High)

st.write("""
## Lowest Price
""")
st.line_chart(tickerDf.Low)

st.write("""
## Volume
""")
st.line_chart(tickerDf.Volume)
