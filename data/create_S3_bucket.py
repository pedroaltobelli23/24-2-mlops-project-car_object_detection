import boto3
import os
import sys
from dotenv import load_dotenv
import traceback
import logging
from botocore.exceptions import ClientError

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-18s %(name)-8s %(levelname)-8s %(message)s",
    datefmt="%y-%m-%d %H:%M",
    filename="logs/s3.log",
    filemode="a",
)

def create_s3(bucket_name):
    """Create a S3 bucket using the AWS account from .env file. Constrain S3 to a region. 

    Args:
        bucket_name (str): Bucket to create

    Returns:
        _type_: _description_
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
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__=="__main__":
    user_input = str(sys.argv[1])
    create_s3(user_input)