"""
    Model training with YOLOv8.
    
    - Mlflow: Model tracking. Can access in localhost:5000.
    - boto3: Connect to S3 bucket
    
    User can easily modify hiperparameters used for training. Logs are saved in logs/model_train.log. Model is saved in .onnx format. 
    This format is lighter and for predictions, it is not necessary to install pytorch and ultralytics packages.
    Very useful to make the ECR Docker lighter.
    The only difference is that it is necessary to do some preprocessing, that is described in the lambda function. 
"""

from ultralytics import YOLO, settings
import mlflow
import os
from dotenv import set_key, find_dotenv, load_dotenv
import boto3
from botocore.exceptions import ClientError
import logging
import traceback

logging.basicConfig(
    format="%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.INFO,
    filename="../logs/model_train.log",
    filemode="a",
)

load_dotenv(find_dotenv())


def train_with_YOLO(hp: dict):
    try:

        model = YOLO("yolov8n.pt")

        logging.info("Training model...")
        with mlflow.start_run():
            mlflow.log_params(hp)
            results = model.train(
                data="config.yaml",
                epochs=hp["epochs"],
                imgsz=hp["imgsz"],
                scale=hp["scale"],
                batch=hp["batch"],
                optimizer=hp["optimizer"],
                amp=False,
            )
        logging.info("Model finished running")
        object_name = "model.onnx"
        model_path = os.path.join(results.save_dir, "weights", "best.onnx")

        # Export model from .pt to .onnx. This format is lighter and for predictions, it is not necessary to install pytorch and ultralytics packages.
        # Very useful to make the ECR Docker lighter.
        # The only difference is that it is necessary to do some preprocessing, that is described in the lambda function. 
        model.export(format="onnx")

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
        project_root = os.getcwd()
        model_path_short = os.path.relpath(model_path, project_root)

        logging.info(f"{model_path_short} saved into {bkt} as {object_name}.")
    except Exception as e:
        logging.error(traceback.format_exc())
        return False
    return True


def main(hp: dict):
    """
    Train a YOLO model using specified hyperparameters and save the trained model to an S3 bucket.

    This function initializes a YOLO model, trains it on the Stanford car dataset using the provided
    hyperparameters, and then exports the best model in ONNX format. The trained model is uploaded
    to an S3 bucket for storage.
    
    Set mlflow to save tracking inside folder model/runs/mlflow. Logs are saved in logs/model_train.log.

    Parameters:
    ~~~~~~~~~~~~~~~~~~~~
    hp : dict
        A dictionary containing hyperparameters for training, including:

        - 'epochs' (int): Number of training epochs.
        - 'imgsz' (int): Image size for training.
        - 'scale' (float): Scaling factor for augmentation.
        - 'batch' (int): Batch size for training.
        - 'optimizer' (str): Optimizer to use for training.

    Returns:
    ~~~~~~~~~~~
    bool
        True if training was successful and the model was uploaded to the S3 bucket, False otherwise.
    """

    try:
        settings.update({"mlflow": True})
        mlflow.set_tracking_uri("file:../models/runs/mlflow")

        mlflow.set_experiment(hp.get("experiment_name"))

        result = train_with_YOLO(hp)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # Change this parameters when training
    hiper_parameters = {
        "experiment_name": "training",
        "epochs": 5,
        "batch": 12,
        "optimizer": "SGD",
        "imgsz": 448,
        "scale": 0.5,
    }
    
    main(hiper_parameters)
