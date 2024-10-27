import requests
import zipfile
import os
import traceback
from dotenv import load_dotenv
import logging
from roboflow import Roboflow
from urllib.error import HTTPError

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-18s %(name)-8s %(levelname)-8s %(message)s",
    datefmt="%y-%m-%d %H:%M",
    filename="logs/download.log",
    filemode="a",
)

rf_logger = logging.getLogger("roboflow")
rf_logger.setLevel(logging.INFO)

def dowload_dataset(location):
    """Download and unzip data from https://universe.roboflow.com/openglpro/stanford_car/dataset/10
    and put it inside "data" folder
    """
    
    try:
        rf = Roboflow(api_key=os.getenv("ROBOFLOW_API_KEY"))
        workspace = "openglpro"
        dataset = "stanford_car"
        version = 10
        model = "yolov8"
        
        project = rf.workspace(workspace).project(dataset).version(version)
            
        logging.info("Downloading dataset...")
        dataset = project.download("yolov8",location=location,overwrite=True)
        logging.info("Dataset downloaded in data/.")
    except Exception as e:
        logging.error(traceback.format_exc())
        
    return None

if __name__=="__main__":
    
    dowload_dataset("data/data/")