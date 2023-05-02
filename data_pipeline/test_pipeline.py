import unittest
from pyspark.sql import SparkSession
from pipeline.transform import Transform

class TransformTest (unittest.TestCase):
    def test_transform_should_replace_null_value (self):
        spark = SparkSession.builder\
        .appName("testing app")\
        .enableHiveSupport().getOrCreate()

        df=spark.read\
        .option("header", "true")\
        .option("inferSchema","true")\
        .csv("test/test_file.csv")

        df.show()

        transform_process = Transform(spark)
        transformed_df = transform_process.transform_data(df)
        transformed_df.show()

        country = transformed_df.filter("age='1'").select("country").collect()[0].country

        print ("Country is " + str(country))

        self.assertEqual("Unknown", str(country))

if __name__=='__main__':
    unittest.main()
