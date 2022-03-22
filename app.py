import pandas as pd
import plotly.graph_objects as go
import streamlit as st
df = pd.read_csv('Data/NVDA.csv')
print(df.head(10))

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
st.plotly_chart(fig)
st.write('Enter welcome to streamlit deploy example')
txt = st.text_input(label='Enter something here')
st.write(txt)
#https://carpentries-incubator.github.io/python-interactive-data-visualizations/08-publish-your-app/index.html
#pip3 freeze > requirements.txt