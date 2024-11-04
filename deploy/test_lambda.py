import boto3
import os
import io
from dotenv import load_dotenv
import json

load_dotenv()

# Create a Boto3 client for AWS Lambda
lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

function_name = "lambda-project-pedroatp"

try:
    # Invoke the function
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
    )

    payload = response["Payload"]

    txt = io.BytesIO(payload.read()).read().decode("utf-8")
    print(f"Response:\n{txt}")

except Exception as e:
    print(e)