# for table styling
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

# if st.checkbox('Show raw data'):
#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader('Raw l4_2022')
#         st.write(l4_2022)
    # with col2:
    #     st.subheader('Raw data23')
    #     st.write(raw_data23)
    # groupped_by = raw_data22.groupby('Cluster')

    # st.write(groupped_by.first())
    # st.subheader('Data Bogor')
    # st.write(groupped_by.get_group('BOGOR'))

# import streamlit as st
# import pandas as pd
# import numpy as np
# from datetime import date
# import datetime


# st.set_page_config(layout="wide")
# st.title('Revenue')

# from dotenv import load_dotenv
# load_dotenv()
# import os
# import MySQLdb

# @st.cache_data
# def load_data():
#     connection = MySQLdb.connect(
#         host= 'localhost',
#         user='root',
#         passwd= '',
#         db= 'ddseastern',
#         autocommit = True
#     )



#     db_cursor = connection.cursor()
#     # db_cursor.execute('SET workload = OLAP')
#     db_cursor.execute('SELECT rev_date, cluster, rev_sum, month, date FROM digital_2022 WHERE reg = "EASTERN JABOTABEK"')
#     table_rows = db_cursor.fetchall()
#     raw_data = pd.DataFrame(table_rows)
#     # raw_data = pd.DataFrame()

#     db_cursor.execute('SELECT cluster, sum(rev_sum) FROM digital_2022 WHERE reg = "EASTERN JABOTABEK" GROUP BY cluster')
#     table_rows = db_cursor.fetchall()
#     df1 = pd.DataFrame(table_rows)

#     df1.columns = ['cluster', 'digital']

#     db_cursor.execute('select rev_date from digital_2023 order by rev_date desc limit 1')
#     table_rows = db_cursor.fetchall()
#     df2 = pd.DataFrame(table_rows)

#     db_cursor.execute('SELECT cluster, sum(rev_sum) FROM digital_2022 WHERE reg = "EASTERN JABOTABEK" AND divisi = "Games Marketplace" GROUP BY cluster')
#     table_rows = db_cursor.fetchall()
#     df_games_marketplace = pd.DataFrame(table_rows)
#     df_games_marketplace.columns = ['cluster', 'Games']

#     db_cursor.execute('SELECT cluster, sum(rev_sum) FROM digital_2022 WHERE reg = "EASTERN JABOTABEK" AND divisi = "Video" GROUP BY cluster')
#     table_rows = db_cursor.fetchall()
#     df_video = pd.DataFrame(table_rows)
#     df_video.columns = ['cluster', 'Video']

    
#     result2 = datetime.datetime.strptime(df2[0][0], "%d/%m/%Y").strftime("%d %B %Y")

#     result = pd.merge(df1, df_games_marketplace, on='cluster', how='left')
#     result = pd.merge(result, df_video, on='cluster', how='left')
#     return result, result2, raw_data


# data, df2, raw_data = load_data()
# c1, c2 = st.columns(2)

# with c1:
#     with st.container():
#         st.write("### Today")
#         today = date.today()
#         today = today.strftime("%d %B %Y")
#         # st.write(today)
#         st.write(f'<p style="font-size:23px; color:grey;">{today}</p>', unsafe_allow_html=True)


# with c2:
#     with st.container():
#         st.write("### Latest Data Date")
#         st.write(f'<p style="font-size:23px; color:grey;">{df2}</p>', unsafe_allow_html=True)

# st.markdown("""---""")


# data = data.set_index('cluster')
# data['digital'] = (data['digital'].astype(float) / 1000000000).map('{:.2f}'.format)

# data['Games'] = (data['Games'].astype(float) / 1000000000).map('{:.2f}'.format)

# data['Video'] = (data['Video'].astype(float) / 1000000000).map('{:.2f}'.format)

# st.write(data)
# raw_data.columns = ['Rev_Date', 'Cluster', 'Rev_sum', 'Month', 'Date']
# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(raw_data)
#     groupped_by = raw_data.groupby('Cluster')

#     # st.write(groupped_by.first())
#     st.subheader('Data Bogor')
#     st.write(groupped_by.get_group('BOGOR'))

# # st.subheader('Number of pickups by hour')
# # hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# # st.bar_chart(hist_values)

# # # Some number in the range 0-23
# # hour_to_filter = st.slider('hour', 0, 23, 17)
# # filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# # st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# # st.map(filtered_data)