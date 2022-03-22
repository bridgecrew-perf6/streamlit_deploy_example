import pandas as pd
import plotly.graph_objects as go
import streamlit as st

#st.write("data_series_path:", st.secrets["data_series"])
st.write("loading from secret")
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

# test streamlit tag
from streamlit_tags import st_tags
keywords = st_tags(
    label='# Enter Keywords:',
    text='Press enter to add more',
    value=['Zero', 'One', 'Two'],
    suggestions=['five', 'six', 'seven',
                 'eight', 'nine', 'three',
                 'eleven', 'ten', 'four'],
    maxtags = 4,
    key='1')
#https://carpentries-incubator.github.io/python-interactive-data-visualizations/08-publish-your-app/index.html
#pip3 freeze > requirements.txt