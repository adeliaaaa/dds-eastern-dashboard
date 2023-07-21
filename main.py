import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import datetime
import plotly.express as px
from PIL import Image
import base64

import calendar
import plotly.graph_objects as go

from numerize import numerize

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

# --------------------------------------------------------- DATABASE ---------------------------------------------------------
@st.cache_data
def load_data():
    connection = MySQLdb.connect(
        host= 'localhost',
        user='root',
        passwd= '',
        db= 'ddseastern',
        autocommit = True
    )

    db_cursor = connection.cursor()
    # db_cursor.execute('SET workload = OLAP')
    db_cursor.execute('SELECT rev_date, cluster, rev_sum, month, date, divisi FROM digital_2022 WHERE reg = "EASTERN JABOTABEK"')
    table_rows = db_cursor.fetchall()
    raw_data22 = pd.DataFrame(table_rows)

    db_cursor.execute('SELECT rev_date, cluster, rev_sum, month, date, divisi FROM digital_2023 WHERE reg = "EASTERN JABOTABEK"')
    table_rows = db_cursor.fetchall()
    raw_data23 = pd.DataFrame(table_rows)


    db_cursor.execute('select rev_date from digital_2023 order by month desc, date desc limit 1')
    table_rows = db_cursor.fetchall()
    max_date_data = pd.DataFrame(table_rows)

    db_cursor.execute('SELECT bulan, subs FROM rgb_all WHERE reg="EASTERN JABOTABEK"')
    table_rows = db_cursor.fetchall()
    rgb_all = pd.DataFrame(table_rows)

    db_cursor.execute('SELECT service, rev_sum, month, day FROM l4 WHERE regional="EASTERN JABOTABEK"')
    table_rows = db_cursor.fetchall()
    l4 = pd.DataFrame(table_rows)


    max_date_data = datetime.datetime.strptime(max_date_data[0][0], "%d/%m/%Y")

    return max_date_data, raw_data22, raw_data23, rgb_all, l4

# --------------------------------------------------------- FUNCTION ---------------------------------------------------------
def color_negative_to_red(val):
    color = 'red' if val[0] == '-' else 'black'
    return 'color: %s' % color

# ------------------------------------------------ COLLECT & PREPARATION DATA ------------------------------------------------
max_date_data, raw_data22, raw_data23, raw_rgb_all, l4 = load_data()
raw_data22.columns = ['Rev_Date', 'Cluster', 'Rev_sum', 'Month', 'Date', 'Service']
raw_data23.columns = ['Rev_Date', 'Cluster', 'Rev_sum', 'Month', 'Date', 'Service']
raw_rgb_all.columns = ['Date', 'Subs']
l4.columns = ['Service', 'Rev_sum', 'Month', 'Day']
raw_data23['Month'] = raw_data23['Month'].astype('int')
raw_data22['Month'] = raw_data22['Month'].astype('int')
l4['Month'] = l4['Month'].astype('int')
raw_data23['Date'] = raw_data23['Date'].astype('int')
raw_data22['Date'] = raw_data22['Date'].astype('int')
l4['Day'] = l4['Day'].astype('int')

target_revenue_eastern = 46671504423.89

image_down = base64.b64encode(open('./assets/down.png', 'rb').read()).decode('utf-8')
image_up = base64.b64encode(open('./assets/up.png', 'rb').read()).decode('utf-8')

# ------------------------------------------------------- TABLE OUTLET -------------------------------------------------------
outlet = pd.DataFrame({
    "Cluster": ["Kota Bekasi", "Depok", "Bogor", "Sukabumi", "Bekasi", "Kapur", "Total"],
    "Outlet":  ["205", "179", "110", "205", "179", "110", "500"],
    "%":  ["0.08%", "0.10%", "0.05%", "0.08%", "0.10%", "0.05%", "2%"],
    "Rev":  ["21.6jt", "17.2jt", "12.0jt", "21.6jt", "17.2jt", "12.0jt", "54jt"],
})
outlet = outlet.set_index('Cluster')


