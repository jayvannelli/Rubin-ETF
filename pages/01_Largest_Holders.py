import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

FMP_BASE_URL = "https://financialmodelingprep.com/api/v4/"

st.header("Largest Stock Holders")

ticker = st.text_input("Ticker: ")

# Hard coded dates, but they can be taken as a variable
dates = ["2022-06-30", "2022-03-31", "2021-12-31", "2021-09-30"]

def stock_ownership_by_holders(symbol, date, page=0, return_df=True):
    req_url = FMP_BASE_URL + f"institutional-ownership/institutional-holders/symbol-ownership-percent?symbol={symbol.upper()}&date={date}&page={page}&apikey={st.secrets['FMP_TOKEN']}"
    req = requests.get(req_url).json()

    if return_df == True:
        df = pd.DataFrame(req)
    else:
        df = req

    return df

def plot_largest_holders(df, top_x_holders=10):
    fig, ax = plt.subplots()

    ax.barh(df[:top_x_holders]['investorName'], df[:top_x_holders]['sharesNumber'])

    ax.set_ylabel('Institution')
    ax.set_xlabel('Quantity of Shares')
    ax.set_title(f"{df['date'][0]} Quarterly 13-F Reportings")

    current_x_ticks = plt.gca().get_xticks()
    plt.gca().set_xticklabels(['{:,.0f}'.format(x) for x in current_x_ticks])
    plt.xticks(rotation=45)

    return plt

if ticker:
    top_x_holders = st.selectbox("Display the top ___ holders", [5, 10, 15, 20])

    col1, col2 = st.columns(2)

    counter = 0
    for date in dates:
        df = stock_ownership_by_holders(ticker, date)
        plot = plot_largest_holders(df, top_x_holders)
        if counter % 2 == 0:
            col1.pyplot(plot)
        else:
            col2.pyplot(plot)
        counter+=1
    
    
    
