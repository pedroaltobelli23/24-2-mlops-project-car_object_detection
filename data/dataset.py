"""This module is used to install and preprocess the data from https://universe.roboflow.com/openglpro/stanford_car/dataset/10 specific for the YOLOv8 version. It is possible to modify the function preprocess to do your onw preprocessing
"""

import os
import traceback
from dotenv import load_dotenv
import logging
from roboflow import Roboflow
from tqdm import tqdm
from glob import glob
import shutil
import argparse

class Dataset:
    def __init__(self):
        pass
    
    def dowload_dataset(self):
        """Download and unzip data from https://universe.roboflow.com/openglpro/stanford_car/dataset/10
        and put it inside "data" folder
        """
        
        location = "data/data/"
        
        try:
            rf = Roboflow(api_key=os.getenv("ROBOFLOW_API_KEY"))
            workspace = "openglpro"
            dataset = "stanford_car"
            version = 10
            model = "yolov8"
            
            project = rf.workspace(workspace).project(dataset).version(version)
                
            logging.info("Downloading dataset...")
            dataset = project.download(model,location=location,overwrite=True)
            logging.info("Dataset downloaded in data/.")
        except Exception as e:
            logging.error(traceback.format_exc())
            
        return None
    
    
    def move_files(self, file_list, origin_dir, destination_dir):
        """
            Move list of files from origin diretory to destination diretory

            Parameters:
            ~~~~~~~~~~~~~~~~~~~~
            file_list (list): All files inside origin dir that will be moved
            origin_dir (strPath): Source diretory
            destination_dir (strPath): Destination diretory
        """
        try:
            for file_name in tqdm(file_list):
                shutil.move(
                    os.path.join(origin_dir, file_name),
                    os.path.join(destination_dir, file_name),
                )
                
            logging.debug(f"Files moved from {origin_dir} to {destination_dir}")
        except Exception as e:
            logging.error(traceback.format_exc())


    def merge_train_test(self, remove_test=True):
        """
            From the https://universe.roboflow.com/openglpro/stanford_car dataset, merge the
            test folder with the train folder.

            Parameters:
            ~~~~~~~~~~~~~~~~~~~~
            remove_test (bool): Remove the test folder after merge. Default is True.
        """
        
        train_dir = "data/data/train"
        test_dir = "data/data/test"

        try:
            test_images = [f for f in os.listdir(os.path.join(test_dir, "images"))]
            test_labels = [f for f in os.listdir(os.path.join(test_dir, "labels"))]

            self.move_files(
                file_list=test_images,
                origin_dir=os.path.join(test_dir, "images"),
                destination_dir=os.path.join(train_dir, "images"),
            )
            
            self.move_files(
                file_list=test_labels,
                origin_dir=os.path.join(test_dir, "labels"),
                destination_dir=os.path.join(train_dir, "labels"),
            )

            if remove_test:
                shutil.rmtree(test_dir)
                logging.debug(f"Removed test directory: {test_dir}")
        except Exception as e:
            logging.error(traceback.format_exc())
        return None

    def preprocess(self, drop=0.5):
        """
            Simple preprocessing. Drop drop*100 from the train and valid datasets

            Parameters:
            ~~~~~~~~~~~~~~~~~~~~
            drop (int): Ratio from dataset to be dropped
        """
        
        train_dir = "data/data/train"
        valid_dir = "data/data/valid"
        try:
            for dir in [train_dir, valid_dir]:
                img_dir = os.path.join(dir, "images")
                label_dir = os.path.join(dir, "labels")

                img_files = sorted(glob(os.path.join(img_dir, "*.jpg")))
                label_files = sorted(glob(os.path.join(label_dir, "*.txt")))

                if 0 < drop < 1:

                    n = len(img_files)
                    num_to_drop = int(n * drop)
                    imgs_to_remove = img_files[:num_to_drop]

                    labels_to_remove = label_files[:num_to_drop]

                    for img, label in zip(imgs_to_remove, labels_to_remove):
                        os.remove(img)
                        os.remove(label)

                    logging.info(f"Dropped {num_to_drop}/{n} images from {dir}")
                else:
                    logging.info("Nothing dropped. No preprocessing.")
        except Exception as e:
            logging.error(traceback.format_exc())
        return None
    
if __name__=="__main__":
    load_dotenv()

    logging.basicConfig(
        format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S',
        level=logging.INFO,
        filename="logs/data.log",
        filemode="a"
    )
    
    logging.info("Starting preprocess...")
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--drop", type=float, help="Ratio from dataset to be dropped. 0 to 1.",default=0.5
    )
    
    parser.add_argument(
        "--download_data", action="store_true", help="True to dowload data from internet using roboflow"
    )

    args = parser.parse_args()

    dataset = Dataset()
    try:
        if args.download_data:
            dataset.dowload_dataset()
        dataset.merge_train_test()
        logging.info(f"Drop used: {args.drop}")
        dataset.preprocess( drop=args.drop)

        logging.info("Preprocessing complete.")
    except Exception as e:
        locals.error(traceback.format_exc())