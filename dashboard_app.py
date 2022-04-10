import os
import streamlit as st
import numpy as np
from PIL import  Image

# Custom imports
from multipage import MultiPage

st.set_page_config(layout="wide")
#import login_with_secret
# Create an instance of the app
app = MultiPage()

# Title of the main page
#display = Image.open('Logo.png')
#display = np.array(display)
# st.image(display, width = 400)
# st.title("Data Storyteller Application")
#col1, col2 = st.columns(2)
#col1.image(display, width = 400)
#col2.title("Brite advisors board")

#########################################
#########################################
#SIGNAL_POINTER_FILE = "signal_pointer_file.csv"


@st.cache(ttl=3600,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def download_all_data():
    try:
        from streamlit_project_settings import DOWNLOADED_DATA_DIR, SIGNAL_POINTER_FILE_ID, SIGNAL_POINTER_FILE
        from gdrive_download_utils import download_all_signals, download_file_from_google_drive_sharables
        st.info('running download all data')
        st.info('download signal pointer file')
        download_file_from_google_drive_sharables(SIGNAL_POINTER_FILE_ID, SIGNAL_POINTER_FILE)
        download_all_signals(SIGNAL_POINTER_FILE, DOWNLOADED_DATA_DIR)
        download_file_from_google_drive_sharables(r'1I8mC11owGeO51A-dUG55HPuM7WQvj_eZ', 'netflix_titles')

        download_file_from_google_drive_sharables("1wqQdJe7JCTg9xoh9yaYCtI8XJGmENs42", "TIMESERIES.pkl")

        return True

    except Exception as e:

        st.exception(e)
        return False

@st.cache(ttl=3600,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def download_all_data_new():
    try:
        from streamlit_project_settings import DOWNLOADED_DATA_DIR, SIGNAL_POINTER_FILE_ID, SIGNAL_POINTER_FILE
        from gdrive_download_utils import download_all_signals, download_file_from_google_drive_sharables
        st.info('running download all data')
        st.info('download signal pointer file')
        #SIGNAL_POINTER_FILE_ID = st.secrets['signal_pointer_fileid']
        #SIGNAL_POINTER_FILE = "signal_pointer_file.csv"  # this is the downloaded file (locally @ streamlit instance)
        download_file_from_google_drive_sharables(SIGNAL_POINTER_FILE_ID, SIGNAL_POINTER_FILE)
        download_all_signals(SIGNAL_POINTER_FILE, DOWNLOADED_DATA_DIR)

        return True

    except Exception as e:

        st.exception(e)
        return False


download_all_data_new()
if "vcpable_universe" not in st.session_state:
    from utils.load_universe_info import get_vcpable_universe
    st.session_state.vcpable_universe = get_vcpable_universe()
    #st.info(st.session_state)
    #print(st.session_state.vcpable_universe)

##########################################
##########################################

def strink_sidebar():
    #https://github.com/streamlit/streamlit/issues/2058

    st.markdown(
    f"""
    <style>
    .appview-container .main .block-container{{
            padding-top: {{padding_top}}rem;    }}
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {{
    width: 200px;
    }}
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {{
    width: 200px;
    margin-left: -200px;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

#Add all your application here
# from dashboard_pages import test_multipage, test_multipage2, test_multipage3, factor_explorer, vcp_page, test_timeseries
from dashboard_pages import vcp_page
app.add_page("Daily VCP scanner",vcp_page.app)
#app.add_page("page1",test_multipage.app)
#app.add_page("Ask god",test_multipage2.app)
#app.add_page("Factor",factor_explorer.app)


# The main app
app.run()
from streamlit_project_settings import DOWNLOADED_DATA_DIR, SIGNAL_POINTER_FILE_ID, SIGNAL_POINTER_FILE
from gdrive_download_utils import download_all_signals, download_file_from_google_drive_sharables

#download_file_from_google_drive_sharables("1wqQdJe7JCTg9xoh9yaYCtI8XJGmENs42", "TIMESERIES.pkl")

#download_file_from_google_drive_sharables(r'1I8mC11owGeO51A-dUG55HPuM7WQvj_eZ', 'netflix_titles')
import pandas as pd
#import pickle
#file_to_read = open("TIMESERIES.pkl", "rb")
#loaded_object = pickle.load(file_to_read)
#file_to_read.close()
#print(loaded_object)