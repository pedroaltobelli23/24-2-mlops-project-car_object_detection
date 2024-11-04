import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the CloudWatch Logs client
client =  boto3.client(
            "logs",
            aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
            region_name=os.getenv("REGION"),
        )

# Define log group and parameters
log_group_name = "/aws/lambda/lambda-project-pedroatp"

def get_logs(log_group_name):
    # Fetch streams within the log group
    response = client.describe_log_streams(
        logGroupName=log_group_name,
        orderBy="LastEventTime",
        descending=True,
        limit=1 # Fetches the 5 most recent streams; adjust as needed
    )

    # Loop through each log stream
    for stream in response["logStreams"]:
        log_stream_name = stream["logStreamName"]

        # Fetch log events from the log stream
        log_events = client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            startFromHead=True
        )

        print(f"\nLog Stream: {log_stream_name}")
        for event in log_events["events"]:
            print(event["message"])

# Call function to print logs
get_logs(log_group_name)
