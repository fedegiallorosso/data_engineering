#Authenticate the gcloud CLI with the google account you used for GCP
gcloud auth login
#Exporting the model from BQ to GCS
bq --project_id noble-return-383707 extract -m trips_data_all.tip_model gs://taxi_ml_model_noble-return-383707/tip_model
#Create a new folder 
mkdir /tmp/model
#Copy the model to local folder
gsutil cp -r gs://taxi_ml_model_noble-return-383707/tip_model /tmp/model
#Create a serving directory
mkdir -p serving_dir/tip_model/1
#Copy the content in this directory
cp -r /tmp/model/tip_model/* serving_dir/tip_model/1
#Pull the tensorflow serving image
docker pull tensorflow/serving
#Run the image
docker run -p 8501:8501 --mount type=bind,source=/home/federico/code/fedegiallorosso/big_data/data_engineering_zoomcamp/week3/serving_dir/tip_model,target=/models/tip_model -e MODEL_NAME=tip_model -t tensorflow/serving &
#Send HTTP request to web APIs
http://localhost:8501/v1/models/tip_model
#Get the prediction
{"instances":[{"passenger_count":1,"trip_distance":22.2,"PULocationID":"193","DOLocationID":"264", "payment_type":"1","fare_amount":20.4,"tolls_amount":0.0}]} 