import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os
from prefect import flow, task
from prefect.tasks import task_input_hash
import argparse
from datetime import timedelta
from prefect_sqlalchemy import SqlAlchemyConnector

@task(log_prints=True, retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(csv_url):

    #for pandas to be able to open the file
    if csv_url.endswith('.csv.gz'):
        csv_name='yellow_tripdata_2021-01.csv'
    else:
        csv_name = 'output.csv'

    #download the csv
    os.system(f"wget {csv_url} -O {csv_name}")

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, compression='gzip')
    df=next(df_iter)
    df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)

    return df

@task(log_prints=True)
def transform_data(df):
    print(f"pre:missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count']!=0]
    print(f"post:missing passenger count: {df['passenger_count'].isin([0]).sum()}") 
    return df

@task(log_prints=True, retries=3)
def ingest_data(table_name, df):

    connection_block= SqlAlchemyConnector.load("connector")
    with connection_block.get_connection(begin=False) as engine:

        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        df.to_sql(name=table_name, con=engine, if_exists='append')

@flow (name="Subflow", log_prints=True)
def log_subflow(table_name:str):
    print ("Logging Subflow for: {table_name}")

@flow (name="Ingest Flow")
def main_flow(table_name:str):

    table_name="yellow_taxi_trips"
    csv_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
    log_subflow(table_name)
    raw_data = extract_data(csv_url)
    data = transform_data(raw_data)
    ingest_data (table_name, data)

if __name__ == "__main__":
    main_flow("yellow_taxi_trips")
