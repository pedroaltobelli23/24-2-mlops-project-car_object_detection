import os
import shutil
from tqdm import tqdm
from glob import glob
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-18s %(name)-8s %(levelname)-8s %(message)s",
    datefmt="%y-%m-%d %H:%M",
    filename="logs/preprocess.log",
    filemode="a",
)

def move_files(file_list,origin_dir, destination_dir):
    """
    Move list of files from origin diretory to destination diretory
    
    Args:
        file_list (list): All files inside origin dir that will be moved
        origin_dir (strPath): Source diretory
        destination_dir (strPath): Destination diretory
    """
    for file_name in tqdm(file_list):
        shutil.move(os.path.join(origin_dir,file_name),os.path.join(destination_dir, file_name))
        
def merge_train_test(train_dir,test_dir,remove_test=True):
    """
    From the https://universe.roboflow.com/openglpro/stanford_car dataset, merge the
    test folder with the train folder.
    
    Args:
        remove_test (bool): Remove the test folder after merge. Default is True.
    """
    
    test_images = [f for f in os.listdir(os.path.join(test_dir,"images"))]
    test_labels = [f for f in os.listdir(os.path.join(test_dir,"labels"))]

    move_files(file_list=test_images,origin_dir=os.path.join(test_dir,"images"),destination_dir=os.path.join(train_dir,"images"))
    move_files(file_list=test_labels,origin_dir=os.path.join(test_dir,"labels"),destination_dir=os.path.join(train_dir,"labels"))

    if remove_test:
        shutil.rmtree(test_dir)
        logging.info(f"Removed test directory: {test_dir}")
    
    return None

def preprocess(train_dir,valid_dir,dir,drop=0.5):
    """
    Simple preprocessing. Drop drop*100 from the train and valid datasets

    Args:
        drop (int): ratio to be dropped. Default is 0.5
    """
    
    for dir in [train_dir,valid_dir]:
        img_dir = os.path.join(dir,"images")
        label_dir = os.path.join(dir,"labels")
        
        img_files = sorted(glob(os.path.join(img_dir,"*.jpg")))
        label_files = sorted(glob(os.path.join(label_dir,"*.txt")))
        
        if drop>0:
            n = len(img_files)
            num_to_drop = int(n*drop)
            imgs_to_remove = img_files[:num_to_drop]
                
            labels_to_remove = label_files[:num_to_drop]
            
            for img,label in zip(imgs_to_remove,labels_to_remove):
                os.remove(img)
                os.remove(label)
                
            logging.info(f"Dropped {num_to_drop}/{n} from {dir}")
        else:
            logging.info("Nothing dropped. No preprocessing")
                
                
    os.remove(os.path.join(dir,"data.yaml"))
    shutil.copy("data.yaml",dir)
    
    return None

if __name__=="__main__":
    logging.info("Starting preprocess...")
    train_dir = "data/data/train"
    test_dir = "data/data/test"
    valid_dir = "data/data/valid"
    
    merge_train_test(train_dir,test_dir)
    preprocess(train_dir,valid_dir,drop=0.6)
    
    logging.info("Preprocessing complete.")