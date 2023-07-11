import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import plotly.express as px
from PIL import Image
import base64

from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

st.set_page_config(layout="wide")

# pie_color = px.colors.sequential.deep
pie_color = px.colors.sequential.Burgyl

# ----------------------------------------------------------- STYLING --------------------------------------------------------
st.markdown(
    """
<style>
    
    .css-fg4pbf [data-testid="column"]:has(div.PortMaker) {
        display: flex;
        align-items: center;
        box-shadow: rgb(0 0 0 / 20%) 0px 2px 1px -1px, rgb(0 0 0 / 14%) 0px 1px 1px 0px, rgb(0 0 0 / 12%) 0px 1px 3px 0px;
        border-radius: 15px;
        padding: 0.5% 0.7% 0.5% 0.7%;
    }

    .css-ffhzg2 [data-testid="column"]:has(div.PortMaker) {
        display: flex;
        align-items: center;
        box-shadow: rgb(255 255 255 / 20%) 0px 2px 1px -1px, rgb(255 255 255 / 14%) 0px 1px 1px 0px, rgb(255 255 255 / 12%) 0px 1px 3px 0px;
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

# -------------------------------------------------------- LINE CHART --------------------------------------------------------
data = pd.DataFrame({
    "Date": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"],
    "Actual":  [111, 117, 109, 111, 81, 85, 82, 80, 70, 71, 102, 100, 102, 102, 99, 88, 79, 82, 84, 92, 100, 103, 91, 78, 82, 72, 82, 79, 99, 111, 99],
    "MoM":  [108, 110, 116, 100, 91, 81, 80, 72, 69, 80, 101, 112, 109, 105, 102, 92, 94, 83, 80, 85, 102, 113, 109, 85, 79, 73, 79, 88, 102, 110, 87],
    "YoY":  [114, 121, 122, 119, 95, 80, 89, 78, 80, 93, 109, 99, 95, 89, 102, 90, 87, 86, 81, 82, 99, 107, 88, 98, 80, 71, 79, 81, 100, 100, 71]
})
data = data.set_index('Date')

data2 = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Des"],
    "Actual":  [25, 45, 167, 70, 71, 46, 51, 94, 62, 56, 38, 112],
    "MoM":  [21, 66, 143, 83, 30, 63, 23, 79, 53, 61, 61, 142],
    "YoY":  [35, 73, 168, 89, 90, 65, 32, 92, 41, 42, 24, 99]
})
data2 = data2.set_index('Month')


# ---------------------------------------------------- PIE CHART SERVICE -----------------------------------------------------
service = pd.DataFrame({
    "Service": ["Digital Banking", "Vas Content", "Music", "Video", "Games Marketplace"],
    "Rev":  np.random.randint(40,200,size=5)
})
serviceChart = px.pie(service, values='Rev', names='Service', color_discrete_sequence= pie_color)

serviceChart.update_layout(
    showlegend=False
)

serviceChart.update_traces(textinfo='label+percent+value', rotation=45, textfont_size=14)
# serviceChart.update_traces(textinfo='label+percent', textposition='outside')

# ----------------------------------------------------- PIE CHART CLUSTER ----------------------------------------------------
cluster = pd.DataFrame({
    "Cluster": ["Kota Bekasi", "Depok", "Bogor", "Sukabumi", "Bekasi", "Kapur"],
    "Rev":  np.random.randint(30,190,size=6)
})
clusterChart = px.pie(cluster, values='Rev', names='Cluster', color_discrete_sequence= pie_color)
clusterChart.update_layout(
    showlegend=False
)
clusterChart.update_traces(textinfo='label+percent+value', rotation=45, textfont_size=14)


# -------------------------------------------------------- TABLE TOP 5 -------------------------------------------------------
top5 = pd.DataFrame({
    "Service": ["Videomax", "Google Playstore", "Upoint", "Transfer Pulsa", "Content RBT"],
    "M":  ["4.36", "3.88", "1.13", "0.75", "0.28"],
    "M-1": ["4.33", "4.11", "2.04", "0.71", "0.28"],
    "MoM":  ["-5.53%", "-44.9%", "0.09%", "-5.53%", "-44.9%"],
    "YtD":  ["-22.6%", "-64.8%", "-55.5%", "-22.6%", "-64.8%"],
    "YoY":  ["-27.8%", "-64.8%", "-35.6%", "-27.8%", "-64.8%"]
})
top5 = top5.set_index('Service')


# ------------------------------------------------------- TABLE OUTLET -------------------------------------------------------
outlet = pd.DataFrame({
    "Cluster": ["Kota Bekasi", "Depok", "Bogor", "Sukabumi", "Bekasi", "Kapur", "Total"],
    "Outlet":  ["205", "179", "110", "205", "179", "110", "500"],
    "%":  ["0.08%", "0.10%", "0.05%", "0.08%", "0.10%", "0.05%", "2%"],
    "Rev":  ["21.6jt", "17.2jt", "12.0jt", "21.6jt", "17.2jt", "12.0jt", "54jt"],
})
outlet = outlet.set_index('Cluster')



# th_props = [
#     ('font-size', '14px'),
#     ('text-align', 'left'),
#     ('font-weight', 'bold'),
#     ('color', '#6d6d6d'),
#     ('background-color', '#f8f9fb')
#   ]

                                    
# td_props = [
#   ('font-size', '12px')
#   ]
                                 

# styles = [
#   dict(selector="th", props=th_props),
#   dict(selector="td", props=td_props)
#   ]
# top5=top5.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)


cola, colb = st.columns([6,1])
with cola:
    st.title(':red[DDS REGIONAL] EASTERN')
with colb:
    selected_type = colb.date_input(
    'Daily',
    date.today(),
    max_value=date.today(),
    label_visibility="hidden")


col1, col2, col3, col4 = st.columns([2,2,3,2])
with col1:
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    with st.container():
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: flex-start; font-size:1.2vw;"> REVENUE TO TARGET </div>', unsafe_allow_html=True)
        col1a, col1b = st.columns([4,2])
        gap = "1.16Mn"
        
        if((selected_type.day %3) == 0):
            with col1a:
                bar = st.progress(90)
            with col1b:
                st.write(f"90%, -{gap}")
        elif((selected_type.day %2) == 0):
            with col1a:
                bar = st.progress(72)
            with col1b:
                st.write(f"72%, -{gap}")
        else:
            with col1a:
                bar = st.progress(20)
            with col1b:
                st.write(f"20%, -{gap}")

    with st.container():
        st.write(f'<div class="PortMakers" style="font-weight: 600; display: flex; justify-content: flex-start; font-size:1.2vw;"> REVENUE CONTRIBUTION </div>', unsafe_allow_html=True)
        col1a, col1b = st.columns([4,2])
        if((selected_type.day %3) == 0):
            with col1a:
                bar = st.progress(45)
            with col1b:
                st.write("45%")
        elif((selected_type.day %2) == 0):
            with col1a:
                bar = st.progress(93)
            with col1b:
                st.write("93%")
        else:
            with col1a:
                bar = st.progress(78)
            with col1b:
                st.write("78%")
        

with col2:
    col2a, col2b = st.columns(2)
    col2c, col2d = st.columns(2)

    with col2a:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> TOTAL REV </div>', unsafe_allow_html=True)
    with col2b:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> DAILY REV </div>', unsafe_allow_html=True)
    with col2c:
        if((selected_type.day %3) == 0):
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> 14.4 Bn </div>', unsafe_allow_html=True)
        elif((selected_type.day %2) == 0):
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> 13.1 Bn </div>', unsafe_allow_html=True)
        else:
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> 12.0 Bn </div>', unsafe_allow_html=True)
        
    with col2d:
        if((selected_type.day %3) == 0):
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> 1.2 Bn </div>', unsafe_allow_html=True)
        elif((selected_type.day %2) == 0):
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> 0.9 Bn </div>', unsafe_allow_html=True)
        else:
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> 0.8 Bn </div>', unsafe_allow_html=True)
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)


with col3:
    col3a, col3b, col3c = st.columns(3)
    col3d, col3e, col3f = st.columns(3)
    col3g, col3h, col3i = st.columns(3)
    col3j, col3k, col3l = st.columns(3)

    with col3a:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> MoM </div> ', unsafe_allow_html=True)

    with col3b:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> YtD </div>', unsafe_allow_html=True)

    with col3c:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> YoY </div>', unsafe_allow_html=True)

    with col3d:
        image = base64.b64encode(open('./assets/down.png', 'rb').read()).decode('utf-8')
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> -4.5% <img src="data:image/png;base64,{image}" width="21" height="21"/> </div> ', unsafe_allow_html=True)
    with col3e:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> -19.4% <img src="data:image/png;base64,{image}" width="21" height="21"/> </div>', unsafe_allow_html=True)
    with col3f:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> -24.0% <img src="data:image/png;base64,{image}" width="21" height="21"/> </div>', unsafe_allow_html=True)
    with col3g:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.15vw;"> Gap </div> ', unsafe_allow_html=True)
    with col3h:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.15vw;"> Gap </div>', unsafe_allow_html=True)
    with col3i:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.15vw;"> Gap </div>', unsafe_allow_html=True)
    with col3j:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> 1.2Mn </div> ', unsafe_allow_html=True)
    with col3k:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> 2.5Mn </div>', unsafe_allow_html=True)
    with col3l:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> 0.8Mn </div>', unsafe_allow_html=True)
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)


with col4:
    col4a, col4b = st.columns(2)
    col4c, col4d = st.columns(2)

    with col4a:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> RGB </div>', unsafe_allow_html=True)
        
    with col4b:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> MoM </div>', unsafe_allow_html=True)
        
    with col4c:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> 1.2Mn </div>', unsafe_allow_html=True)
        
    with col4d:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> -0.61% </div>', unsafe_allow_html=True)
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)        

col6, col7 = st.columns([6,3])
with col6:
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    col6a, col6b = st.columns([4,1])
    selected_type = col6b.selectbox(
    'Daily',
    ('Daily', 'Monthly'), label_visibility="hidden")
    # with col6a:
    #     st.write(f'<div style="font-weight: 600; display: flex; justify-content: flex-start; font-size:2vw;"> Trend {selected_type} Revenue </div>', unsafe_allow_html=True)
    col6a.subheader(f"Trend {selected_type} Revenue")

    if(selected_type == 'Daily'):
        lchart = px.line(data, line_shape="spline")
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
        lchart = px.line(data2, line_shape="spline")
        lchart.update_layout(autosize=True, legend_title=None, legend=dict(
            orientation = "h",
            xanchor = "center",
            x = 0.5,
            y = -0.2,
            entrywidth=40
        ))
        lchart

with col7:
    st.subheader("By Service")
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    st.plotly_chart(serviceChart, use_container_width=True)

col8, col9, col10 = st.columns([3,3,2])
with col8:
    st.subheader("By Cluster")
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    st.plotly_chart(clusterChart, use_container_width=True)

with col9:
    st.subheader("Top 5 L4 Contributor")
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    st.dataframe(top5, use_container_width=True)

with col10:
    st.subheader("Outlet Digital Aktif & Rev")
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    st.dataframe(outlet, use_container_width=True)

