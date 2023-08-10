import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

import plotly.graph_objects as go

from function import regexFromDate2022, regexFromDate2022OneMonth, color_negative_to_red, PIE_COLOR, load_data, addCustomStyle, branchToCluster, TARGET_REVENUE_EASTERN, TARGET_REVENUE_BEKASI, TARGET_REVENUE_BOGOR, TARGET_REVENUE_KARAWANG, IMAGE_DOWN, IMAGE_UP, TARGET_REVENUE_DAILY_EASTERN, TARGET_REVENUE_DAILY_BEKASI, TARGET_REVENUE_DAILY_BOGOR, TARGET_REVENUE_DAILY_KARAWANG
from numerize import numerize

st.set_page_config(layout="wide")

# ----------------------------------------------------------- STYLING --------------------------------------------------------
addCustomStyle()

# ------------------------------------------------ COLLECT & PREPARATION DATA ------------------------------------------------
# max_date_data, raw_data22, raw_data23, raw_rgb_all, raw_l4, raw_l4_2022, raw_outlet, outlet_data, eastern_jabotabek_all_revenue = load_data('All')
max_date_data, raw_data22, raw_data23, raw_rgb_all, raw_l4, raw_l4_2022, raw_outlet, outlet_data = load_data('All')
raw_data22.columns = ['Rev_Date', 'Cluster', 'Rev_sum', 'Month', 'Date', 'Service']
raw_data23.columns = ['Rev_Date', 'Cluster', 'Rev_sum', 'Month', 'Date', 'Service']
raw_rgb_all.columns = ['Date', 'Subs', 'Cluster']
raw_l4.columns = ['Service', 'Rev_sum', 'Month', 'Day', 'Divisi', 'Cluster']
raw_l4_2022.columns = ['Date', 'Service', 'Rev_sum', 'Cluster']
raw_outlet.columns = ['Cluster', 'Outlet Register']
outlet_data.columns = ['Cluster', 'Outlet', 'Rev_sum']
# eastern_jabotabek_all_revenue.columns = ['Keterangan', 'Value']
# eastern_jabotabek_all_revenue
# all_rev_eastern = eastern_jabotabek_all_revenue.loc[eastern_jabotabek_all_revenue['Keterangan'] == 'all revenue', 'Value'].iloc[0]
# all_rev_eastern
# target_revenue_eastern = eastern_jabotabek_all_revenue.loc[eastern_jabotabek_all_revenue['Keterangan'] == 'target revenue eastern', 'Value'].iloc[0]
# target_revenue_eastern
# target_revenue_daily_eastern = eastern_jabotabek_all_revenue.loc[eastern_jabotabek_all_revenue['Keterangan'] == 'target revenue daily eastern', 'Value'].iloc[0]
# target_revenue_daily_eastern

raw_data23['Month'] = raw_data23['Month'].astype('int')
raw_data22['Month'] = raw_data22['Month'].astype('int')
raw_l4['Month'] = raw_l4['Month'].astype('int')
raw_data23['Date'] = raw_data23['Date'].astype('int')
raw_data22['Date'] = raw_data22['Date'].astype('int')
raw_l4['Day'] = raw_l4['Day'].astype('int')
raw_outlet['Outlet Register'] = raw_outlet['Outlet Register'].astype('int')
outlet_data['Outlet'] = outlet_data['Outlet'].astype('int')
outlet_data['Rev_sum'] = outlet_data['Rev_sum'].astype('int')




# ---------------------------------------------------------- HEADER ----------------------------------------------------------
cola, colb, colc = st.columns([9, 1, 2])
with cola:
    st.title(':red[DDS REGIONAL] EASTERN')
with colb:
    selected_type = colb.date_input(
    'Daily',
    max_date_data,
    max_value=max_date_data,
    min_value=datetime.datetime(2023, 1, 1),
    label_visibility="hidden")
with colc:
    selected_branch = st.selectbox(
        'EASTERN JABOTABEK',
        ('EASTERN JABOTABEK', 'BEKASI', 'BOGOR', 'KARAWANG PURWAKARTA'), label_visibility="hidden"
    ) 

