import boto3
import os
import sys
from dotenv import load_dotenv,find_dotenv, set_key
import traceback
from botocore.exceptions import ClientError
import argparse
import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO,
    filename="logs/s3.log",
    filemode="a"
)

print(find_dotenv())
load_dotenv(find_dotenv())

def create_s3(bucket_name,save_model):
    """Create a S3 bucket using the AWS account from .env file. Constrain S3 to a region. 

    Args:
        bucket_name (str): Bucket to create

    Returns:
        bool: True if the S3 was created
    """
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
        
        # Save name of the bucket inside .env variable
        if save_model:
            a = set_key(dotenv_path=find_dotenv(),key_to_set="BUCKET_MODEL",value_to_set=str(bucket_name))
            if a[0]:
                logging.info(f"{a[1]}={a[2]}")
            else:
                logging.error("env not found.")
    except ClientError as e:
        logging.error(traceback.format_exc())
        return False
    return True

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bucket_name", type=str, help="Name of the S3 bucket that will be created"
    )
    
    parser.add_argument(
        "--model_bucket", action="store_true", help="Name of the S3 bucket is saved in the .env file as BUCKET_MODEL"
    )

    args = parser.parse_args()

    create_s3(args.bucket_name,args.model_bucket)