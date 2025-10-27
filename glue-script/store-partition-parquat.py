import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql.functions import year, month, dayofmonth, to_timestamp

## Get job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

## Load CSV from Glue Catalog
input_path = "s3://superstore-data-2510/raw/Sample - Superstore.csv"

df = spark.read.format("csv") \
    .option("header", "true") \
    .option("quote", '"') \
    .option("escape", '"') \
    .option("multiLine", "true") \
    .load(input_path)

## Convert Order Date to timestamp
df = df.withColumn("OrderDate", to_timestamp("Order Date", "M/d/yyyy"))

## Add year/month/day columns for partitioning
df = df.withColumn("year", year("OrderDate")) \
       .withColumn("month", month("OrderDate")) \
       .withColumn("day", dayofmonth("OrderDate"))

## Write to S3 in Parquet, partitioned by year/month/day with Snappy compression
output_path = "s3://superstore-data-2510/processed/"
df.write.mode("overwrite") \
    .partitionBy("year","month","day") \
    .option("compression","snappy") \
    .parquet(output_path)
    
job.commit()