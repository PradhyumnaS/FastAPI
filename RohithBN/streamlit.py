import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Data Viz Dashboard", layout="wide")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.sidebar.header("Filters")
    
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    x_column = st.sidebar.selectbox("Select X axis", df.columns)
    y_column = st.sidebar.selectbox("Select Y axis", numeric_columns)
    
    plot_type = st.sidebar.selectbox("Select Plot Type", 
                                   ["Scatter", "Line", "Bar", "Box"])
    
    st.title("Data Analysis Dashboard")
    
    st.subheader("Data Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Dataset Shape:", df.shape)
    with col2:
        st.write("Columns:", ", ".join(df.columns))
    
    if plot_type == "Scatter":
        fig = px.scatter(df, x=x_column, y=y_column)
    elif plot_type == "Line":
        fig = px.line(df, x=x_column, y=y_column)
    elif plot_type == "Bar":
        fig = px.bar(df, x=x_column, y=y_column)
    else:
        fig = px.box(df, x=x_column, y=y_column)
        
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Summary Statistics")
    st.write(df.describe())

else:
    st.info("Upload a CSV file to begin analysis")