# ---------------------------------------------------------- HEADER ----------------------------------------------------------
cola, colb = st.columns([6,1])
with cola:
    st.title(':red[DDS REGIONAL] EASTERN')
with colb:
    selected_type = colb.date_input(
    'Daily',
    max_date_data,
    max_value=max_date_data,
    min_value=datetime.datetime(2023, 1, 1),
    label_visibility="hidden")

# -------------------------------------------------------- TOTAL REV ---------------------------------------------------------
total_rev_number_M = raw_data23.loc[(raw_data23['Month'] == selected_type.month) & (raw_data23['Date'] <= selected_type.day), 'Rev_sum'].sum()
total_rev_number_M_1 = raw_data23.loc[(raw_data23['Month'] == (selected_type.month - 1)) & (raw_data23['Date'] <= selected_type.day), 'Rev_sum'].sum()

# -------------------------------------------------------- DAILY REV ---------------------------------------------------------
daily_rev = numerize.numerize(total_rev_number_M / selected_type.day)

# ------------------------------------------------------ REV TO TARGET -------------------------------------------------------
rev_to_target_number = float(total_rev_number_M) / target_revenue_eastern * 100
rev_to_target_gap = numerize.numerize(float(total_rev_number_M) - target_revenue_eastern)

# ----------------------------------------------------------- MoM ------------------------------------------------------------
MoM = numerize.numerize(((total_rev_number_M / total_rev_number_M_1) - 1) * 100)
MoM_gap = numerize.numerize(float(total_rev_number_M - total_rev_number_M_1))

# ----------------------------------------------------------- Y-1 ------------------------------------------------------------
y_1_date = datetime.datetime(2022, selected_type.month, selected_type.day)
total_rev_2022 = raw_data22.loc[(raw_data22['Month'] <= selected_type.month -1) | ((raw_data22['Month'] == selected_type.month) & (raw_data22['Date'] <= selected_type.day)), 'Rev_sum'].sum()
total_rev_2023 = raw_data23.loc[(raw_data23['Month'] <= selected_type.month -1) | ((raw_data23['Month'] == selected_type.month) & (raw_data23['Date'] <= selected_type.day)), 'Rev_sum'].sum()

# ----------------------------------------------------------- YtD ------------------------------------------------------------
YtD = numerize.numerize(((total_rev_2023 / total_rev_2022) - 1) * 100)
YtD_gap = numerize.numerize(float(total_rev_2023 - total_rev_2022))

# ----------------------------------------------------------- YoY ------------------------------------------------------------
total_rev__number_M_22 = raw_data22.loc[(raw_data22['Month'] == selected_type.month) & (raw_data22['Date'] <= selected_type.day), 'Rev_sum'].sum()
YoY = numerize.numerize(((total_rev_number_M / total_rev__number_M_22) - 1) * 100)
YoY_gap = numerize.numerize(float(total_rev_number_M - total_rev__number_M_22))


# -------------------------------------------------------- LINE CHART --------------------------------------------------------
trend_monthly_rev = (raw_data23.groupby(['Month'])['Rev_sum'].sum()).to_frame().reset_index()
trend_monthly_rev.columns = ['Month', 'Actual']
trend_monthly_rev_YoY_data = raw_data22.loc[(raw_data22['Month'] <= selected_type.month -1) | ((raw_data22['Month'] == selected_type.month) & (raw_data22['Date'] <= selected_type.day))]
trend_monthly_rev_YoY = (trend_monthly_rev_YoY_data.groupby(['Month'])['Rev_sum'].sum()).to_frame().reset_index()
trend_monthly_rev_YoY.columns = ['Month', 'Y-1']
trend_monthly = pd.merge(trend_monthly_rev, trend_monthly_rev_YoY, on='Month')
trend_monthly = trend_monthly.set_index('Month')
trend_monthly.index = trend_monthly.index.astype(str)
trend_monthly.rename(index={'1':'Jan', '2':'Feb', '3':'Mar', '4': 'Apr', '5': 'May', '6': 'Jun', '7': 'Jul', '8': 'Aug', '9': 'Sept', '10': 'Oct', '11': 'Nov', '12': 'Des'}, inplace=True)

