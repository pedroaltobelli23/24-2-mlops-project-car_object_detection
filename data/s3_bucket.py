import boto3
import os
import sys
from dotenv import load_dotenv, find_dotenv, set_key
import traceback
from botocore.exceptions import ClientError
import argparse
import logging


class S3_Bucket:
    def __init__(self, access_key_id, secret_access_key, region):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region = region
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region,
        )

    def create_S3_bucket(self, bucket_name, type="model"):
        try:
            self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": self.region},
            )

            logging.info(f"{type} Bucket {bucket_name} created")

            if type == "model":
                a = set_key(
                    dotenv_path=find_dotenv(),
                    key_to_set="BUCKET_MODEL",
                    value_to_set=str(bucket_name),
                )
            elif type == "dataset":
                a = set_key(
                    dotenv_path=find_dotenv(),
                    key_to_set="BUCKET_DATASET",
                    value_to_set=str(bucket_name),
                )
            else:
                logging.error(f"Type {type} don't exist.")

            if a[0]:
                logging.info(f"{a[1]}={a[2]}")
            else:
                logging.error("env not found.")
        except ClientError as e:
            logging.error(traceback.format_exc())
            return False
        return True

    def delete_S3_bucket(self, bucket_name):
        try:
            bucket = boto3.resource(
                "s3",
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name=self.region,
            ).Bucket(bucket_name)
            bucket.objects.all().delete()

            self.s3.delete_bucket(Bucket=bucket_name)
            logging.info(f"Bucket {bucket_name} deleted")
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def list_S3_buckets(self):
        try:
            response = self.s3.list_buckets()

            for bucket in response["Buckets"]:
                logging.info(f'  {bucket["Name"]}')
        except ClientError as e:
            logging.error(traceback.format_exc())
            return False
        except Exception as e:
            logging.error(traceback.format_exc())
            return False
        return True

    def add_file_model_S3_bucket(self, bucket_name, file_path, object_name):
        try:
            base, ext = os.path.splitext(object_name)
            if file_path.endswith(ext):
                response = self.s3.upload_file(
                    file_path,
                    bucket_name,
                    object_name,
                )
            else:
                logging.error(f"{file_path} isn't a {ext} file")
                return False

            logging.info(
                f"{file_path} saved in the bucket {bucket_name} as {object_name}"
            )
        except Exception as e:
            logging.error(traceback.format_exc())
            return False
        return True

    def handle_arguments(self, args):
        if any(vars(args).values()):
            if args.file_path:
                res = self.add_file_model_S3_bucket(
                    os.getenv("BUCKET_MODEL"), args.file_path, args.object_name
                )
                if not res:
                    logging.error(f"{args.bucket_model} not created")
                return

            if args.bucket_model:
                res = self.create_S3_bucket(args.bucket_model)
                if not res:
                    logging.error(f"{args.bucket_model} not created")
                    return

            if args.bucket_dataset:
                res = self.create_S3_bucket(args.bucket_dataset, type="dataset")
                if not res:
                    logging.error(f"{args.bucket_dataset} not created")
                    return

            if args.list_buckets:
                res = self.list_S3_buckets()
                if not res:
                    logging.error(
                        "Error while trying to list all s3 buckets from account"
                    )
                    return

            if args.delete_bucket:
                res = self.delete_S3_bucket(args.delete_bucket)
                if not res:
                    logging.error(f"Error while trying to delete {args.delete_bucket}")
                    return
        else:
            logging.info("No arguments provided")
        return


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=logging.INFO,
        filename="logs/s3.log",
        filemode="a",
    )

    load_dotenv(find_dotenv())

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--bucket_model",
        type=str,
        help="Name of the bucket to be created and saved as model bucket.",
    )

    parser.add_argument(
        "--bucket_dataset",
        type=str,
        help="Name of the bucket to be created and saved as dataset bucket.",
    )

    parser.add_argument(
        "--delete_bucket", type=str, help="Name of the bucket to be deleted."
    )

    parser.add_argument(
        "--list_buckets", action="store_true", help="List all buckets in the account."
    )

    parser.add_argument("--file_path", type=str, help="Add file to model bucket.")

    parser.add_argument(
        "--object_name",
        type=str,
        help="Object name that will be saved inside the model bucket",
        default="model.onnx",
    )

    bucket_module = S3_Bucket(
        os.getenv("AWS_ACCESS_KEY_ID"),
        os.getenv("AWS_SECRET_ACCESS_KEY"),
        os.getenv("AWS_REGION"),
    )

    args = parser.parse_args()

    bucket_module.handle_arguments(args)
