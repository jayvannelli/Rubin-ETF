import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

FMP_BASE_URL = "https://financialmodelingprep.com/api/"

st.header("ETF Stock Exposure")

col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input("Ticker: ")
with col2:
    sort_by = st.selectbox("Sort by: ", ["Quantity of Shares", "Weight Percentage"])
with col3:
    top_x_etfs = st.selectbox("View the top ___ etfs: ", [5, 10, 15, 20, 25, 30])

def get_etf_stock_exposure(ticker, return_df=True):
    req_url = FMP_BASE_URL + f"v3/etf-stock-exposure/{ticker.upper()}?apikey={st.secrets['FMP_TOKEN']}"
    req = requests.get(req_url).json()

    if return_df == True:
        df = pd.DataFrame(req)
    else:
        df = req

    return df

def plot_etf_exposure(df, sorted_by, top_x_values=10):
    if sorted_by == "shares":
        fig, ax = plt.subplots()

        ax.bar(df[:top_x_values]['etfSymbol'], df[:top_x_values]['sharesNumber'])

        ax.set_ylabel('Number of Shares')

        current_y_ticks = plt.gca().get_yticks()
        plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_y_ticks])

        plt.xticks(rotation=60)
    else:
        fig, ax = plt.subplots()

        ax.bar(df[:top_x_values]['etfSymbol'], df[:top_x_values]['weightPercentage'])

        ax.set_ylabel('Weight Percentage of Fund')
        plt.xticks(rotation=60)

    st.pyplot(plt)

if ticker:
    etf_exposure = get_etf_stock_exposure(ticker)

    if sort_by == "Quantity of Shares":
        df = etf_exposure.sort_values(by='sharesNumber', ascending=False)
        plot_etf_exposure(df, "shares", top_x_etfs)
    else:
        df = etf_exposure.sort_values(by="weightPercentage", ascending=False)
        plot_etf_exposure(df, "weighting", top_x_etfs)

    st.dataframe(df)