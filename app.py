import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.write("data_series_path:", st.secrets["data_series"])

#df = pd.read_csv('Data/NVDA.csv')
url = st.secrets["data_series"]
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
df = pd.read_csv(url)
st.write(df.head(10))

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