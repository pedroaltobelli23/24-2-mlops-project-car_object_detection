from ultralytics import YOLO, settings
import mlflow

if __name__=="__main__":
    model = YOLO("yolov10n.pt")

    settings.update({"mlflow": True})
    mlflow.set_tracking_uri("file:./runs/mlflow")
    
    epochs=1
    batch_size = 12
    optimizer = "AdamW"
    scale=0.5
    imgsz=512
    
    if mlflow.active_run():
        mlflow.end_run()
    
    with mlflow.start_run():
        #guardar parametros do modelo
        mlflow.log_param("model", "YOLOv10")
        mlflow.log_param("dataset", "Current tag")
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("config", "config.yaml")
        mlflow.set_tracking_uri("file:./runs/mlflow")
        mlflow.log_param("batch", batch_size)
        mlflow.log_param("optimizer", optimizer)
        mlflow.log_param("imgsz", imgsz)
        mlflow.log_param("scale", scale)
    
    results = model.train(data="config.yaml", epochs=epochs,imgsz=imgsz,scale=scale,batch=batch_size,optimizer=optimizer, amp=False)