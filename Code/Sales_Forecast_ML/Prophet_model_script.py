from pyspark.sql.types import DateType, FloatType, IntegerType, StructField, StructType
from pyspark.sql import SparkSession
from pyspark.context import SparkContext as sc 
from fbprophet import Prophet
import logging
import pandas as pd
from pyspark.sql.functions import current_date

# Create a Spark session
spark = SparkSession.builder.master("yarn").getOrCreate()

# read the training file into a dataframe from S3 bucket
s3_path = "s3://my-sales-data-storage/Sales.csv"
train_schema = StructType([
    StructField('date', DateType()),
    StructField('store', IntegerType()),
    StructField('item', IntegerType()),
    StructField('sales', IntegerType())
])
train = spark.read.csv(s3_path, header=True, schema=train_schema)

# make the dataframe queriable as a temporary view
train.createOrReplaceTempView('train') 


#Retrieve Data for All Store-Item Combinations
sql_statement = '''
  SELECT
    store,
    item,
    CAST(date as date) as ds,
    SUM(sales) as y
  FROM train
  GROUP BY store, item, ds
  ORDER BY store, item, ds
  '''
 # Run SQL statement and cache the result
store_item_history = (
  spark
    .sql( sql_statement )
    .repartition(sc.defaultParallelism, ['store', 'item'])
  ).cache()


#Define Result Schema
result_schema =StructType([
  StructField('ds',DateType()),
  StructField('store',IntegerType()),
  StructField('item',IntegerType()),
  StructField('y',FloatType()),
  StructField('yhat',FloatType()),
  StructField('yhat_upper',FloatType()),
  StructField('yhat_lower',FloatType())
  ])

#Define Function to Train Model & Generate Forecast

def forecast_store_item( history_pd: pd.DataFrame ) -> pd.DataFrame:
  
  # TRAIN MODEL AS BEFORE
  # --------------------------------------
  # remove missing values (more likely at day-store-item level)
  history_pd = history_pd.dropna()
  
  # configure the model
  model = Prophet(
    interval_width=0.95,
    growth='linear',
    daily_seasonality=False,
    weekly_seasonality=True,
    yearly_seasonality=True,
    seasonality_mode='multiplicative'
    )
  
  # train the model
  model.fit( history_pd )
  # --------------------------------------
  
  # BUILD FORECAST AS BEFORE
  # --------------------------------------
  # make predictions
  future_pd = model.make_future_dataframe(
    periods=90, 
    freq='d', 
    include_history=True
    )
  forecast_pd = model.predict( future_pd )  
  # --------------------------------------
  
  # ASSEMBLE EXPECTED RESULT SET
  # --------------------------------------
  # get relevant fields from forecast
  f_pd = forecast_pd[ ['ds','yhat', 'yhat_upper', 'yhat_lower'] ].set_index('ds')
  
  # get relevant fields from history
  h_pd = history_pd[['ds','store','item','y']].set_index('ds')
  
  # join history and forecast
  results_pd = f_pd.join( h_pd, how='left' )
  results_pd.reset_index(level=0, inplace=True)
  
  # get store & item from incoming data set
  results_pd['store'] = history_pd['store'].iloc[0]
  results_pd['item'] = history_pd['item'].iloc[0]
  # --------------------------------------
  
  # return expected dataset
  return results_pd[ ['ds', 'store', 'item', 'y', 'yhat', 'yhat_upper', 'yhat_lower'] ]  

# Apply Forecast Function to Each Store-Item Combination
results = (
  store_item_history
    .groupBy('store', 'item')
      .applyInPandas(forecast_store_item, schema=result_schema)
    .withColumn('training_date', current_date() )
    )
 
results.createOrReplaceTempView('new_forecasts')


# Write the predictions to Redshift
jdbc_url = "jdbc:redshift://default-workgroup.572561648008.ap-south-1.redshift-serverless.amazonaws.com:5439/sales-forecast"
jdbc_properties = {
    "user": "admin",
    "password": "Input Your Password",
    "driver": "com.amazon.redshift.jdbc.Driver"
}
results.write \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "predictions") \
    .options(**jdbc_properties) \
    .mode("append") \
    .save()
# Stop the Spark session
spark.stop()