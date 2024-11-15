"""
This script automates the deployment of an AWS Lambda function using an ECR Image and integrates it with an API Gateway for HTTP/HTTPS access. 
The `Deployment` class handle the creation and configuration of the Lambda function and API Gateway.

The script uses environment variables for AWS credentials and Lambda configuration, and uses `argparse` to handle commandline arguments. 
This feature is important to automate the deploy using github actions, allowing to set the API endpoint as the output of this script
and pass as argument the URI of an ECR Image and the name for the API gateway.
"""
import boto3
import os
from dotenv import load_dotenv
import argparse
import random
import traceback
import string


class Deployment:
    """
    Class to handle AWS Lmabda function deployment inside the ECR container and API Gateway integration.
    """
    def __init__(
        self, lambda_name, access_key_id, secret_access_key, region, lambda_role_arn, bucket
    ):
        """
        Parameters:
        ~~~~~~~~~~~~~~~~~~~~
        lambda_name : str
            The name of the Lambda function to be created or updated.
        access_key_id : str
            AWS access key ID for authentication.
        secret_access_key : str
            AWS secret access key for authentication.
        region : str
            AWS region for Lambda and API Gateway deployment.
        lambda_role_arn : str
            ARN of the IAM Role for Lambda execution permissions.
        bucket : str
            S3 bucket name for Lambda resources (e.g., model files).
        """
        self.lambda_name = lambda_name
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region = region
        self.lambda_role_arn = lambda_role_arn
        self.bucket = bucket

    def create_lambda_function(self, image_uri):
        """
            Creates Lambda function using specified ECR image URI.

            If the Lambda function already exists, it deletes the function before creating a new one.
            Configures the Lambda function with environment variables for S3 bucket access and AWS credentials.

            Parameters:
            ~~~~~~~~~~~~~~~~~~~~
            image_uri : str
                The URI of the container image in ECR to be used for Lambda deployment.

            Returns:
            ~~~~~~~~~~
            bool
                True if the Lambda function creation is successful, False otherwise.
        """
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
                        "BUCKET_MODEL": self.bucket,
                        "ACCESS_KEY_ID": self.access_key_id,
                        "SECRET_ACCESS_KEY": self.secret_access_key,
                        "REGION": self.region,
                    }
                },
            )
        except Exception as e:
            print(traceback.format_exc())
            return False
        return True

    def create_API(self, api_gateway_name):
        """
        Creates an API Gateway with an HTTP POST endpoint to expose the Lambda function.

        Sets up permissions to allow the API Gateway to invoke the Lambda function and generates
        a unique API Gateway endpoint URL for access.

        Parameters:
        ~~~~~~~~~~~~~~~~~~~~
        api_gateway_name : str
            The name of the API Gateway to be created.
        """
        try:
            load_dotenv()

            id_num = "".join(random.choices(string.digits, k=7))

            api_gateway = boto3.client(
                "apigatewayv2",
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name=self.region,
            )

            lambda_function = boto3.client(
                "lambda",
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name=self.region,
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

            # Github actions don't print the endpoint correctly so it is necessary to replace the environment variabel region wiht the word REGION.
            endpoint = str(api_gateway_create["ApiEndpoint"])
            
            endpoint_no_region = endpoint.replace(self.region, "REGION")
            
            print(endpoint_no_region)
        except Exception as e:
            print(traceback.format_exc())

    def full_deploy(self, args):
        """
        Performs a full deployment process. Integration between lambda function and API.

        Parameters:
        ~~~~~~~~~~~~~~~~~~~~
        args : Namespace
            Parsed commandline arguments containing `image_uri` for the ECR URI and `api_gateway` for the API name.
        """
        if any(vars(args).values()):
            if args.image_uri and args.api_gateway:
                self.create_lambda_function(args.image_uri)
                self.create_API(args.api_gateway)
            else:
                print("Invalid arguments provided.")
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
        "lambda-project-car-detection",
        os.getenv("AWS_ACCESS_KEY_ID"),
        os.getenv("AWS_SECRET_ACCESS_KEY"),
        os.getenv("AWS_REGION"),
        os.getenv("AWS_LAMBDA_ROLE_ARN"),
        os.getenv("BUCKET_MODEL"),
    )

    deployment_module.full_deploy(args)