current_month_data = raw_data23.loc[((raw_data23['Month'] == selected_type.month) & (raw_data23['Date'] <= selected_type.day))]
Y_1_month_data = raw_data22.loc[((raw_data22['Month'] == selected_type.month) & (raw_data22['Date'] <= selected_type.day))]
M_1_data = raw_data23.loc[((raw_data23['Month'] == selected_type.month-1) & (raw_data23['Date'] <= selected_type.day))]

trend_daily_rev = (current_month_data.groupby(['Date'])['Rev_sum'].sum()).to_frame().reset_index()
trend_daily_rev.columns = ['Date', 'Actual']
trend_daily_rev_M_1 = (M_1_data.groupby(['Date'])['Rev_sum'].sum()).to_frame().reset_index()
trend_daily_rev_Y_1 = (Y_1_month_data.groupby(['Date'])['Rev_sum'].sum()).to_frame().reset_index()

trend_daily_rev = trend_daily_rev.set_index('Date')
trend_daily_rev_M_1 = trend_daily_rev_M_1.set_index('Date')
trend_daily_rev_Y_1 = trend_daily_rev_Y_1.set_index('Date')

# ---------------------------------------------------- PIE CHART SERVICE -----------------------------------------------------
rev_service = (current_month_data.groupby(['Service'])['Rev_sum'].sum()).to_frame().reset_index()
rev_service = rev_service.set_index('Service')

rev_service = rev_service[(rev_service.index == 'Digital Banking') | (rev_service.index == 'Digital Music')| (rev_service.index == 'Games Marketplace') | (rev_service.index == 'VAS Content') | (rev_service.index == 'Video')]
rev_service['Rev_sum'] = rev_service['Rev_sum'].apply(lambda x: "{:.2f}".format(x/1000000000))

serviceChart = px.pie(rev_service, values='Rev_sum', names=rev_service.index, color_discrete_sequence= pie_color)

serviceChart.update_layout(showlegend=False)

serviceChart.update_traces(texttemplate = "%{label} <br> %{value}B <br>(%{percent})", rotation=15, textfont_size=14)

# ----------------------------------------------------- PIE CHART CLUSTER ----------------------------------------------------
rev_cluster = (current_month_data.groupby(['Cluster'])['Rev_sum'].sum()).to_frame().reset_index()
rev_cluster = rev_cluster.set_index('Cluster')

rev_cluster = rev_cluster[(rev_cluster.index == 'KOTA BEKASI') | (rev_cluster.index == 'DEPOK')| (rev_cluster.index == 'BOGOR') | (rev_cluster.index == 'SUKABUMI') | (rev_cluster.index == 'BEKASI') | (rev_cluster.index == 'KARAWANG PURWAKARTA')]
rev_cluster['Rev_sum'] = rev_cluster['Rev_sum'].apply(lambda x: "{:.2f}".format(x/1000000000))

clusterChart = px.pie(rev_cluster, values='Rev_sum', names=rev_cluster.index, color_discrete_sequence= pie_color)
clusterChart.update_layout(
    showlegend=False
)
clusterChart.update_traces(texttemplate = "%{label} <br> %{value}B <br>(%{percent})", rotation=45, textfont_size=14)


# ------------------------------------------------------------ RGB -----------------------------------------------------------
last_month_date = datetime.datetime(selected_type.year, selected_type.month-1, selected_type.day)
today_date = selected_type.strftime("%d/%m/%Y")
last_month = last_month_date.strftime("%d/%m/%Y")

rgb_all_M = raw_rgb_all.loc[(raw_rgb_all['Date'] == today_date), 'Subs'].sum()
rgb_all_M_1 = raw_rgb_all.loc[(raw_rgb_all['Date'] == last_month), 'Subs'].sum()

