
#import module
import pandas as pd
import streamlit as st
import plotly.express as px 
import altair as alt 
from streamlit_extras.dataframe_explorer import dataframe_explorer 
from datetime import datetime
import datetime 
import plotly.graph_objects as go
from PIL import Image


# Config the page width
st.set_page_config(page_title="Main Report", page_icon="", layout="wide")

#------------------------------- PAGE SETUP ----------------------------------------------------------
about_page = st.Page(
    page="views/about.py",
    title="About",
    icon="📀",
    default=True
)
project_1_page = st.Page(
    page="views/mainreport.py",
    title="Main Report",
    icon="🥽",
)
project_2_page = st.Page(
    page="views/detailreport.py",
    title="Detail Report",
    icon="🤿",
)

#------------------------------- NAVIGATION SETUP ----------------------------------------------------------
pg= st.navigation({
    #"Info": [about_page],
    "Projects": [project_1_page,project_2_page]
})

#------------------------------- RUN NAVIGATION ------------------------------------------------------------
pg.run()
