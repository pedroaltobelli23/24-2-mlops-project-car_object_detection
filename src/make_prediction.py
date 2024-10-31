import boto3
import os

def startup_event():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
        region_name=os.getenv("REGION"),
    )
    
    obj = s3.get_object(
        Bucket=os.getenv("BUCKET_NAME"),
        Key="pedroatp/model.pkl",
    )
    
    return loaded_model,loaded_ohe

def make_prediction(event, context):
    """Receives json with binarized image

    Args:
        event (_type_): _description_
        context (_type_): _description_

    Returns:
        _type_: _description_
    """
    return None