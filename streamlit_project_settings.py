import streamlit as st
import os
PROJECT_PATH = os.path.realpath(".")
DOWNLOADED_DATA_DIR = "./Downloaded_data"
SIGNAL_POINTER_FILE_ID = st.secrets['signal_pointer_fileid']
SIGNAL_POINTER_FILE = "SIGNAL_POINTER_LIVE.csv"# # this is the downloaded file (locally @ streamlit instance)
OHLCV_PICKLE = os.path.join(DOWNLOADED_DATA_DIR,'OHLCVDICT.pickle')
VCP_DF_PATH = os.path.join(DOWNLOADED_DATA_DIR,'HARDCOREVCP.csv')