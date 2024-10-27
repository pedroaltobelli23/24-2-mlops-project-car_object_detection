import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

bucket_name = os.getenv("AWS_BUCKET_NAME")

# List objects in the specified S3 bucket
response = s3.list_objects_v2(Bucket=bucket_name)

# Check if the bucket is empty
if 'Contents' not in response:
    print(f"The bucket '{bucket_name}' is empty.")
else:
    # Get the list of keys in the bucket
    keys = [item['Key'] for item in response['Contents']]
    
    print(keys)
