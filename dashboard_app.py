import os
import streamlit as st
import numpy as np
from PIL import  Image

# Custom imports
from multipage import MultiPage

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
SIGNAL_POINTER_FILE = "signal_pointer_file.csv"
#DOWNLOADED_DATA_DIR = "./Downloaded_data"
#SIGNAL_POINTER_FILE_ID = st.secrets['signal_pointer_fileid']


@st.cache(ttl=600,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def download_all_data():
    print('RUNNING DOWNLOAD ALL DATA')
    from streamlit_project_settings import DOWNLOADED_DATA_DIR, SIGNAL_POINTER_FILE_ID

    from gdrive_download_utils import download_signal_pointer_file, download_all_signals
    download_signal_pointer_file(SIGNAL_POINTER_FILE_ID, SIGNAL_POINTER_FILE)
    download_all_signals(SIGNAL_POINTER_FILE, DOWNLOADED_DATA_DIR)
    pass

download_all_data()



##########################################
##########################################



# Add all your application here
from dashboard_pages import test_multipage, test_multipage2
app.add_page("page1",test_multipage.app)

#app.add_page("Login",login_with_secret.app)
app.add_page("page2",test_multipage2.app)

#app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()