# -------------------------------------------------------- TOTAL REV ---------------------------------------------------------
list_cluster_in_branch = branchToCluster(selected_branch)
raw_data23_branch = raw_data23.loc[raw_data23['Cluster'].isin(list_cluster_in_branch)]
raw_data22_branch = raw_data22.loc[raw_data22['Cluster'].isin(list_cluster_in_branch)]
# if(selected_branch == 'EASTERN JABOTABEK'):
#     raw_data23_branch = raw_data23
#     raw_data22_branch = raw_data22
# else:
#     raw_data23_branch = raw_data23.loc[raw_data23['Cluster'] == selected_branch]
#     raw_data22_branch = raw_data22.loc[raw_data22['Cluster'] == selected_branch]

total_rev_number_M = raw_data23_branch.loc[(raw_data23_branch['Month'] == selected_type.month) & (raw_data23_branch['Date'] <= selected_type.day), 'Rev_sum'].sum()
if(selected_type.month == 1):
    total_rev_number_M_1 = raw_data22_branch.loc[(raw_data22_branch['Month'] == 12) & (raw_data22_branch['Date'] <= selected_type.day), 'Rev_sum'].sum()
else:
    total_rev_number_M_1 = raw_data23_branch.loc[(raw_data23_branch['Month'] == (selected_type.month - 1)) & (raw_data23_branch['Date'] <= selected_type.day), 'Rev_sum'].sum()

# ------------------------------------------------ DAILY REV & REV TO TARGET -------------------------------------------------
daily_rev = total_rev_number_M / selected_type.day

if(selected_branch == 'EASTERN JABOTABEK'):
    daily_rev_gap = numerize.numerize(float(daily_rev - TARGET_REVENUE_DAILY_EASTERN))
    rev_to_target_number = float(total_rev_number_M) / TARGET_REVENUE_EASTERN * 100
    rev_to_target_gap = numerize.numerize(float(total_rev_number_M) - TARGET_REVENUE_EASTERN)
elif(selected_branch == 'BEKASI'):
    daily_rev_gap = numerize.numerize(float(daily_rev - TARGET_REVENUE_DAILY_BEKASI))
    rev_to_target_number = float(total_rev_number_M) / TARGET_REVENUE_BEKASI * 100
    rev_to_target_gap = numerize.numerize(float(total_rev_number_M) - TARGET_REVENUE_BEKASI)
elif(selected_branch == 'BOGOR'):
    daily_rev_gap = numerize.numerize(float(daily_rev - TARGET_REVENUE_DAILY_BOGOR))
    rev_to_target_number = float(total_rev_number_M) / TARGET_REVENUE_BOGOR * 100
    rev_to_target_gap = numerize.numerize(float(total_rev_number_M) - TARGET_REVENUE_BOGOR)
elif(selected_branch == 'KARAWANG PURWAKARTA'):
    daily_rev_gap = numerize.numerize(float(daily_rev - TARGET_REVENUE_DAILY_KARAWANG))
    rev_to_target_number = float(total_rev_number_M) / TARGET_REVENUE_KARAWANG * 100
    rev_to_target_gap = numerize.numerize(float(total_rev_number_M) - TARGET_REVENUE_KARAWANG)
else:
    daily_rev_gap = numerize.numerize(float(daily_rev - TARGET_REVENUE_DAILY_EASTERN))
    rev_to_target_number = float(total_rev_number_M) / TARGET_REVENUE_EASTERN * 100
    rev_to_target_gap = numerize.numerize(float(total_rev_number_M) - TARGET_REVENUE_EASTERN)

# ----------------------------------------------------------- MoM ------------------------------------------------------------
MoM = numerize.numerize(((total_rev_number_M / total_rev_number_M_1) - 1) * 100)
MoM_gap = numerize.numerize(float(total_rev_number_M - total_rev_number_M_1))

# ----------------------------------------------------------- Y-1 ------------------------------------------------------------
y_1_date = datetime.datetime(2022, selected_type.month, selected_type.day)
total_rev_2022 = raw_data22_branch.loc[(raw_data22_branch['Month'] <= selected_type.month -1) | ((raw_data22_branch['Month'] == selected_type.month) & (raw_data22_branch['Date'] <= selected_type.day)), 'Rev_sum'].sum()
total_rev_2023 = raw_data23_branch.loc[(raw_data23_branch['Month'] <= selected_type.month -1) | ((raw_data23_branch['Month'] == selected_type.month) & (raw_data23_branch['Date'] <= selected_type.day)), 'Rev_sum'].sum()

