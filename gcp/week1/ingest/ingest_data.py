import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
#import os

def main(params):
    user=params.user
    password=params.password
    host=params.host
    port=params.port
    db=params.db
    #url=params.url
    table_name_tripdata=params.table_name_tripdata
    table_name_zone=params.table_name_zone
    csv_name='yellow_tripdata_2021-01.csv'

    #download the csv
    #os.system(f"wget {url} -O {csv_name}")

    engine=create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_zones= pd.read_csv("zone_lookup.csv")
    df_zones.to_sql(name=table_name_zone, con=engine, if_exists='replace')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, nrows=1369765)

    df=next(df_iter)

    df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name_tripdata, con=engine, if_exists='replace')

    df.to_sql(name=table_name_tripdata, con=engine, if_exists='append')

    while True:

        t_start=time()

        df=next(df_iter)

        df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name_tripdata, con=engine, if_exists='append')

        t_end=time()

        print ('inserted another chunk..., took %.3f second' % (t_end - t_start))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # user, password, host, port, database name, table name, url of the csv
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name_tripdata', help='name of the table where we will write the results to')
    parser.add_argument('--table_name_zone', help='name of the table describing zones')
    #parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)
