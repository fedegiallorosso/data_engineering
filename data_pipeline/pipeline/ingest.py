import logging.config

class Ingest:
    logging.config.fileConfig("pipeline/resources/configs/logging.conf")

    def __init__(self,spark):
        self.spark=spark

    def ingest_data(self):
        logger = logging.getLogger("Ingest")
        logger.info("Ingesting from csv")
        course_df=self.spark.read.option("header", True).csv("pipeline/retailstore.csv")
        logger.info('DataFrame created')
        logger.warning('Dataframe created with warning')
        return course_df
