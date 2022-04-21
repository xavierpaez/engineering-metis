from pickle import TRUE
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import psycopg2
from sqlalchemy import create_engine
import altair as alt
# Streamlit Config
st.set_page_config(page_title="IRS Form 990", layout="wide")

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


st.write(
    '''## IRS Form 990 Dashboard''')

col1, col2 = st.columns(2)
with col1:
    option = st.selectbox(
        'Please select tax year',
        ('2017', '2016', '2015'))

selected_table = 'irs_{}'.format(option)
df = pd.read_sql('select * from {}'.format(selected_table), conn)

# Display Top 10 Non Profits by Revenue
top_10 = df.sort_values('revenue', ascending=False).head(10)
top_10 = top_10[['name', 'revenue']]
bar_chart = alt.Chart(top_10).mark_bar().encode(
    y=alt.Y('revenue'),
    x=alt.X('name:N', sort='-y'),
    tooltip='revenue:N'
).properties(height=500)

# Display States with more Organizations
top_states_df = df['state'].value_counts().reset_index().rename(
    columns={'index': 'state', 'state': 'count'}).head(10)

state_bar_chart = alt.Chart(top_states_df).mark_bar().encode(
    y=alt.Y('count'),
    x=alt.X('state:N', sort='-y'),
    tooltip='count:N'
).properties(height=500)

col1, col2 = st.columns(2)
with col1:
    col1.subheader('Top 10 Organization by Revenue')
    col1.altair_chart(bar_chart, use_container_width=True)

    col1.subheader('Top States by Organizations Count')
    col1.altair_chart(state_bar_chart, use_container_width=True)

# United States Map
states = alt.topo_feature(
    'https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json', feature='states')

variable_list = ['count']

# Display Hospital VS Non Hospital Organizations Pie Chart
col2.subheader('Hospital VS Non Hospital Organizations')
serie = df['is_hospital'].value_counts().reset_index().rename(
    columns={'index': 'is_hospital', 'is_hospital': 'value'})
is_hospital_chart = alt.Chart(serie).mark_arc().encode(
    theta=alt.Theta(field="value", type="quantitative"),
    color=alt.Color(field="is_hospital", type="nominal"),
    tooltip='value:N'
)
col2.altair_chart(is_hospital_chart, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
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

# print(serie.dtype)