# ----------------------------------------------------------- YtD ------------------------------------------------------------
YtD = numerize.numerize(((total_rev_2023 / total_rev_2022) - 1) * 100)
YtD_gap = numerize.numerize(float(total_rev_2023 - total_rev_2022))

# ----------------------------------------------------------- YoY ------------------------------------------------------------
total_rev__number_M_22 = raw_data22_branch.loc[(raw_data22_branch['Month'] == selected_type.month) & (raw_data22_branch['Date'] <= selected_type.day), 'Rev_sum'].sum()
YoY = numerize.numerize(((total_rev_number_M / total_rev__number_M_22) - 1) * 100)
YoY_gap = numerize.numerize(float(total_rev_number_M - total_rev__number_M_22))

# -------------------------------------------------------- LINE CHART --------------------------------------------------------
trend_monthly_rev_actual_data = raw_data23_branch.loc[(raw_data23_branch['Month'] <= selected_type.month -1) | ((raw_data23_branch['Month'] == selected_type.month) & (raw_data23_branch['Date'] <= selected_type.day))]
trend_monthly_rev = (trend_monthly_rev_actual_data.groupby(['Month'])['Rev_sum'].sum()).to_frame().reset_index()
trend_monthly_rev.columns = ['Month', 'Actual']
trend_monthly_rev_YoY_data = raw_data22_branch.loc[(raw_data22_branch['Month'] <= selected_type.month -1) | ((raw_data22_branch['Month'] == selected_type.month) & (raw_data22_branch['Date'] <= selected_type.day))]
trend_monthly_rev_YoY = (trend_monthly_rev_YoY_data.groupby(['Month'])['Rev_sum'].sum()).to_frame().reset_index()
trend_monthly_rev_YoY.columns = ['Month', 'Y-1']
trend_monthly = pd.merge(trend_monthly_rev, trend_monthly_rev_YoY, on='Month')
trend_monthly = trend_monthly.set_index('Month')
trend_monthly.index = trend_monthly.index.astype(str)
trend_monthly.rename(index={'1':'Jan', '2':'Feb', '3':'Mar', '4': 'Apr', '5': 'May', '6': 'Jun', '7': 'Jul', '8': 'Aug', '9': 'Sept', '10': 'Oct', '11': 'Nov', '12': 'Des'}, inplace=True)

current_month_data = raw_data23_branch.loc[((raw_data23_branch['Month'] == selected_type.month) & (raw_data23_branch['Date'] <= selected_type.day))]
Y_1_month_data = raw_data22_branch.loc[((raw_data22_branch['Month'] == selected_type.month) & (raw_data22_branch['Date'] <= selected_type.day))]
if(selected_type.month == 1):
    M_1_data = raw_data22_branch.loc[((raw_data22_branch['Month'] == 12) & (raw_data22_branch['Date'] <= selected_type.day))]
else:
    M_1_data = raw_data23_branch.loc[((raw_data23_branch['Month'] == selected_type.month-1) & (raw_data23_branch['Date'] <= selected_type.day))]

trend_daily_rev = (current_month_data.groupby(['Date'])['Rev_sum'].sum()).to_frame().reset_index()
trend_daily_rev.columns = ['Date', 'Actual']
trend_daily_rev_M_1 = (M_1_data.groupby(['Date'])['Rev_sum'].sum()).to_frame().reset_index()
trend_daily_rev_Y_1 = (Y_1_month_data.groupby(['Date'])['Rev_sum'].sum()).to_frame().reset_index()

trend_daily_rev = trend_daily_rev.set_index('Date')
# trend_daily_rev_M_1 = trend_daily_rev_M_1.set_index('Date')
# trend_daily_rev_Y_1 = trend_daily_rev_Y_1.set_index('Date')

# ---------------------------------------------------- PIE CHART SERVICE -----------------------------------------------------
rev_service = (current_month_data.groupby(['Service'])['Rev_sum'].sum()).to_frame().reset_index()
rev_service = rev_service.set_index('Service')

