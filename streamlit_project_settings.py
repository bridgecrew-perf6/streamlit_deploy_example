import streamlit as st
import os
PROJECT_PATH = os.path.realpath(".")
DOWNLOADED_DATA_DIR = "./Downloaded_data"

OVERRIDE_SECRET = False
if not OVERRIDE_SECRET:
    SIGNAL_POINTER_FILE_ID = st.secrets['signal_pointer_fileid']
# below are files that are downloaded to local (locally @ streamlit instance)
SIGNAL_POINTER_FILE = "SIGNAL_POINTER_LIVE.csv"
OHLCV_PICKLE = os.path.join(DOWNLOADED_DATA_DIR,'OHLCVDICT.pickle')
VCP_DF_PATH = os.path.join(DOWNLOADED_DATA_DIR,'LIVEVCP.csv')
RSSCORE_DF_PATH = os.path.join(DOWNLOADED_DATA_DIR,'RSSCORE.csv')
SCTRSCORE_DF_PATH = os.path.abspath(os.path.join(DOWNLOADED_DATA_DIR,'SCTRSCORE.csv'))
MRSQUARE_DF_PATH = os.path.join(DOWNLOADED_DATA_DIR,'MRSQUARE.csv')
STOCKBASIS_DF_PATH = os.path.join(DOWNLOADED_DATA_DIR,"STOCKBASIS.csv")

#streamlit run C:/Users/tclyu/PycharmProjects/streamlit_deploy_example/dashboard_app.py
