import streamlit as st
import pandas as pd
import numpy as np
import requests

import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf

st.set_option('deprecation.showPyplotGlobalUse', False)
FMP_BASE_URL = "https://financialmodelingprep.com/api/v4/"

st.header("Stock Institutional Ownership Statistics")

ticker = st.text_input("Ticker: ")

def get_price_history(ticker, period="2y"):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

def plot_stock_chart(df):
    fig = mpf.plot(df, type='candle', style='charles', volume=True)
    st.pyplot(fig)

def institutional_ownership_stats(symbol, include_current_quarter=True, return_df=True):
    req_url = FMP_BASE_URL + f"institutional-ownership/symbol-ownership?symbol={symbol.upper()}&includeCurrentQuarter={include_current_quarter}&apikey={st.secrets['FMP_TOKEN']}"
    req = requests.get(req_url).json()
    
    if return_df == True:
        df = pd.DataFrame(req)
    else:
        df = req
    
    return df

def plot_number_of_13f_shares(df, last=6):
    fig, ax = plt.subplots()

    ax.bar(df[:last]['date'], df[:last]['numberOf13Fshares'])

    ax.set_ylabel('Number of 13-F Shares')
    plt.xticks(rotation=45)

    st.pyplot(plt)

def plot_new_and_closed_positions(df, last=6):
    x = np.arange(last)
    width = 0.35

    fig, ax = plt.subplots()
    r1 = ax.bar(x - width/2, df[:last]['newPositions'], width, label='New Positions')
    r2 = ax.bar(x + width/2, df[:last]['closedPositions'], width, label='Closed Positions')

    ax.set_ylabel('Quantity of Positions')
    ax.set_xticks(x, df[:last]['date'])

    plt.xticks(rotation=45)
    ax.bar_label(r1, padding=3)
    ax.bar_label(r2, padding=3)

    fig.tight_layout()

    ax.legend()

    st.pyplot(plt)

def plot_increased_and_decreased_positions(df, last=6):
    x = np.arange(last)
    width = 0.35

    fig, ax = plt.subplots()
    r1 = ax.bar(x - width/2, df[:last]['increasedPositions'], width, label='Increased Positions')
    r2 = ax.bar(x + width/2, df[:last]['reducedPositions'], width, label='Reduced Positions')

    ax.set_ylabel('Quantity of Positions')
    ax.set_xticks(x, df[:last]['date'])

    plt.xticks(rotation=45)
    ax.bar_label(r1, padding=3)
    ax.bar_label(r2, padding=3)

    fig.tight_layout()

    ax.legend()

    st.pyplot(plt)

def plot_put_call_ratio(df, last=6):
    fig, ax = plt.subplots()

    ax.bar(df[:last]['date'], df[:last]['putCallRatio'])

    ax.set_ylabel('Put/Call Ratio')
    plt.xticks(rotation=45)

    st.pyplot(plt)

if ticker:
    institutional_stats = institutional_ownership_stats(ticker)

    df = get_price_history(ticker)
    plot_stock_chart(df)

    col1, col2 = st.columns(2)
    with col1:
        st.write('Total Number of 13-F Shares by Quarter')
        plot_number_of_13f_shares(institutional_stats, last=6)
        st.write('Increased & Reduced Positions by Quarter')
        plot_increased_and_decreased_positions(institutional_stats, last=6)
    with col2:
        st.write('Put/Call Ratio by Quarter')
        plot_put_call_ratio(institutional_stats, last=6)
        st.write('New & Closed Positions by Quarter')
        plot_new_and_closed_positions(institutional_stats, last=6)
    
    st.write(institutional_stats)