rev_service = rev_service[(rev_service.index == 'Digital Banking') | (rev_service.index == 'Digital Music')| (rev_service.index == 'Games Marketplace') | (rev_service.index == 'VAS Content') | (rev_service.index == 'Video')]
rev_service['Rev_sum'] = rev_service['Rev_sum'].apply(lambda x: "{:.2f}".format(x/1000000000))

serviceChart = px.pie(rev_service, values='Rev_sum', names=rev_service.index, color_discrete_sequence= PIE_COLOR)

serviceChart.update_layout(showlegend=False)

serviceChart.update_traces(texttemplate = "%{label} <br> %{value}B <br>(%{percent})", textfont_size=14)

# ----------------------------------------------------- PIE CHART CLUSTER ----------------------------------------------------
rev_cluster = (current_month_data.groupby(['Cluster'])['Rev_sum'].sum()).to_frame().reset_index()
rev_cluster = rev_cluster.set_index('Cluster')

rev_cluster = rev_cluster[(rev_cluster.index == 'KOTA BEKASI') | (rev_cluster.index == 'DEPOK')| (rev_cluster.index == 'BOGOR') | (rev_cluster.index == 'SUKABUMI') | (rev_cluster.index == 'BEKASI') | (rev_cluster.index == 'KARAWANG PURWAKARTA')]
rev_cluster['Rev_sum'] = rev_cluster['Rev_sum'].apply(lambda x: "{:.2f}".format(x/1000000000))

clusterChart = px.pie(rev_cluster, values='Rev_sum', names=rev_cluster.index, color_discrete_sequence= PIE_COLOR)
clusterChart.update_layout(
    showlegend=False
)
clusterChart.update_traces(texttemplate = "%{label} <br> %{value}B <br>(%{percent})", rotation=30, textfont_size=14)


# ------------------------------------------------------------ RGB -----------------------------------------------------------
raw_rgb_all_branch = raw_rgb_all.loc[(raw_rgb_all['Cluster'].isin(list_cluster_in_branch))]
rgbbb = (raw_rgb_all_branch.groupby(['Date'])['Subs'].sum()).to_frame().reset_index().sort_values('Date', ascending=False)
rgbM = rgbbb.take([0])
rgbM_1 = rgbbb.take([1])

# ------------------------------------------------------ TABLE TOP 5 M -------------------------------------------------------
today_r4_data = raw_l4.loc[((raw_l4['Month'] == selected_type.month) & (raw_l4['Day'] == selected_type.day))]

