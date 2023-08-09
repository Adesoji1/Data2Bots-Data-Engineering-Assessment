import boto3
from botocore import UNSIGNED
from botocore.client import Config

# Create an S3 client with unsigned requests
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

filename = 'agg_public_holiday.csv'
bucket_name = 'd2b-internal-assessment-bucket'
your_id = 'adesalu8398'  # Replace with your unique ID
object_name = f'analytics_export/{your_id}/agg_public_holiday.csv'

# Upload the file to the S3 bucket
s3.upload_file(filename, bucket_name, object_name)

print(f"Uploaded {filename} to {bucket_name}/{object_name}")