# ------------------------------------------------------ TABLE TOP 5 M -------------------------------------------------------
l4_this_month_data = l4.loc[((l4['Month'] == selected_type.month) & (l4['Day'] <= selected_type.day))]
top_5 = (l4_this_month_data.groupby(['Service'])['Rev_sum'].sum()).to_frame().reset_index().sort_values('Rev_sum', ascending=False)
top_5.columns = ['Service', 'M']
top_5 = top_5.head(5)
# top_5['M'] = top_5['M'].apply(lambda x: "{:.2f}".format(x/1000000000)).astype('str')

# ----------------------------------------------------- TABLE TOP 5 M-1 ------------------------------------------------------
l4_this_month_1_data = l4.loc[(l4['Month'] == selected_type.month-1) & (l4['Day'] <= selected_type.day) & (l4['Service'].isin(top_5['Service']))]
top_5_M_1 = (l4_this_month_1_data.groupby(['Service'])['Rev_sum'].sum()).to_frame().reset_index().sort_values('Rev_sum', ascending=False)
top_5_M_1.columns = ['Service', 'M-1']
top_5 = pd.merge(top_5, top_5_M_1, on='Service')

# ----------------------------------------------------- TABLE TOP 5 MoM ------------------------------------------------------
top_5['MoM'] = ((top_5['M'].astype('float') / top_5['M-1'].astype('float')) - 1) * 100

# -------------------------------------------------------- TABLE TOP 5 -------------------------------------------------------
top_5 = top_5.set_index('Service')
top_5['MoM'] = top_5['MoM'].apply(lambda x: "{:.2f}%".format(x)).astype('str')
top_5['M-1'] = top_5['M-1'].apply(lambda x: "{:.2f}".format(x/1000000000)).astype('str')
top_5['M'] = top_5['M'].apply(lambda x: "{:.2f}".format(x/1000000000)).astype('str')
top_5 = top_5.style.applymap(color_negative_to_red)

# ---------------------------------------------------------- DESIGN ----------------------------------------------------------

col1, col2, col3, col4 = st.columns([2,2,3,2])
with col1:
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    with st.container():
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: flex-start; font-size:1.2vw;"> REVENUE TO TARGET </div>', unsafe_allow_html=True)
        col1a, col1b = st.columns([4,3])
        gap = "1.16Mn"
        
        with col1a:
            bar = st.progress(int(rev_to_target_number))
        with col1b:
            st.write(f"{numerize.numerize(rev_to_target_number)}%, {rev_to_target_gap}")

    with st.container():
        st.write(f'<div class="PortMakers" style="font-weight: 600; display: flex; justify-content: flex-start; font-size:1.2vw;"> REVENUE CONTRIBUTION </div>', unsafe_allow_html=True)
        col1a, col1b = st.columns([4,3])
        with col1a:
            bar = st.progress(45)
        with col1b:
            st.write("45%")
        

with col2:
    col2a, col2b = st.columns(2)
    col2c, col2d = st.columns(2)


    with col2a:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> TOTAL REV </div>', unsafe_allow_html=True)
    with col2b:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> DAILY REV </div>', unsafe_allow_html=True)
    with col2c:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> {numerize.numerize(float(total_rev_number_M))} </div>', unsafe_allow_html=True)
        
    with col2d:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> {daily_rev} </div>', unsafe_allow_html=True)
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
        if(MoM_gap[0] == '-'):
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {MoM}% <img src="data:image/png;base64,{image_down}" width="21" height="21"/> </div> ', unsafe_allow_html=True)
        else:
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {MoM}% <img src="data:image/png;base64,{image_up}" width="21" height="21"/> </div> ', unsafe_allow_html=True)
    with col3e:
        if(YtD_gap[0] == '-'):
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {YtD}% <img src="data:image/png;base64,{image_down}" width="21" height="21"/> </div>', unsafe_allow_html=True)
        else:
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {YtD}% <img src="data:image/png;base64,{image_up}" width="21" height="21"/> </div>', unsafe_allow_html=True)
    with col3f:
        if(YoY_gap[0] == '-'):
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {YoY}% <img src="data:image/png;base64,{image_down}" width="21" height="21"/> </div>', unsafe_allow_html=True)
        else:
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {YoY}% <img src="data:image/png;base64,{image_up}" width="21" height="21"/> </div>', unsafe_allow_html=True)
    with col3g:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.15vw;"> Gap </div> ', unsafe_allow_html=True)
    with col3h:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.15vw;"> Gap </div>', unsafe_allow_html=True)
    with col3i:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.15vw;"> Gap </div>', unsafe_allow_html=True)
    with col3j:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {MoM_gap} </div> ', unsafe_allow_html=True)
    with col3k:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {YtD_gap} </div>', unsafe_allow_html=True)
    with col3l:
        st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {YoY_gap} </div>', unsafe_allow_html=True)
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)


