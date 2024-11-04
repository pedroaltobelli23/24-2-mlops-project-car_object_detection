import boto3
import os
from dotenv import load_dotenv
import random
import string
import argparse
import traceback

def create_API(lambda_function_name, api_gateway_name):
    try:
        load_dotenv()

        id_num = "".join(random.choices(string.digits, k=7))

        api_gateway = boto3.client(
            "apigatewayv2",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )

        lambda_function = boto3.client(
            "lambda",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )

        lambda_function_get = lambda_function.get_function(FunctionName=lambda_function_name)

        api_gateway_create = api_gateway.create_api(
            Name=api_gateway_name,
            ProtocolType="HTTP",
            Version="1.0",
            RouteKey="POST /predict", # Create a /polarity POST route
            Target=lambda_function_get["Configuration"]["FunctionArn"],
        )

        api_gateway_permissions = lambda_function.add_permission(
            FunctionName=lambda_function_name,
            StatementId="api-gateway-permission-statement-" + id_num,
            Action="lambda:InvokeFunction",
            Principal="apigateway.amazonaws.com",
        )

        print("API Endpoint:", api_gateway_create["ApiEndpoint"])

        print(api_gateway_create)
    except Exception as e:
        print(traceback.format_exc())
            
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--lambda_function", type=str, help="name of the lambda function that will be used in the API.", default="lambda-function"
    )
    
    parser.add_argument(
        "--api_gateway", type=str, help="name of the API gateway. Default is demo_project.", default="demo_project"
    )

    args = parser.parse_args()
    
    create_API(lambda_function_name=args.lambda_function, api_gateway_name=args.api_gateway)