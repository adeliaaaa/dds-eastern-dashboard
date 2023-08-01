import plotly.express as px
import pandas as pd
import MySQLdb
import streamlit as st
import datetime
import base64
import warnings

# ----------------------------------------------------------- CONST ----------------------------------------------------------
PIE_COLOR = px.colors.sequential.Burgyl
TARGET_REVENUE_EASTERN = 46671504423.89
TARGET_REVENUE_DAILY_EASTERN = 1555716814.13

IMAGE_DOWN = base64.b64encode(open('./assets/down.png', 'rb').read()).decode('utf-8')
IMAGE_UP = base64.b64encode(open('./assets/up.png', 'rb').read()).decode('utf-8')

# --------------------------------------------------------- DATABASE ---------------------------------------------------------
@st.cache_data
def load_data(type):

    connection = MySQLdb.connect(
        host= st.secrets["HOST_DB"],
        user= st.secrets["USERNAME_DB"],
        passwd= st.secrets["PASSWORD_DB"],
        db= st.secrets["DATABASE_DB"],
        autocommit = True,
        ssl      = {
            "ca": ".\cacert.pem"
        }
    )

    db_cursor = connection.cursor()
    # db_cursor.execute('SET workload = OLAP')
    db_cursor.execute('SELECT rev_date, cluster, rev_sum, month, date, divisi FROM digital_2022 WHERE reg = "EASTERN JABOTABEK"')
    table_rows = db_cursor.fetchall()
    raw_data22 = pd.DataFrame(table_rows)

    db_cursor.execute('SELECT rev_date, cluster, rev_sum, month, date, divisi FROM digital_2023 WHERE reg = "EASTERN JABOTABEK"')
    table_rows = db_cursor.fetchall()
    raw_data23 = pd.DataFrame(table_rows)

    db_cursor.execute('select rev_date from digital_2023 order by ABS(month) desc, ABS(date) desc limit 1')
    table_rows = db_cursor.fetchall()
    max_date_data = pd.DataFrame(table_rows)
    max_date_data = datetime.datetime.strptime(max_date_data[0][0], "%d/%m/%Y")

    if(type == 'All'):
        db_cursor.execute('SELECT bulan, subs FROM rgb_all WHERE reg="06.Eastern Jabotabek"')
        table_rows = db_cursor.fetchall()
        rgb_all = pd.DataFrame(table_rows)
    else:
        db_cursor.execute('SELECT bulan, subs, divisi FROM rgb_service WHERE reg="06.Eastern Jabotabek"')
        table_rows = db_cursor.fetchall()
        rgb_all = pd.DataFrame(table_rows)

    db_cursor.execute('SELECT service, rev_sum, month, day, divisi FROM l4 WHERE regional="EASTERN JABOTABEK"')
    table_rows = db_cursor.fetchall()
    l4 = pd.DataFrame(table_rows)

    db_cursor.execute('SELECT event_date, l4, rev_sum FROM l4_2022')
    table_rows = db_cursor.fetchall()
    l4_2022 = pd.DataFrame(table_rows)

    db_cursor.execute("SELECT reg, COUNT(reg) FROM `raw_outlet` WHERE reg='KOTA BEKASI' or reg='DEPOK' or reg='BOGOR' or reg='SUKABUMI' or reg='BEKASI' or reg='KARAWANG PURWAKARTA' GROUP by reg")
    table_rows = db_cursor.fetchall()
    raw_outlet = pd.DataFrame(table_rows)

    db_cursor.execute("SELECT cluster, count(rev_sum), sum(rev_sum) FROM `outlet` WHERE trx_sum >= 2 and regional='EASTERN JABOTABEK' group by cluster;")
    table_rows = db_cursor.fetchall()
    outlet_data = pd.DataFrame(table_rows)

    return max_date_data, raw_data22, raw_data23, rgb_all, l4, l4_2022, raw_outlet, outlet_data

# ---------------------------------------------------------- HELPER ----------------------------------------------------------
def color_negative_to_red(val):
    if(val[0] == '-'):
        color = 'red'
        return 'color: %s' % color
    # color = 'red' if val[0] == '-' else 'black'

def regexFromDate2022(day, month):
    if (day < 10):
        reg_day = f'(?:0[1-{day}])/'
    elif(day < 20):
        days = day-10
        reg_day = f'(?:0[1-9]|1[0-{days}])/'
    elif(day < 30):
        days = day-20
        reg_day = f'(?:0[1-9]|1[0-9]|2[0-{days}])/'
    elif(day < 33):
        days = day-30
        reg_day = f'(?:0[1-9]|1[0-9]|2[0-9]|3[0-{days}])/'

    if(month < 10):
        reg_month = f'(?:0[{month}])/2022'
    elif(month < 13):
        months = month - 10
        reg_month = f'(?:0[1-9]|1[{months}])/2022'
    regex1 = reg_day + reg_month

    if(month != 1):
        if(month < 10):
            months = month - 1
            regex2 = f'(?:0[1-9]|1[0-9]|2[0-9]|3[0-1])/(?:0[1-{months}])/2022'
        else:
            months = month - 1 - 12
            regex2 = f'(?:0[1-9]|1[0-9]|2[0-9]|3[0-1])/(?:0[1-9]|1[{months}])/2022'
        final_regex = '(' + regex1 + ')' + '|' + '(' + regex2 + ')'
        return final_regex
    else:
        return regex1

def regexFromDate2022OneMonth(day, month):
    if (day < 10):
        reg_day = f'(?:0[1-{day}])/'
    elif(day < 20):
        days = day-10
        reg_day = f'(?:0[1-9]|1[0-{days}])/'
    elif(day < 30):
        days = day-20
        reg_day = f'(?:0[1-9]|1[0-9]|2[0-{days}])/'
    elif(day < 33):
        days = day-30
        reg_day = f'(?:0[1-9]|1[0-9]|2[0-9]|3[0-{days}])/'

    if(month < 10):
        reg_month = f'(?:0[{month}])/2022'
    elif(month < 13):
        months = month - 10
        reg_month = f'(?:1[{months}])/2022'
    regex1 = reg_day + reg_month

    return regex1

def addCustomStyle():
    warnings.filterwarnings("ignore", 'This pattern has match groups')
    
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

        .css-ffhzg2 .eastern-color{
            color: white;
            margin-left: 2px;
        }

        .css-fg4pbf .eastern-color{
            color: black;
            margin-left: 2px;
        }


        # .stDataFrame {
        #     width:100%;
        # }

    </style>
    """,
        unsafe_allow_html=True,
    )

def serviceToDigitalNameFormat(service):

    if(service == 'GAMES MARKETPLACE'):
        new_service = 'Games Marketplace'
    elif(service == 'VIDEO'):
        new_service = 'Video'
    elif(service == 'DIGITAL MUSIC'):
        new_service = 'Digital Music'
    elif(service == 'VAS CONTENT'):
        new_service = 'VAS Content'
    elif(service == 'DIGITAL BANKING'):
        new_service = 'Digital Banking'
    return new_service