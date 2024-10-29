from ultralytics import YOLO, settings
import mlflow
import uuid

def train_with_YOLO(hp : dict):
    """Train YOLO using the stanford car dataset

    Args:
        hp (dict): dict of hyperparameters. Here is an example:
        {
            "experiment_name":"test",
            "epochs":1,
            "batch":12,
            "optimizer":"AdamW",
            "imgsz":512,
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
    hiper_parameters = {"experiment_name":"starter","epochs":1,"batch":12,"optimizer":"AdamW","imgsz":640,"scale":0.5}
    
    model = YOLO("yolov8n.pt")
    
    settings.update({"mlflow":True})
    mlflow.set_tracking_uri("file:../runs/mlflow")
    
    id_experiment = uuid.uuid4()
    mlflow.set_experiment(hiper_parameters.get("experiment_name"))
    
    train_with_YOLO(hiper_parameters)