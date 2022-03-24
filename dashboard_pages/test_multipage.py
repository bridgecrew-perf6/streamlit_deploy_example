import streamlit as st
import numpy as np
import pandas as pd


def strdate2date(str_date):
    import datetime

    return datetime.datetime.strptime(str_date,'%Y-%m-%d').date()

def app():
    SINAL_POINTER_FILE = "signal_pointer_file.csv"
    DOWNLOADED_DATA_DIR = "./Downloaded_data"
    SIGNAL_POINTER_FILE_ID = st.secrets['signal_pointer_fileid']

    # @st.cache(ttl=6000)
    @st.cache(ttl=600, allow_output_mutation=True, suppress_st_warning=True,
              hash_funcs={"_thread.RLock": lambda _: None, pd.DataFrame: lambda _: None})
    def load_data():
        import pandas as pd

        from gdrive_download_utils import download_signal_pointer_file, download_all_signals
        download_signal_pointer_file(SIGNAL_POINTER_FILE_ID, SINAL_POINTER_FILE)
        download_all_signals(SINAL_POINTER_FILE, DOWNLOADED_DATA_DIR)

        nvda_df = pd.read_csv(DOWNLOADED_DATA_DIR + '/NFLX.csv')
        return nvda_df

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
        maxtags=4,
        key='1')
    # https://carpentries-incubator.github.io/python-interactive-data-visualizations/08-publish-your-app/index.html
    # pip3 freeze > requirements.txt