if(not today_r4_data.empty):
    raw_l4_branch = raw_l4.loc[(raw_l4['Cluster'].isin(list_cluster_in_branch))]
    raw_l4_2022_branch = raw_l4_2022.loc[(raw_l4_2022['Cluster'].isin(list_cluster_in_branch))]
    # ------------------------------------------------------ TABLE TOP 5 M -------------------------------------------------------
    top_5_m = pd.DataFrame()
    l4_this_month_data = raw_l4_branch.loc[((raw_l4_branch['Month'] == selected_type.month) & (raw_l4_branch['Day'] <= selected_type.day))]
    top_5 = (l4_this_month_data.groupby(['Service'])['Rev_sum'].sum()).to_frame().reset_index().sort_values('Rev_sum', ascending=False)
    top_5.columns = ['Service', 'M']
    top_5 = top_5.head(5)
    top_5_m = top_5.copy()

    # ----------------------------------------------------- TABLE TOP 5 M-1 ------------------------------------------------------
    if(selected_type.month == 1):
        regex_dec_month_2022 = regexFromDate2022OneMonth(selected_type.day, 12)
        l4_2022_dec = raw_l4_2022_branch[raw_l4_2022_branch.Date.str.contains(regex_dec_month_2022, regex=True, na=False)]
        l4_this_month_1_data = l4_2022_dec.loc[(l4_2022_dec['Service'].isin(top_5['Service']))]
    else:
        l4_this_month_1_data = raw_l4_branch.loc[(raw_l4_branch['Month'] == selected_type.month-1) & (raw_l4_branch['Day'] <= selected_type.day) & (raw_l4_branch['Service'].isin(top_5['Service']))]

    top_5_M_1 = (l4_this_month_1_data.groupby(['Service'])['Rev_sum'].sum()).to_frame().reset_index().sort_values('Rev_sum', ascending=False)
    top_5_M_1.columns = ['Service', 'M-1']
    top_5 = pd.merge(top_5, top_5_M_1, on='Service')

    # ----------------------------------------------------- TABLE TOP 5 MoM ------------------------------------------------------
    top_5['MoM'] = ((top_5['M'].astype('float') / top_5['M-1'].astype('float')) - 1) * 100

    # ----------------------------------------------------- TABLE TOP 5 YtD ------------------------------------------------------
    regex_final = regexFromDate2022(selected_type.day, selected_type.month)
    l4_2022_until_now = raw_l4_2022_branch[raw_l4_2022_branch.Date.str.contains(regex_final, regex=True, na=False)]
    top_5_2022 = l4_2022_until_now.loc[l4_2022_until_now['Service'].isin(top_5['Service'])]
    top_5_2022 = (top_5_2022.groupby(['Service'])['Rev_sum'].sum()).to_frame().reset_index().sort_values('Rev_sum', ascending=False)
    top_5_2022.columns = ['Service', '2022']

    l4_2023_until_now = raw_l4_branch.loc[ (raw_l4_branch['Month'] <= selected_type.month - 1) | ((raw_l4_branch['Month'] == selected_type.month) & (raw_l4_branch['Day'] <= selected_type.day))]
    top_5_2023 = l4_2023_until_now.loc[l4_2023_until_now['Service'].isin(top_5['Service'])]
    top_5_2023 = (top_5_2023.groupby(['Service'])['Rev_sum'].sum()).to_frame().reset_index().sort_values('Rev_sum', ascending=False)
    top_5_2023.columns = ['Service', '2023']

    top_5 = pd.merge(top_5, top_5_2022, on='Service')
    top_5 = pd.merge(top_5, top_5_2023, on='Service')
    top_5['YtD'] = ((top_5['2023'] / top_5['2022']) - 1) * 100

    # ----------------------------------------------------- TABLE TOP 5 YoY ------------------------------------------------------
    regex_1_month_2022 = regexFromDate2022OneMonth(selected_type.day, selected_type.month)
    l4_2022_1_month = raw_l4_2022_branch[raw_l4_2022_branch.Date.str.contains(regex_1_month_2022, regex=True, na=False)]
    top_5_2022_1_month = l4_2022_1_month.loc[l4_2022_1_month['Service'].isin(top_5['Service'])]
    top_5_2022_1_month = (top_5_2022_1_month.groupby(['Service'])['Rev_sum'].sum()).to_frame().reset_index().sort_values('Rev_sum', ascending=False)
    top_5_2022_1_month.columns = ['Service', 'month-22']

    top_5 = pd.merge(top_5, top_5_2022_1_month, on='Service')
    top_5['YoY'] = ((top_5['M'] / top_5['month-22']) - 1) * 100

    # -------------------------------------------------------- TABLE TOP 5 -------------------------------------------------------
    top_5 = top_5.set_index('Service')

    top_5 = top_5.drop(['2022', '2023', 'month-22'], axis=1)

    top_5['MoM'] = top_5['MoM'].apply(lambda x: "{:.2f}%".format(x)).astype('str')
    top_5['M-1'] = top_5['M-1'].apply(lambda x: "{:.2f}".format(x/1000000000)).astype('str')
    top_5['M'] = top_5['M'].apply(lambda x: "{:.2f}".format(x/1000000000)).astype('str')

    top_5['YtD'] = top_5['YtD'].apply(lambda x: "{:.2f}%".format(x)).astype('str')
    top_5['YoY'] = top_5['YoY'].apply(lambda x: "{:.2f}%".format(x)).astype('str')
    top_5 = top_5.style.applymap(color_negative_to_red)

# ------------------------------------------------------- TABLE OUTLET -------------------------------------------------------
outlet = raw_outlet.set_index('Cluster')
outlet = pd.merge(outlet, outlet_data, on='Cluster')
outlet['%'] = (outlet['Outlet'] / outlet['Outlet Register']) * 100
outlet = outlet.drop(['Outlet Register'], axis=1)

outlet = outlet.set_index('Cluster')
outlet.loc['EASTERN JABOTABEK']= outlet.sum(numeric_only=True)

