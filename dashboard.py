import streamlit as st 
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px

st.title('📈 Financial Stock Dashboard Analysis ')

ticker = st.sidebar.text_input('Enter Stock Ticker (e.g., MSFT)', 'MSFT')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')


if ticker and start_date and end_date:
    data = yf.download(ticker, start=start_date, end=end_date)

    
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # --- Show Raw Data ---
    st.subheader(f'{ticker} Historical Data')
    st.write(data)

    # --- Price Chart ---
    fig = px.line(data.reset_index(), x='Date', y='Open', title=f"{ticker} Stock Price - Open")
    st.plotly_chart(fig)

    # --- Tabs Section ---
    pricing_data, fundamental_data, news = st.tabs(["💹 Pricing Data", "📊 Fundamental Data", "📰 Top 10 News"])

    with pricing_data:
        st.header('📈 Price Movements')
        data2 = data.copy()
        data2['% Change'] = data2['Open'] / data2['Open'].shift(1) - 1
        data2.dropna(inplace=True)
        st.write(data2)

        annual_return = data2['% Change'].mean() * 252 * 100
        st.write(f"**Annual Return:** {annual_return:.2f}%")

        stdev = np.std(data2['% Change']) * np.sqrt(252)
        st.write(f"**Standard Deviation (Volatility):** {stdev * 100:.2f}%")

    
else:
    st.warning("Please enter ticker symbol and valid date range.")

from alpha_vantage.fundamentaldata import FundamentalData
with fundamental_data:
    key = 'E7JKKTO4AVSD0OCP'
    fd = FundamentalData (key, output_format = 'pandas')
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader('Income Statement')
    income_statement = fd.get_income_statement_annual(ticker)[0]
    is1 = income_statement.T[2:]
    is1.columns= list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader('Cash Flow Statement')
    cash_flow = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)

from stocknews import StockNews
with news:
    st.header(f'News of {ticker}')
    sn = StockNews(ticker , save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment {news_sentiment}')
