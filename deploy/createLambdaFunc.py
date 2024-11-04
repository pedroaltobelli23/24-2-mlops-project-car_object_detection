import boto3
import os
from dotenv import load_dotenv
import argparse

def create_lambda_function(image_uri):    
    function_name="lambda-project-pedroatp"
    load_dotenv()
    lambda_role_arn = os.getenv("AWS_LAMBDA_ROLE_ARN")
    # Create a Boto3 client for AWS Lambda
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    # Delete AWS Lambda that already exists
    try:
        response = lambda_client.delete_function(FunctionName=function_name)
    except Exception as e:
        print(f"Error deleting function: {str(e)}")

    response = lambda_client.create_function(
        FunctionName=function_name,
        PackageType="Image",
        Code={"ImageUri": image_uri},
        Role=lambda_role_arn,
        Timeout=900,
        MemorySize=512,
        Environment = {
            "Variables": {
                "BUCKET_MODEL": os.getenv("BUCKET_MODEL"),
                "ACCESS_KEY_ID":os.getenv("AWS_ACCESS_KEY_ID"),
                "SECRET_ACCESS_KEY":os.getenv("AWS_SECRET_ACCESS_KEY"),
                "REGION":os.getenv("AWS_REGION"),
            }
        }
    )

    print("Lambda function created successfully:")
    print(f"Function Name: {response['FunctionName']}")
    print(f"Function ARN: {response['FunctionArn']}")
    
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--image_uri", type=str, help="ECR uri"
    )

    args = parser.parse_args()
    image_uri = "ID.dkr.ecr.REGION.amazonaws.com/mlops-pedroatp-projeto3:latest"

    create_lambda_function(image_uri=args.image_uri)