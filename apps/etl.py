import time
import os
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import src.load as l
import src.transform as t
import src.extract as e
import src.start_env as s
import findspark
findspark.init("/opt/spark")


def main():
    spark = SparkSession.builder \
        .appName('portafolio.com') \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')\
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    # start_env: Loads the mongodb and postgres databases with the client data before starting the ETL.
    s.start_env()
    # Extract : It retrieves client data from MongoDb and Postgres, and returns it in a single data frame.
    df_customers = e.extract(spark)
    # Transform: Group and filter customer data to be later saved.
    df_customers = t.transform(df_customers, spark)
    # Load: Results are stored in a csv file. /data/output
    l.load(df_customers)
    # To see the jobs by spark ui : time.sleep(10)


if __name__ == "__main__":
    main()
