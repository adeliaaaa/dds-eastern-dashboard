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
    [data-testid="column"]:has(div.PortMaker) {
        display: flex;
        align-items: center;
        box-shadow: rgb(0 0 0 / 20%) 0px 2px 1px -1px, rgb(0 0 0 / 14%) 0px 1px 1px 0px, rgb(0 0 0 / 12%) 0px 1px 3px 0px;
        border-radius: 15px;
        padding: 1% 1% 1% 1%;
    }

    [data-testid="column"] {
        display: flex;
        align-items: flex-start;
    }

    .stProgress .st-au {
        height: 10px;
    }

    .stDateInput label{
        display:none;
    }

    .stSelectbox label{
        display:none;
    }

    h1 {
        margin: 0px;
        padding: 0px;
    }

    h3 {
        margin: 0px;
        padding: 0px;
    }

</style>
""",
    unsafe_allow_html=True,
)

cola, colb = st.columns([6,1])
with cola:
    st.title('DDS EASTERN')
with colb:
    selected_type = colb.date_input(
    'Daily',
    datetime.date(2023,7,4), 
    label_visibility="hidden")


col1, col2, col3, col4 = st.columns([2,2,3,2])

with col1:
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    with st.container():
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: flex-start"> REVENUE TO TARGET </div>', unsafe_allow_html=True)
        col1a, col1b = st.columns([3,1])
        with col1a:
            bar = st.progress(90)
        with col1b:
            st.write("90%")
    with st.container():
        st.write(f'<div class="PortMakers" style="font-weight: 600; display: flex; justify-content: flex-start"> REVENUE CONTRIBUTION </div>', unsafe_allow_html=True)
        col1a, col1b = st.columns([3,1])
        with col1a:
            bar = st.progress(45)
        with col1b:
            st.write("45%")
        

with col2:
    
    col2a, col2b = st.columns(2)
    col2c, col2d = st.columns(2)

    with col2a:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center;"> TOTAL REV </div>', unsafe_allow_html=True)
    with col2b:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center;"> DAILY REV </div>', unsafe_allow_html=True)
    with col2c:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center;"> 14.4 Bn </div>', unsafe_allow_html=True)
    with col2d:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center;"> 1.2 Bn </div>', unsafe_allow_html=True)
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)

with col3:
    
    col3a, col3b, col3c = st.columns(3)
    col3d, col3e, col3f = st.columns(3)
    with col3a:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center;"> MoM </div> ', unsafe_allow_html=True)

    with col3b:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center;"> YtD </div>', unsafe_allow_html=True)

    with col3c:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center;"> YoY </div>', unsafe_allow_html=True)

    with col3d:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center;"> -4.5% </div>', unsafe_allow_html=True)

    with col3e:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center;"> -19.4% </div>', unsafe_allow_html=True)

    with col3f:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center;"> -24.0% </div>', unsafe_allow_html=True)
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)


with col4:

    col4a, col4b = st.columns(2)
    col4c, col4d = st.columns(2)
    with col4a:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center;"> RGB </div>', unsafe_allow_html=True)
        
    with col4b:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center;"> MoM </div>', unsafe_allow_html=True)
        
    with col4c:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center;"> 1.2Mn </div>', unsafe_allow_html=True)
        
    with col4d:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center;"> -0.61% </div>', unsafe_allow_html=True)
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)        

col6, col7 = st.columns([5,2])
data = pd.DataFrame({
    "Date": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"],
    "Rev1":  [150, 100, 30, 130, 80, 70, 170, 83, 70, 10, 150, 100, 30, 130, 80, 70, 170, 83, 70, 10, 150, 100, 30, 130, 80, 70, 170, 83, 70, 10, 3],
    "Rev2":  [150, 100, 30, 130, 80, 70, 170, 83, 70, 10, 150, 100, 30, 130, 80, 70, 170, 83, 70, 10, 150, 100, 30, 130, 80, 70, 170, 83, 70, 10, 3],
    "Rev3":  [150, 100, 30, 130, 80, 70, 170, 83, 70, 10, 150, 100, 30, 130, 80, 70, 170, 83, 70, 10, 150, 100, 30, 130, 80, 70, 170, 83, 70, 10, 3]
})
data2 = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Des"],
    "Rev1":  [20, 50, 120, 90, 10, 63, 23, 79, 53, 56, 64, 246],
    "Rev2":  [20, 50, 120, 90, 10, 63, 23, 79, 53, 56, 64, 246],
    "Rev3":  [20, 50, 120, 90, 10, 63, 23, 79, 53, 56, 64, 246]
})

data11 = pd.DataFrame(
    np.random.randn(31, 3),
    columns=['a', 'b', 'c'])

with col6:
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    col6a, col6b = st.columns([4,1])
    selected_type = col6b.selectbox(
    'Daily',
    ('Daily', 'Monthly'), label_visibility="hidden")
    col6a.subheader(f"Trend {selected_type} Revenue")


    if(selected_type == 'Daily'):
        st.line_chart(data11)
    else:
        st.line_chart(data11)

with col7:
    st.subheader("By Cluster")
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)

col8, col9, col10 = st.columns([2,3,2])
with col8:
    st.subheader("By Service")
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)

with col9:
    st.subheader("Top 5 L4 Contributor")
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)

with col10:
    st.subheader("OUTLET DIGITAL AKTIF & REV")
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)


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
# st.write(fig)
