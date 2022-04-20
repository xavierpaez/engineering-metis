from google.cloud import bigquery
import os
from sqlalchemy import create_engine

# Create a Google Cloud account and provide authentication credentials to your application
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/xavierpaez/Downloads/onyx-day-170318-bb177fa52b9d.json"

irs_data_years = ['2017', '2016', '2015']


def irs_data_fetch(client):
    dataframe_collection = {}
    for year in irs_data_years:
        query_string = """
        SELECT
            irsein.name AS name,
            irsein.state AS state,
            irsein.city AS city,
            irsein.ein as EIN,
            irs990.totrevenue AS revenue,
            irs990.totcntrbgfts as contributions,
            irs990.totfuncexpns as total_expenses,
            irs990.totprgmrevnue as program_services,
            irs990.noemplyeesw3cnt AS employees,
            irs990.noindiv100kcnt AS employees_over_100k,
            irs990.compnsatncurrofcr AS officers_comp,
            irs990.operatehosptlcd AS is_hospital,
            irs990.operateschools170cd as is_school,
            irs990.politicalactvtscd as political_activities,
            irs990.lbbyingactvtscd as lobbying_activities,
            irs990.frgnrevexpnscd as foreing_activities
            FROM
                `bigquery-public-data.irs_990.irs_990_ein` AS irsein
            JOIN
                `bigquery-public-data.irs_990.irs_990_{}` AS irs990
            USING (ein)
            ORDER BY
            revenue DESC
        """.format(year)
        try:
            df = (
                client.query(query_string)
                .result()
                .to_dataframe(
                    create_bqstorage_client=True,
                )
            )
            dataframe_collection[year] = df
        except Exception as e:
            print('Unable to retrieve data for year {}'.format(year))
            print(e)

    return dataframe_collection


def dataframe_collection_to_sql(db_engine, df_collection):
    try:
        print(db_engine)
        for year in irs_data_years:
            df_collection[year].to_sql('irs_{}'.format(year), con=db_engine)
    except Exception as e:
        print("Unable to save the data")
        print(e)


def init_db_connection():
    db_string = "postgresql://postgres:083019@localhost/irs_data"
    return create_engine(db_string, echo=False)


def main():
    client = bigquery.Client()
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        print("Connecting to database and create engine...")
        db_engine = init_db_connection()
        print("Pulling IRS Form 990 from Big Query...")
        data_dfs = irs_data_fetch(client)
        print("Saving data in database...")
        dataframe_collection_to_sql(db_engine, data_dfs)
    else:
        print("Unable to run script - GOOGLE_APPLICATION_CREDENTIALS - not defined.")


main()
