import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import datetime
import plotly.express as px


st.set_page_config(layout="wide")
st.title('RGB')


# This dataframe has 244 lines, but 4 distinct values for `day`
df = px.data.tips()
fig = px.pie(df, values='tip', names='day')
st.write(fig)