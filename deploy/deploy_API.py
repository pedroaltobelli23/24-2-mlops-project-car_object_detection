import boto3
import os
from dotenv import load_dotenv
import argparse
import random
import traceback
import string


class Deployment:
    def __init__(
        self, lambda_name, access_key_id, secret_access_key, region, lambda_role_arn
    ):
        self.lambda_name = lambda_name
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region = region
        self.lambda_role_arn = lambda_role_arn

    def create_lambda_function(self, image_uri):
        try:
            function_name = self.lambda_name

            lambda_client = boto3.client(
                "lambda",
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name=self.region,
            )

            try:
                response = lambda_client.delete_function(FunctionName=function_name)
            except Exception as e:
                print(f"Function don't exist: {str(e)}")

            response = lambda_client.create_function(
                FunctionName=function_name,
                PackageType="Image",
                Code={"ImageUri": image_uri},
                Role=self.lambda_role_arn,
                Timeout=900,
                MemorySize=512,
                Environment={
                    "Variables": {
                        "BUCKET_MODEL": os.getenv("BUCKET_MODEL"),
                        "ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
                        "SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
                        "REGION": os.getenv("AWS_REGION"),
                    }
                },
            )

            print("Lambda function created successfully:")
            print(f"Function Name: {response['FunctionName']}")
            print(f"Function ARN: {response['FunctionArn']}")
        except Exception as e:
            print(traceback.format_exc())
            return False
        return True

    def create_API(self, api_gateway_name):
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

            lambda_function_get = lambda_function.get_function(
                FunctionName=self.lambda_name
            )

            api_gateway_create = api_gateway.create_api(
                Name=api_gateway_name,
                ProtocolType="HTTP",
                Version="1.0",
                RouteKey="POST /predict",  # Create a /polarity POST route
                Target=lambda_function_get["Configuration"]["FunctionArn"],
            )

            api_gateway_permissions = lambda_function.add_permission(
                FunctionName=self.lambda_name,
                StatementId="api-gateway-permission-statement-" + id_num,
                Action="lambda:InvokeFunction",
                Principal="apigateway.amazonaws.com",
            )

            print("API Endpoint:", api_gateway_create["ApiEndpoint"])

            print(api_gateway_create)
        except Exception as e:
            print(traceback.format_exc())

    def full_deploy(self, args):
        if any(vars(args).values()):
            if args.image_uri and args.api_gateway:
                self.create_lambda_function(args.image_uri)
                self.create_API(args.api_gateway)
            else:
                print("Wrong arguments")
        else:
            print("No arguments provided")


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--image_uri", 
        type=str, 
        help="ECR uri",
    )

    parser.add_argument(
        "--api_gateway",
        type=str,
        help="name of the API gateway. Default is demo_project.",
        default="demo_project",
    )

    args = parser.parse_args()

    deployment_module = Deployment(
        "lambda-project-pedroatp",
        os.getenv("AWS_ACCESS_KEY_ID"),
        os.getenv("AWS_SECRET_ACCESS_KEY"),
        os.getenv("AWS_REGION"),
        os.getenv("AWS_LAMBDA_ROLE_ARN"),
    )

    deployment_module.full_deploy(args)