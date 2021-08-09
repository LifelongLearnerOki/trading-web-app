import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import yfinance as yf
yf.pdr_override()
from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.momentum import RSIIndicator

# Page Title 
st.set_page_config(
    page_title="Trading Web App")

st.title("Trading Web App")

## Getting tickers from S&P500 company list ##

@st.cache
def load_data():
    components = pd.read_html('https://en.wikipedia.org/wiki/List_of_S'
                    '%26P_500_companies')[0]
    components.drop('SEC filings', axis=1)
    return components['Symbol']

## Sidebar ##

# Menu
st.sidebar.header("Menu")
menu = ["Technical Analysis","Twitter", "Position Sizing Calculator","About"]
choice = st.sidebar.selectbox("Choose from",menu)

#Choose a stock from S&P500 
st.sidebar.header("Choose Stock")
# tickers = st.selectbox('Choose a stock from S&P500', ('CHKP', 'PANW', 'FTNT', 'PNGAY', 'TKC', 'AKAM', 'BEI'))
ticker = st.sidebar.selectbox('Choose a stock from S&P500', load_data())

st.sidebar.header("Select Date")
#st.sidebar.subheader('Financials')
startdate = st.sidebar.date_input('Start Date', date(2019, 1, 1))
enddate = st.sidebar.date_input('End Date')

#Load stock price data
stockpricedf = pdr.get_data_yahoo(ticker,startdate,enddate)

# External Links
st.sidebar.header('External Links')
marketwatch = '[YahooFinance](https://finance.yahoo.com/quote/'+ticker+')'
st.sidebar.write(marketwatch)

## Viz ##

if choice == "Technical Analysis":
    st.subheader("Technical Analysis")
    
    #Stock Price
    st.line_chart(stockpricedf['Close'])

    # Bollinger Bands (BB)
    indicator_bb = BollingerBands(stockpricedf['Close'])
    
    bb = stockpricedf
    bb['bb_h'] = indicator_bb.bollinger_hband()
    bb['bb_l'] = indicator_bb.bollinger_lband()
    bb = bb[['Close','bb_h','bb_l']]
    
    # Moving Average Convergence Divergence
    macd = MACD(stockpricedf['Close']).macd()

    # Resistence Strength Indicator
    rsi = RSIIndicator(stockpricedf['Close']).rsi()
    
    # Viz price with BB
    st.write('Stock Bollinger Bands')
    st.line_chart(bb)

    # Plot RSI
    st.write('Stock RSI ')
    st.line_chart(rsi)
    
    # Current Data
    st.write('Display Current Data')
    currentdata = st.checkbox('Current Data')
    
    if currentdata:
        displaydata = st.dataframe(stockpricedf)
        if displaydata.empty == True:
            st.write("No data available")
        else:
            st.write(displaydata)
            
if choice == "Twitter":
    st.header("Twitter")
    
    st.write('Twitter analysis option will be added soon! ')
    
if choice == "Position Sizing Calculator":
    
    #Stock Price
    st.line_chart(stockpricedf['Close'])
    
    #Total Trading Capital
    st.subheader("1) Trading Capital")
    capital = st.number_input('Enter your Total Trading Capital ($)', key = "capital")
    
    #Risk per Trade
    st.subheader("2) Risk per Trade")
    riskptrade = st.slider('Choose your Risk per Trade (%)', min_value=0, max_value=10, key = "riskptrade")
    st.write('Your Risk per Trade ($) is', (capital*(riskptrade/100)))
    
    #Trade Entry Price
    st.subheader("3) Entry Price")
    entryprice = st.number_input('Put in the Entry Price ($)', key = "entryprice", step=0.1)
    st.write('Current Stock Price ($)', stockpricedf['Close'].iloc[-1])
    
    #Risk per Share
    st.subheader("4) Risk per Share")
    riskpshare = st.number_input('Enter your risk per share ($)', key = "riskpshare", step=0.1)
    
    #Risk-Reward Ratio
    st.subheader("5) Risk-Reward Ratio")
    riskreward = st.radio('Choose your Risk-Reward Ratio', ['1:2','1:3'])

    
    #Determination of Stop Loss & Take Profit Limits
    st.subheader('6) Calculation Stop Loss & Take Profit')
    stoploss = entryprice-riskpshare
    st.write('Set Stop Loss at ($):', stoploss)
    
    if riskreward == '1:2':
        ratio = 2
        takeprofit = entryprice+(ratio*riskpshare)
        st.write('Set Take Profit at ($):', takeprofit)
    elif riskreward == '1:3':
        ratio = 3
        takeprofit = entryprice+(ratio*riskpshare)
        st.write('Set Take Profit at ($):', takeprofit)
    
    # #Shares to buy & Positzion Size 
    st.subheader("7) Determination Number of Shares to buy and Position Size")

    if riskpshare == False:
        st.write('Please Enter your Risk per Share first')
    else:
        numberOfShares = ((capital*(riskptrade/100))/riskpshare)
        st.write('Number of Shares to buy:', numberOfShares)
        positionsize = numberOfShares * entryprice
        st.write('Your Position Size ($) for this trade is:', positionsize)
    
    st.write("""
    # Do you want to take this trade ?
    """)
    
    if st.button('Take Trade'):
        st.balloons()
        
        
elif choice == "About":
    st.info("Built with Streamlit by [Lifelonglearner](https://www.lifelonglearner.de/)")
    st.write("Inspired by [Adam Khoo](https://www.youtube.com/watch?v=pFHTccTf3QM&list=PLddKKXhQ4Wv9Qx2OeAdR7QQHmNbGJAs4n&index=1)")
    
    