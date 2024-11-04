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

load_dotenv(find_dotenv())

def add_model(model_path):
    """Upload model file to S3 bucket. Overwrite any model file in the bucket if exists.

    Args:
        model_path (str): _description_

    Returns:
        bool: True if the model was uploaded, else False
    """
    
    object_name = "model.onnx"
    
    try:
        if model_path.endswith(".onnx"):
            s3 = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION"),
            )
            
            response = s3.upload_file(
                model_path,
                os.getenv("BUCKET_MODEL"),
                object_name,
            )
        else:
            logging.error(f"{model_path} isn't a .onnx (Place-Text) file")
            return False
    except Exception as e:
        logging.error(traceback.format_exc())
        return False
    a = os.getenv("BUCKET_MODEL")
    logging.info(f"Model saved in the bucket {a}")
    return True

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--model_path", type=str, help=".pt file where the model is saved"
    )

    args = parser.parse_args()

    add_model(args.model_path)