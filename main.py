import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
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
        padding: 0.5% 0.7% 0.5% 0.7%;
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

    .stPlotlyChart {
        width:100%;
    }


    # .stDataFrame {
    #     width:100%;
    # }

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
    date.today(), 
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
    "Rev1":  [111, 117, 109, 111, 81, 69, 82, 80, 70, 71, 102, 100, 102, 102, 99, 88, 79, 82, 84, 69, 100, 103, 91, 78, 82, 72, 82, 79, 77, 111, 99],
    "Rev2":  [108, 110, 116, 100, 70, 81, 80, 70, 69, 80, 111, 112, 109, 105, 102, 92, 98, 83, 72, 92, 89, 89, 69, 85, 79, 73, 78, 83, 70, 110, 87],
    "Rev3":  [114, 121, 122, 119, 95, 80, 89, 78, 80, 93, 109, 99, 106, 112, 110, 91, 101, 92, 80, 82, 99, 107, 88, 98, 80, 71, 79, 81, 76, 100, 71]
})
data = data.set_index('Date')



data2 = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Des"],
    "Rev1":  [25, 45, 167, 70, 71, 46, 51, 94, 62, 56, 38, 112],
    "Rev2":  [21, 66, 143, 83, 30, 63, 23, 79, 53, 61, 61, 142],
    "Rev3":  [35, 73, 168, 89, 90, 99, 32, 92, 41, 42, 24, 99]
})
data2 = data2.set_index('Month')



with col6:
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    col6a, col6b = st.columns([4,1])
    selected_type = col6b.selectbox(
    'Daily',
    ('Daily', 'Monthly'), label_visibility="hidden")
    col6a.subheader(f"Trend {selected_type} Revenue")


    if(selected_type == 'Daily'):
        lchart = px.line(data)
        lchart.update_layout(autosize=True, legend_title=None, legend=dict(
            orientation = "h",
            xanchor = "center",
            x = 0.5,
            y = -0.2,
            entrywidth=40
        ))
        lchart.update_xaxes(dtick=1)
        lchart
    else:
        lchart = px.line(data2)
        lchart.update_layout(autosize=True, legend_title=None, legend=dict(
            orientation = "h",
            xanchor = "center",
            x = 0.5,
            y = -0.2,
            entrywidth=40
        ))
        lchart

with col7:
    st.subheader("By Cluster")
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)

top5 = pd.DataFrame({
    "Service": ["Videomax", "Google Playstore", "Ipoint", "Content", "Pulsa"],
    "M":  [3.8, 1.13, 0.34, 3.88, 1.13],
    "MoM":  ["-5.53%", "-44.9%", "0.09%", "-5.53%", "-44.9%"],
    "YtD":  ["-22.6%", "-64.8%", "-55.5%", "-22.6%", "-64.8%"],
    "YoY":  ["-27.8%", "-64.8%", "-35.6%", "-27.8%", "-64.8%"]
})
top5 = top5.set_index('Service')


outlet = pd.DataFrame({
    "Cluster": ["Kota Bekasi", "Depok", "Bogor", "Sukabumi", "Bekasi", "Kapur"],
    "M":  [205, 179, 110, 205, 179, 110],
    "MoM":  ["0.08%", "0.10%", "0.05%", "0.08%", "0.10%", "0.05%"],
    "YtD":  ["21.6jt", "17.2jt", "12.0jt", "21.6jt", "17.2jt", "12.0jt"],
})
outlet = outlet.set_index('Cluster')

col8, col9, col10 = st.columns([2,3,2])
with col8:
    st.subheader("By Service")
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)

with col9:
    st.subheader("Top 5 L4 Contributor")
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    st.dataframe(top5, use_container_width=True)

with col10:
    st.subheader("Outlet Digital Aktif & Rev")
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    st.dataframe(outlet, use_container_width=True)

