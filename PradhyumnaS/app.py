from dotenv import load_dotenv
import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from transformers import pipeline
import requests
import random
import os
from textblob import TextBlob
import finnhub

sentiment_analyzer = pipeline("sentiment-analysis")

load_dotenv()

finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

def fetch_stock_data(ticker):
    """
    Fetch comprehensive stock data
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1y")
        
        info = stock.info
        
        return df, info
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return None, None

def generate_company_sentiment(ticker):
    """
    Generate sentiment analysis using pre-trained models
    """
    try:
        news = finnhub_client.company_news(ticker, _from="2023-01-01", to="2024-01-01")
        
        sentiments = []
        for article in news[:5]:
            headline = article.get('headline', '')
            
            blob_sentiment = TextBlob(headline).sentiment
            
            hf_sentiment = sentiment_analyzer(headline)[0]
            
            sentiments.append({
                'headline': headline,
                'textblob_polarity': blob_sentiment.polarity,
                'huggingface_sentiment': hf_sentiment['label'],
                'huggingface_score': hf_sentiment['score']
            })
        
        return sentiments
    except Exception as e:
        st.error(f"Error generating sentiment: {e}")
        return []

def create_stock_dashboard():
    """
    Create the main Streamlit dashboard
    """
    st.set_page_config(page_title="Stock Insights", layout="wide")

    
    st.title("📈 AI-Powered Stock Market Insights")
    
    st.sidebar.header("Stock Selector")
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    selected_ticker = st.sidebar.selectbox("Choose a Stock", tickers)
    
    df, company_info = fetch_stock_data(selected_ticker)
    
    if df is not None and company_info is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"{selected_ticker} Stock Price")
            fig_price = px.line(df, x=df.index, y='Close', 
                                title=f'{selected_ticker} Closing Price',
                                labels={'Close': 'Price ($)'})
            fig_price.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_price)
        
        with col2:
            st.subheader("Trading Volume")
            fig_volume = px.bar(df, x=df.index, y='Volume', 
                                title=f'{selected_ticker} Trading Volume')
            fig_volume.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_volume)
        
        st.header("🤖 AI Sentiment Analysis")
        sentiments = generate_company_sentiment(selected_ticker)
        
        for sentiment in sentiments:
            st.markdown(f"""
            **Headline:** {sentiment['headline']}
            - TextBlob Polarity: {sentiment['textblob_polarity']:.2f}
            - HuggingFace Sentiment: {sentiment['huggingface_sentiment']}
            - Confidence: {sentiment['huggingface_score']:.2%}
            """)
        
        st.header("🏢 Company Overview")
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.metric("Current Price", f"${df['Close'].iloc[-1]:.2f}")
            st.metric("Market Cap", f"${company_info.get('marketCap', 'N/A'):,}")
        
        with col_info2:
            st.metric("52-Week High", f"${company_info.get('fiftyTwoWeekHigh', 'N/A')}")
            st.metric("52-Week Low", f"${company_info.get('fiftyTwoWeekLow', 'N/A')}")
        
        st.header("🎲 Market Risk Spectrum")
        risk_scores = {
            "Low Risk": random.uniform(0, 3),
            "Medium Risk": random.uniform(3, 6),
            "High Risk": random.uniform(6, 10)
        }
        
        risk_df = pd.DataFrame.from_dict(risk_scores, orient='index', columns=['Risk Score'])
        fig_risk = px.bar(risk_df, title="Investment Risk Assessment")
        st.plotly_chart(fig_risk)

def main():
    create_stock_dashboard()

if __name__ == "__main__":
    main()