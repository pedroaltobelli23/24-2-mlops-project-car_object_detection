import boto3
import os
import sys
from dotenv import load_dotenv
import traceback
import logging
from botocore.exceptions import ClientError

load_dotenv()

logging.basicConfig(
    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO,
    filename="logs/s3.log",
    filemode="a"
)

def list_s3():
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )

        response = s3.list_buckets()
        
        for bucket in response['Buckets']:
            logging.info(f'  {bucket["Name"]}')
    except ClientError as e:
        logging.error(traceback.format_exc())
        return False
    except Exception as e:
        logging.error(traceback.format_exc())
        return False
    return True

if __name__=="__main__":
    logging.info("All S3 buckets:")
    list_s3()