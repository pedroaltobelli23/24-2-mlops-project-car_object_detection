"""
    See most recent logs from the lambda function.
    
    Usage:
        python3 logs/see_logs_lambda.py --lambda_name <lambda function name>
"""
import boto3
import os
from dotenv import load_dotenv
import argparse

load_dotenv()

def get_logs(lambda_name):
    """
    Retrieves and prints the most recent log events from a specified AWS Lambda function. First, the method connect
    to AWS CloudWatch Logs, identifies the most recent log values for the given Lambda function, and then fetches and displays it.

    Parameters:
    ~~~~~~~~~~~~~~~~~~~~
    lambda_name : str
        AWS lambda function from which logs will be retrieved
    """
    
    log_group_name = "/aws/lambda/"+lambda_name
    
    # CloudWatch Logs client init
    client =  boto3.client(
                "logs",
                aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
                region_name=os.getenv("REGION"),
            )
    
    response = client.describe_log_streams(
        logGroupName=log_group_name,
        orderBy="LastEventTime",
        descending=True,
        limit=1  # Fetches only the most recent stream
    )

    for stream in response["logStreams"]:
        log_stream_name = stream["logStreamName"]

        log_events = client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            startFromHead=True
        )

        print(f"\nLog Stream: {log_stream_name}")
        for event in log_events["events"]:
            print(event["message"])

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--lambda_name", type=str, help="Name of the lambda function",default="lambda-function-name"
    )
    
    args = parser.parse_args()
    
    get_logs(args.lambda_name)