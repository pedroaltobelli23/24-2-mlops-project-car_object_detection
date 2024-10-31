from ultralytics import YOLO, settings
import mlflow
import uuid
import os
from dotenv import set_key, find_dotenv, load_dotenv
import boto3
from botocore.exceptions import ClientError
import logging
import traceback

logging.basicConfig(
    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO,
    filename="../logs/model_train.log",
    filemode="a"
)

load_dotenv(find_dotenv())

def train_with_YOLO(hp : dict):
    """Train YOLO using the stanford car dataset and save it inside S3 bucket

    Args:
        hp (dict): dict of hyperparameters. Here is an example:
        {
            "experiment_name":"test",
            "epochs":1,
            "batch":12,
            "optimizer":"AdamW",
            "imgsz":640,
            "scale":0.5
        }

    Returns:
        bool: True if train was succesful and model saved inside S3 bucket
    """
    
    try:
        
        logging.info("Training model...")
        with mlflow.start_run():
            mlflow.log_params(hp)
            results = model.train(data="config.yaml", epochs=hp["epochs"],imgsz=hp['imgsz'],scale=hp['scale'],batch=hp['batch'],optimizer=hp['optimizer'], amp=False)
        logging.info("Model finished running")        
        object_name = "model.pt"
        model_path = os.path.join(results.save_dir,"weights","best.pt")
        
        logging.info(results)
        
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
        
        bkt = os.getenv("BUCKET_MODEL")
        logging.info(f"{model_path} saved into {bkt} as {object_name}.")
    except Exception as e:
        logging.error(traceback.format_exc())
        return False
    return True

if __name__=="__main__":
    try:
        hiper_parameters = {"experiment_name":"training","epochs":1,"batch":8,"optimizer":"SGD","imgsz":420,"scale":0.5}
    
        model = YOLO("yolov8n.pt")
    
        settings.update({"mlflow":True})
        mlflow.set_tracking_uri("file:../models/runs/mlflow")
    
        mlflow.set_experiment(hiper_parameters.get("experiment_name"))
        
        result = train_with_YOLO(hiper_parameters)
        
    except Exception as e:
        print(e)