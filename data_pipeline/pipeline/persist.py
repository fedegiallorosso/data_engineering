import logging.config
import psycopg2

class Persist:
    logging.config.fileConfig("pipeline/resources/configs/logging.conf")

    def __init__(self, spark):
        self.spark = spark

    def persist_data(self, df):
        try:
            logger = logging.getLogger("Persist")
            logger.info ("Persisting")
            df.write.option("header","true").csv("transformed_retailstore.csv")

        except Exception as exp:
            logger.error ("An error occurred while persisting data > " + str(exp))
            #send an email notification
            raise Exception ("HDFS directory already exists")
            #sys.exit(1)

    def insert_into_pg(self, transformed_df):
        connection = psycopg2.connect(user='postgres', password='Fededata93!', host='localhost', database='postgres')
        cursor = connection.cursor()

        transformed_df = transformed_df.toPandas()

        cursor.execute("DROP TABLE IF EXISTS ultimo;")

        sql = f'''CREATE TABLE ultimo(
                {transformed_df.columns[0]} SMALLINT NOT NULL,
                {transformed_df.columns[1]} DECIMAL(20,2) NOT NULL,
                {transformed_df.columns[2]} CHAR(12) NOT NULL,
                {transformed_df.columns[3]} CHAR(30) NOT NULL,
                {transformed_df.columns[4]} CHAR(11) NOT NULL
                )'''
        cursor.execute(sql);

        for i in transformed_df.index:
            cols = ','.join(list(transformed_df.columns))
            vals = [transformed_df.at[i, col] for col in list(transformed_df.columns)]
            query = f'''INSERT INTO ultimo({cols}) VALUES ({vals[0]},{vals[1]},'{vals[2]}','{vals[3]}','{vals[4]}')'''
            cursor.execute(query);

        logging.info("Transformed data loaded to PostgreQSL")

        cursor.close()
        connection.commit()
