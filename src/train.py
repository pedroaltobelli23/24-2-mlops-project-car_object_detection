from ultralytics import YOLO, settings
import mlflow
import uuid
import os
from dotenv import set_key, find_dotenv, load_dotenv

load_dotenv(find_dotenv())

def train_with_YOLO(hp : dict):
    """Train YOLO using the stanford car dataset

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
        Dict|None: Training metrics if available and training is successful; otherwise, None.
    """
    
    
    with mlflow.start_run():
        mlflow.log_params(hp)    
        results = model.train(data="config.yaml", epochs=hp["epochs"],imgsz=hp['imgsz'],scale=hp['scale'],batch=hp['batch'],optimizer=hp['optimizer'], amp=False)
    return results

if __name__=="__main__":
    try:
        hiper_parameters = {"experiment_name":"starter","epochs":1,"batch":8,"optimizer":"SGD","imgsz":420,"scale":0.5}
    
        model = YOLO("yolov8n.pt")
    
        settings.update({"mlflow":True})
        mlflow.set_tracking_uri("file:../models/runs/mlflow")
    
        id_experiment = uuid.uuid4()
        mlflow.set_experiment(hiper_parameters.get("experiment_name"))
    
        results = train_with_YOLO(hiper_parameters)
        set_key(key_to_set="MODEL_DEPLOY_PATH",value_to_set=str(os.path.join(results.save_dir,"weights","best.pt")),dotenv_path=find_dotenv())
    except Exception as e:
        print(e)