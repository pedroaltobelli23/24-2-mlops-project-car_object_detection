import boto3
import os
import sys
from dotenv import load_dotenv
import traceback
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-18s %(name)-8s %(levelname)-8s %(message)s",
    datefmt="%y-%m-%d %H:%M",
    filename="logs/bucket.log",
    filemode="a",
)

def create_s3(bucket_name):
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )

        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": os.getenv("AWS_REGION")},
        )

        logging.info(f"Bucket {bucket_name} created")
    except Exception as e:
        logging.error(traceback.format_exc())
        
    return None

if __name__=="__main__":
    user_input = str(sys.argv[1])
    create_s3(user_input)