import streamlit as st
import numpy as np
import pandas as pd


def strdate2date(str_date):
    import datetime
    return datetime.datetime.strptime(str_date,'%Y-%m-%d').date()

def app():
    st.write('hello world PAGE2')