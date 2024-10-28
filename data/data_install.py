import requests
import zipfile
import os
import traceback
from dotenv import load_dotenv
import logging
from roboflow import Roboflow
from urllib.error import HTTPError
import sys


current_filename = os.path.basename(sys.argv[0])

load_dotenv()

logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO,
    filename="logs/data.log",
    filemode="a"
)

logger = logging.getLogger(__name__)

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
            
        logger.info("Downloading dataset...")
        dataset = project.download(model,location=location,overwrite=True)
        logger.info("Dataset downloaded in data/.")
    except Exception as e:
        logger.error(traceback.format_exc())
        
    return None

if __name__=="__main__":
    
    dowload_dataset("data/data/")