with col4:
    col4a, col4b = st.columns(2)
    col4c, col4d = st.columns(2)

    with col4a:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> RGB </div>', unsafe_allow_html=True)
        
    with col4b:
        st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> MtD </div>', unsafe_allow_html=True)
        
    if(rgb_all_M == 0 or rgb_all_M_1 == 0):
        with col4c:
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> - </div>', unsafe_allow_html=True)
            
        with col4d:
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> - </div> ', unsafe_allow_html=True) 
                
    else:
        with col4c:
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> {numerize.numerize(float(rgb_all_M))} </div>', unsafe_allow_html=True)        
        with col4d:
            rgb_mtd = ((rgb_all_M/rgb_all_M_1)-1) * 100
            if(rgb_mtd < 0):
                st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {numerize.numerize(rgb_mtd)}% <img src="data:image/png;base64,{image_down}" width="21" height="21"/> </div> ', unsafe_allow_html=True)
            else:
                st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {numerize.numerize(rgb_mtd)}% <img src="data:image/png;base64,{image_up}" width="21" height="21"/> </div> ', unsafe_allow_html=True)
    
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)        

col6, col7 = st.columns([6,3])
with col6:
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    col6a, col6b = st.columns([4,1])
    selected_type = col6b.selectbox(
    'Daily',
    ('Daily', 'Monthly'), label_visibility="hidden")

    col6a.subheader(f"Trend {selected_type} Revenue")

    if(selected_type == 'Daily'):
        lchart = px.line(trend_daily_rev, line_shape="spline", color_discrete_sequence= px.colors.qualitative.Plotly, markers=True)
        lchart.update_layout(autosize=True, legend_title=None, yaxis_title='Revenue', legend=dict(
            orientation = "h",
            xanchor = "center",
            x = 0.5,
            y = -0.2,
            entrywidth=40
        ))
        lchart.add_traces(go.Scatter(x=trend_daily_rev_M_1.index, y=trend_daily_rev_M_1['Rev_sum'], name='M-1', line_shape="spline", mode='markers+lines'))
        lchart.add_traces(go.Scatter(x=trend_daily_rev_Y_1.index, y=trend_daily_rev_Y_1['Rev_sum'], name='Y-1', line_shape="spline", mode='markers+lines'))
        lchart.update_xaxes(dtick=1)
        lchart
    else:
        lchart = px.line(trend_monthly, line_shape="spline", color_discrete_sequence= px.colors.qualitative.Plotly, markers=True)
        lchart.update_layout(autosize=True, legend_title=None, yaxis_title='Revenue', legend=dict(
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
    st.dataframe(top_5, use_container_width=True)

with col10:
    st.subheader("Outlet Digital Aktif & Rev")
    st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
    st.dataframe(outlet, use_container_width=True)


if st.checkbox('Show raw data'):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Raw data22')
        st.write(raw_data22)
    with col2:
        st.subheader('Raw data23')
        st.write(raw_data23)
    # groupped_by = raw_data22.groupby('Cluster')

    # st.write(groupped_by.first())
    # st.subheader('Data Bogor')
    # st.write(groupped_by.get_group('BOGOR'))

def debug():
    st.write("m", total_rev_number_M)
    st.write("m-1", total_rev_number_M_1)
    st.write("total rev 22", total_rev_2022)
    st.write("total rev 23", total_rev_2023)
    st.write("selected_type", selected_type)
    st.write("today", selected_type.strftime("%d/%m/%Y"))
    st.write("last year", y_1_date.strftime("%d/%m/%Y"))


