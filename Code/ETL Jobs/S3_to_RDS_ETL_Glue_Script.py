import boto3
from awsglue.transforms import *
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
from botocore.exceptions import ClientError

# Create a GlueContext
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Get Username and password for RDS database
def get_secret():
    secret_name = "prod/rds"
    region_name = "ap-south-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return eval(secret)

# Read data from S3
s3_path = "s3://my-sales-data-storage/Sales.csv"
dataframe = spark.read.csv(s3_path, header=True, inferSchema=True)

# Transform data if needed
# You can apply any necessary data transformations using Spark DataFrame API

# Write data to RDS
database_name = "ProductSales"
table_name = "SalesData"
jdbc_url = "jdbc:mysql://sales.cusdzyvxlo3h.ap-south-1.rds.amazonaws.com:3306/ProductSales"
secret = get_secret()
jdbc_properties = {
    "user": secret["username"],
    "password": secret["password"],
    "driver": "com.mysql.cj.jdbc.Driver"
}

dataframe.write \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", f"{database_name}.{table_name}") \
    .options(**jdbc_properties) \
    .mode("append") \
    .save()

# Commit the job
#glueContext.commit()
