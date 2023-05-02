from pyspark.sql import SparkSession
from pipeline.ingest import Ingest
from pipeline.persist import Persist
from pipeline.transform import Transform
import logging.config
import sys

class Pipeline:
    logging.config.fileConfig("pipeline/resources/configs/logging.conf")

    def create_spark_session (self):
        self.spark = SparkSession.builder\
            .appName("my first spark app")\
            .enableHiveSupport().getOrCreate()

    def run_pipeline(self):
        try:
            print("Running Pipeline")
            ingest_process = Ingest(self.spark)
            df=ingest_process.ingest_data()
            df.show()
            transform_process = Transform(self.spark)
            transformed_df=transform_process.transform_data(df)
            transformed_df.show()
            persist_process = Persist(self.spark)
            persist_process.insert_into_pg(transformed_df)
        except Exception as exp:
            logging.error("An error occurred while running the pipeline > " + str(exp))
            #send email notification
            sys.exit(1)
        return

if __name__ == '__main__':
    logging.info("Application started")
    pipeline = Pipeline()
    pipeline.create_spark_session()
    logging.info("Spark Session created")
    pipeline.run_pipeline()
    logging.info("Pipeline executed")
