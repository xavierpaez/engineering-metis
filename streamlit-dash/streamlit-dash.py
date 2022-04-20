import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import psycopg2
from sqlalchemy import create_engine
import altair as alt

st.write(
    '''## IRS Form 990 Dashboard''')

# Connecting Streamlit to Postgres


def connect():
    conn = None
    try:
        print('Connecting to Postgres Database')
        conn = psycopg2.connect(**st.secrets["postgres"])
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
        st.write('Can not connected to db')
    print("Connection created successfuly")
    return conn


conn = connect()


def print_organization_details(df):
    st.markdown(
        '**{}**'.format(format(df['name'].iloc[0] + ' - ' + df['EIN'].iloc[0])))
    st.write()
    st.write(df['city'].iloc[0] + ', ' + df['state'].iloc[0])
    st.metric('Total Revenue', "{:,}".format(df['revenue'].iloc[0]))
    st.metric('Revenue - Program Services',
              "{:,}".format(df['program_services'].iloc[0]))
    st.metric('Total Contributions', "{:,}".format(
        df['contributions'].iloc[0]))
    st.metric('Employees', "{:,}".format(df['employees'].iloc[0]))
    st.metric('Number individuals greater than $100K,',
              "{:,}".format(df['employees_over_100k'].iloc[0]))


option = st.selectbox(
    'Please select tax year',
    ('2017', '2016', '2015'))

selected_table = 'irs_{}'.format(option)

# Display Top 10 Non Profits by Revenue
df = pd.read_sql('select * from {}'.format(selected_table), conn)
top_10 = df.sort_values('revenue', ascending=False).head(10)

st.subheader('Top 10 Organization by Revenue')
top_10 = top_10[['name', 'revenue']]
bar_chart = alt.Chart(top_10).mark_bar().encode(
    y=alt.Y('revenue', sort='x'),
    x='name'


).properties(height=500)

st.altair_chart(bar_chart, use_container_width=True)

# Organization look up
st.subheader('Organization Look up')
# Streamlit is not very efficient in having a dropdown of that many names
# option = st.selectbox(
#     'Please select organization',
#     df['name'].sort_values())
# st.write(
#     '''#### OR''')
ein = st.text_input('Enter Employee Identification Number (EIN)', '')
if ein != "":
    ein = ein.replace("-", "")
    selected_df = df[df['EIN'] == ein]
    if selected_df.empty:
        st.write("Can't find organization")
    else:
        print_organization_details(selected_df)
