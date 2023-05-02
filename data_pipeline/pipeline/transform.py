from pyspark.sql.types import IntegerType, FloatType
from pyspark.sql.functions import mean
import logging.config


class Transform:
    logging.config.fileConfig("pipeline/resources/configs/logging.conf")

    def __init__(self, spark):
        self.spark = spark

    def transform_data(self, bankProspectsDF):
        logger = logging.getLogger("Transform")
        logger.info("Transforming")
        logger.warning("Warning in Trasformer")
        # Filter out records with unknown values
        bankProspectsDF1 = bankProspectsDF.filter(bankProspectsDF["country"] != "unknown")

        bankProspectsDF2 = bankProspectsDF1.withColumn("age", bankProspectsDF1["age"].cast(IntegerType())).withColumn(
            "salary", bankProspectsDF1["salary"].cast(FloatType()))

        mean_age_val = bankProspectsDF2.select(mean(bankProspectsDF2['age'])).collect()
        mean_age_val = mean_age_val[0][0]

        mean_salary_val = bankProspectsDF2.select(mean(bankProspectsDF2['salary'])).collect()
        mean_salary_val = mean_salary_val[0][0]

        #now we substitute the null values with mean value
        bankProspectsDF3 = bankProspectsDF2.na.fill(mean_age_val, ["age"])

        bankProspectsDF4 = bankProspectsDF3.na.fill(mean_salary_val, ["salary"])

        return bankProspectsDF4
