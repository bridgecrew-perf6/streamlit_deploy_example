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

# Add all your application here
from dashboard_pages import test_multipage, test_multipage2
app.add_page("page1",test_multipage.app)

#app.add_page("Login",login_with_secret.app)
app.add_page("page2",test_multipage2.app)

#app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()
