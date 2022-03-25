import streamlit as st
import numpy as np
import pandas as pd


def strdate2date(str_date):
    import datetime
    return datetime.datetime.strptime(str_date,'%Y-%m-%d').date()

"""
@st.cache(ttl=600,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def load_time_series_data(ticker):
    import pandas as pd
    ts_df = pd.read_csv(DOWNLOADED_DATA_DIR +'/'+ ticker.upper() +'.csv')
    return ts_df
"""

def app():
    st.write('hello world 2')
    from utils.load_data import load_time_series_data
    import plotly.graph_objects as go
    df = load_time_series_data('NFLX')

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