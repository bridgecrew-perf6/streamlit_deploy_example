import pandas as pd
import plotly.graph_objects as go
import streamlit as st

#st.write("data_series_path:", st.secrets["data_series"])
st.write("loading from secret")
#df = pd.read_csv('Data/NVDA.csv')
#url = st.secrets["data_series"]

import streamlit as st
from gsheetsdb import connect

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
#@st.cache(ttl=600,
#https://discuss.streamlit.io/t/secrets-management-unhashable-in-st-cache/15409
#@st.cache(ttl=600,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None, pd.DataFrame: lambda _: None
#def run_query(query):
#    rows = conn.execute(query, headers=1)
#    return rows

#sheet_url = st.secrets["public_gsheets_url"]
#sheet_url = st.secrets["data_series"]
#rows = run_query(f'SELECT * FROM "{sheet_url}"')

import requests



#url ='https://drive.google.com/uc?id=' + st.secrets["data_series"].split('/')[-2]
#df = pd.read_csv(url)
#st.write(df.head(10))
@st.cache(ttl=6000)
def load_data():
    from upload2gdrive import download_file_from_google_drive
    from pathlib import Path
    downloaded_data_dir = "./Downloaded_data"
    p = Path(downloaded_data_dir)
    p.mkdir(exist_ok=True)
    destination= downloaded_data_dir+"/meow.csv"
    id="1tOMgTtlmke7CeCzfnX8LpWCLxK16DqS4"
    # make sure your link is set to EDIT
    download_file_from_google_drive(id, destination)


    df = pd.read_csv(destination)
    return df

df = load_data()
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