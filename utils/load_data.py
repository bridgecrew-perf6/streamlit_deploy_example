import streamlit as st


@st.cache(ttl=600,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def load_time_series_data(ticker):
    import pandas as pd
    from streamlit_project_settings import DOWNLOADED_DATA_DIR
    ts_df = pd.read_csv(DOWNLOADED_DATA_DIR +'/'+ ticker.upper() +'.csv')
    return ts_df