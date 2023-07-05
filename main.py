import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import datetime
import plotly.express as px

from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

st.set_page_config(layout="wide")

st.markdown(
    """
<style>
    # [data-testid="column"] {
    #     display: flex;
    #     align-items: center;
    #     box-shadow: rgb(0 0 0 / 20%) 0px 2px 1px -1px, rgb(0 0 0 / 14%) 0px 1px 1px 0px, rgb(0 0 0 / 12%) 0px 1px 3px 0px;
    #     border-radius: 15px;
    #     padding: 2% 2% 2% 2%;
    # } 
</style>
""",
    unsafe_allow_html=True,
)

st.title('DDS EASTERN')

col1, col2 = st.columns([1, 4])
data = np.random.randn(31, 1)

with col1:
    st.write(f'<div style="font-size:18px; font-weight: 400;"> TOTAL REV </div> <div style="font-size:32px; font-weight: 700; margin:0; padding:0;"> 19.94 Bn </div>', unsafe_allow_html=True)
    st.write("###")
    st.write(f'<div style="font-size:18px; font-weight: 400;"> DAILY REV </div> <div style="font-size:32px; font-weight: 700; margin:0; padding:0;"> 1.17 Bn </div>', unsafe_allow_html=True)
    st.write("###")
    st.write(f'<div style="font-size:18px; font-weight: 400;"> YTD </div> <div style="font-size:32px; font-weight: 700; margin:0; padding:0;"> -19.52% </div>', unsafe_allow_html=True)
    st.write("###")
    st.write(f'<div style="font-size:18px; font-weight: 400;"> YOY </div> <div style="font-size:32px; font-weight: 700; margin:0; padding:0;"> -23.7% </div>', unsafe_allow_html=True)
    st.write("###")
    st.write(f'<div style="font-size:18px; font-weight: 400;"> MTD </div> <div style="font-size:32px; font-weight: 700; margin:0; padding:0;"> -4.77% </div>', unsafe_allow_html=True)


col2.subheader("Daily Revenue Graph")
col2.line_chart(data)


# df = px.data.tips()
# fig = px.pie(df, values='tip', names='day')
# fig.update_layout(
#     autosize=False,
#     width=200,
#     height=200,
#     showlegend=False,
#     margin=dict(t=5, b=5, l=5, r=5)
# )
# fig.update_traces(hovertemplate=None, textposition='outside', textinfo='percent+label', rotation=0)
# col1.write(fig)





df = px.data.tips()
df.drop(df[df['day'] == "Sat"].index, inplace = True)
df.drop(df[df['day'] == "Thur"].index, inplace = True)
fig = px.pie(df, values='tip', names='day', hole=0.7)
fig.update_layout(
    autosize=False,
    width=180,
    height=180,
    showlegend=False,
    margin=dict(t=5, b=5, l=5, r=5)
)
# fig.update_traces(hovertemplate=None, textposition=None, textinfo=None, rotation=0)
fig.update_traces(textinfo='none')
fig.add_annotation(dict(x=0.5, y=0.53,  align='center',
                        xref = "paper", yref = "paper",
                        showarrow = False, 
                        text="<span style='font-size: 22px; color=#555; font-family:Times New Roman'>78% <br> from target</span>"))
# fig2.show()

col3, col4 = st.columns(2)

with col3:
    st.subheader("PREDICTION")
    # col3a, col3b = st.columns(2)
    st.write(f'<div style="font-size:18px; font-weight: 400;"> TOTAL REV </div> <div style="font-size:32px; font-weight: 700; margin:0; padding:0;"> 19.94 Bn </div>', unsafe_allow_html=True)
    st.write("###")
    # st.progress(80, "80%")
    st.write(fig)
    st.write("###")

with col4:
    st.subheader("MTD GROWTH")
    st.write("""
    Games: -18.60%
    <br>
    Video: +9.3%
    <br>
    Music: -5.9%
    <br>
    Vas: +8.2%
    <br>
    Banking: +6.08%
    """, unsafe_allow_html=True)
