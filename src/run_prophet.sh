#!/bin/bash

# Set the Python script path
PY_SCRIPT="s3://my-sales-data-storage/code/Prophet_model_script.py"

# Install dependencies
sudo pip install pandas fbprophet==0.6 pystan==2.19.1.1

# Run the Python script
spark-submit --master yarn --deploy-mode cluster $PY_SCRIPT
