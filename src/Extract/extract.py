import boto3
from botocore import UNSIGNED
from botocore.client import Config

# Create a boto3 client for S3
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

# Specify the bucket name
bucket_name = "d2b-internal-assessment-bucket"

# List of files to download
files = ["orders.csv", "reviews.csv", "shipment_deliveries.csv"]

# Download each file
for file in files:
    s3.download_file(bucket_name, f"orders_data/{file}", file)