outlet['Outlet'] = outlet['Outlet'].astype('str')
outlet['Rev_sum'] = outlet['Rev_sum'].apply(lambda x: "{:.2f}".format(x/1000000)).astype('str')
outlet['%'] = outlet['%'].apply(lambda x: "{:.2f}%".format(x)).astype('str')

outlet.columns = ['Outlet', 'Rev(M)', '%']

# ---------------------------------------------------------- DESIGN ----------------------------------------------------------
def createUI():
    col1, col2, col3, col4 = st.columns([2,2,3,2])
    with col1:
        st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
        with st.container():
            st.write(f'<div style="font-weight: 600; display: flex; justify-content: flex-start; font-size:1.2vw;"> REVENUE TO TARGET </div>', unsafe_allow_html=True)
            col1a, col1b = st.columns([4,4])
            
            with col1a:
                st.progress(int(rev_to_target_number))
            with col1b:
                st.write(f"{numerize.numerize(rev_to_target_number)}%, {rev_to_target_gap}")

        # with st.container():
        #     st.write(f'<div class="PortMakers" style="font-weight: 600; display: flex; justify-content: flex-start; font-size:1.2vw;"> REVENUE CONTRIBUTION </div>', unsafe_allow_html=True)
        #     rev_contribution = int(float(total_rev_number_M) / float(all_rev_eastern) * 100)
            
        #     col1a, col1b = st.columns([4,3])
        #     with col1a:
        #         st.progress(rev_contribution)
        #     with col1b:
        #         st.write(f"{rev_contribution}%")
            
    with col2:
        col2a, col2b = st.columns(2)
        col2c, col2d = st.columns(2)
        col2e, col2f = st.columns(2)

        with col2a:
            st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> TOTAL REV </div>', unsafe_allow_html=True)
        with col2b:
            st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> DAILY REV </div>', unsafe_allow_html=True)
        
        with col2c:
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> {numerize.numerize(float(total_rev_number_M))} </div>', unsafe_allow_html=True)           
        with col2d:
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw; flex-direction: column; align-items: center;"> {numerize.numerize(float(daily_rev))} </div>', unsafe_allow_html=True)
        
        with col2f:
            st.write(f'<hr class="solid"> <div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {daily_rev_gap} </div>', unsafe_allow_html=True)
        
        st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)


    with col3:
        col3a, col3b, col3c = st.columns(3)
        col3d, col3e, col3f = st.columns(3)
        # col3g, col3h, col3i = st.columns(3)
        col3j, col3k, col3l = st.columns(3)

        with col3a:
            st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> MoM </div> ', unsafe_allow_html=True)

        with col3b:
            st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> YtD </div>', unsafe_allow_html=True)

        with col3c:
            st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> YoY </div>', unsafe_allow_html=True)

        with col3d:
            if(MoM_gap[0] == '-'):
                st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {MoM}% <img src="data:image/png;base64,{IMAGE_DOWN}" width="21" height="21"/> </div> ', unsafe_allow_html=True)
            else:
                st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {MoM}% <img src="data:image/png;base64,{IMAGE_UP}" width="21" height="21"/> </div> ', unsafe_allow_html=True)
        with col3e:
            if(YtD_gap[0] == '-'):
                st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {YtD}% <img src="data:image/png;base64,{IMAGE_DOWN}" width="21" height="21"/> </div>', unsafe_allow_html=True)
            else:
                st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {YtD}% <img src="data:image/png;base64,{IMAGE_UP}" width="21" height="21"/> </div>', unsafe_allow_html=True)
        with col3f:
            if(YoY_gap[0] == '-'):
                st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {YoY}% <img src="data:image/png;base64,{IMAGE_DOWN}" width="21" height="21"/> </div>', unsafe_allow_html=True)
            else:
                st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {YoY}% <img src="data:image/png;base64,{IMAGE_UP}" width="21" height="21"/> </div>', unsafe_allow_html=True)
        # with col3g:
        #     st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.15vw;"> Gap </div> ', unsafe_allow_html=True)
        # with col3h:
        #     st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.15vw;"> Gap </div>', unsafe_allow_html=True)
        # with col3i:
        #     st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.15vw;"> Gap </div>', unsafe_allow_html=True)
        with col3j:
            st.write(f'<hr class="solid"> <div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {MoM_gap} </div> ', unsafe_allow_html=True)
        with col3k:
            st.write(f'<hr class="solid"> <div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {YtD_gap} </div>', unsafe_allow_html=True)
        with col3l:
            st.write(f'<hr class="solid"> <div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {YoY_gap} </div>', unsafe_allow_html=True)
        st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)


    with col4:
        col4a, col4b = st.columns(2)
        col4c, col4d = st.columns(2)
        col4e, col4f = st.columns(2)

        with col4a:
            st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> RGB </div>', unsafe_allow_html=True)
            
        with col4b:
            st.write(f'<div style="font-weight: 600; display: flex; justify-content: center; font-size:1.2vw;"> MoM </div>', unsafe_allow_html=True)
            
        with col4c:
            st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; font-size:1.5vw;"> {numerize.numerize(float(rgbM.iloc[0]["Subs"]))} </div>', unsafe_allow_html=True)        
        
        with col4d:
            rgb_mtd = ((rgbM.iloc[0]['Subs']/rgbM_1.iloc[0]['Subs'])-1) * 100
            if(rgb_mtd < 0):
                st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {numerize.numerize(rgb_mtd)}% <img src="data:image/png;base64,{IMAGE_DOWN}" width="21" height="21"/> </div> ', unsafe_allow_html=True)
            else:
                st.write(f'<div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center; gap:5px;  font-size:1.5vw;"> {numerize.numerize(rgb_mtd)}% <img src="data:image/png;base64,{IMAGE_UP}" width="21" height="21"/> </div> ', unsafe_allow_html=True)
        
        with col4f:
            st.write(f'<hr class="solid"> <div style="font-weight: 900; font-size: 22px; margin:0px; padding:0; display: flex; justify-content: center; align-items: center;  font-size:1.5vw;"> {numerize.numerize(float(rgbM.iloc[0]["Subs"] - rgbM_1.iloc[0]["Subs"]))} </div>', unsafe_allow_html=True)
        st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)        

    col6, col7 = st.columns([6,3])
    with col6:
        st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
        col6a, col6b = st.columns([4,1])
        selected_daily_monthly = col6b.selectbox(
        'Daily',
        ('Daily', 'Monthly'), label_visibility="hidden")

        col6a.subheader(f"Trend {selected_daily_monthly} Revenue")

        if(selected_daily_monthly == 'Daily'):
            lchart = px.line(trend_daily_rev, line_shape="spline", color_discrete_sequence= px.colors.qualitative.Plotly, markers=True)
            lchart.update_layout(autosize=True, legend_title=None, yaxis_title='Revenue', legend=dict(
                orientation = "h",
                xanchor = "center",
                x = 0.5,
                y = -0.2,
                entrywidth=40
            ))
            lchart.add_traces(go.Scatter(x=trend_daily_rev_M_1['Date'], y=trend_daily_rev_M_1['Rev_sum'], name='M-1', line_shape="spline", mode='markers+lines'))
            lchart.add_traces(go.Scatter(x=trend_daily_rev_Y_1['Date'], y=trend_daily_rev_Y_1['Rev_sum'], name='Y-1', line_shape="spline", mode='markers+lines'))
            lchart.update_xaxes(dtick=1)
            lchart.update_traces(hovertemplate='Date: %{x}'+'<br>Rev: %{y}')
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
            lchart.update_traces(hovertemplate='Month: %{x}'+'<br>Rev: %{y}')
            lchart

    with col7:
        st.subheader("By Service")
        st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
        st.plotly_chart(serviceChart, use_container_width=True)

    col8, col9, col10 = st.columns([11,12,9])
    with col8:
        st.subheader("By Cluster")
        st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
        st.plotly_chart(clusterChart, use_container_width=True)

    with col9:
        st.subheader("Top 5 L4 Contributor")
        st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
        if(today_r4_data.empty):
            st.write("Data not updated until selected date")
        else:
            st.dataframe(top_5, use_container_width=True)

    with col10:
        st.subheader("Outlet Digital Aktif & Rev")
        st.write("""<div class='PortMaker' style='margin:0px;'/>""", unsafe_allow_html=True)
        st.dataframe(outlet, use_container_width=True, column_order=['Outlet', '%', 'Rev(M)'])

createUI()