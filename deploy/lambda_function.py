"""
    This script serves as an AWS Lambda function for performing object detection on images using an ONNX model stored in an S3 bucket. The function is designed to handle image input in base64 format, download the model if it's not already available, and make predictions on bounding boxes for detected objects.

    - Load AWS information from `.env` file.
    - Decode the base64-encoded image input from a HTTP request and match resize the image to the correct input.
    - Download the ONNX model from an S3 bucket and save it into `/tmp`.
    - Run inference.
    - Calculate Intersection Over Union (IoU) to remove overlapping boxes.
    - Return the prediction results.
"""

import boto3
import os
from dotenv import load_dotenv
import onnxruntime as ort
import numpy as np
import traceback
import sys
from PIL import Image
import base64
from io import BytesIO
import json
import sys

load_dotenv()

def intersectionOverUnion(bb1, bb2):
    r"""
        Calculate the Intersection Over Union (IoU) between two bounding boxes.

        .. math::

            \text{IoU} = \frac{\text{Intersection Area}}{\text{Union Area}}
            
        Parameters:
        ~~~~~~~~~~~~~~~~~~~~
        bb1 : list
            Coordinates of the first bounding box in the format `[x1, y1, x2, y2]`.
        bb2 : list
            Coordinates of the second bounding box in the format `[x1, y1, x2, y2]`.

        Returns:
        ~~~~~~~~~~
        float
            IoU value
    """
    bb1_x1, bb1_y1, bb1_x2, bb1_y2 = bb1[:4]
    bb2_x1, bb2_y1, bb2_x2, bb2_y2 = bb2[:4]
    
    x1 = max(bb1_x1, bb2_x1)
    y1 = max(bb1_y1, bb2_y1)
    x2 = min(bb1_x2, bb2_x2)
    y2 = min(bb1_y2, bb2_y2)
    intersec = (x2-x1)*(y2-y1)
    
    bb1_area = (bb1_x2-bb1_x1)*(bb1_y2-bb1_y1)
    bb2_area = (bb2_x2-bb2_x1)*(bb2_y2-bb2_y1)
    
    union = bb1_area + bb2_area - intersec
    IoU = intersec/union
    return IoU


def make_prediction(event, context):
    """
        Handle the prediction process for an image input using the model inside S3 bucket.

        Parameters:
        ~~~~~~~~~~~~~~~~~~~~
        event (dict): Event data from AWS Lambda containing the encoded image.
        
        Returns:
        ~~~~~~~~~~
        dict: The result of the prediction, containing detected bounding boxes or an error message.
            - Class (str): Name of the class
            - Confidence (float): Percentage of confidence for the bounding box predicted
            - Point 1 (int, int): Top left corner of the bounding box
            - Point 2 (int, int): Bottom right corner of the bounding box
    """
    try:
        print("Python version")
        print(sys.version)
        print("Version info.")
        print(sys.version_info)
        
        img_B = event["body"].encode("utf-8")
        img_b64 = base64.b64decode(img_B)
        img = Image.open(BytesIO(img_b64))
        
        print("Downloading model")
        model_path = os.path.join("/tmp", "model.onnx")
        
        # Dowload file from S3 if not dowloaded it in the docker
        if not os.path.exists(model_path):
        
            s3 = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
                region_name=os.getenv("REGION"),
            )
            
            bucket_name = os.getenv("BUCKET_MODEL")
            print(f"Bucket: {bucket_name}")
            s3.download_file(bucket_name, 'model.onnx', model_path)
        
        so = ort.SessionOptions()
        so.log_severity_level = 3
        
        model = ort.InferenceSession(model_path, sess_options=so)
        
        
        model_input = model.get_inputs()
        
        img_sz = model_input[0].shape[-1]
    
        img_width, img_height = img.size
        img = img.resize((img_sz,img_sz))
        img = img.convert("RGB")
        inputer = np.array(img) / 255.0
        inputer = inputer.transpose(2, 0, 1)
        inputer = inputer.reshape(1, 3, img_sz, img_sz).astype(np.float32)
        
        ort_inputs = {model.get_inputs()[0].name: inputer}
        
        print("Inference started...")
        outputs = model.run(None, ort_inputs)

        output = outputs[0].astype(float)
        output = output.transpose()

        yolo_classes = ["motorbike","vehicle"]

        boxes = []
        for row in output:
            prob = row[4:].max()
            if prob < 0.5:
                continue
            class_id = row[4:].argmax()
            label = yolo_classes[class_id]
            xc, yc, w, h = row[:4]
            x1 = (xc - w/2) / img_sz * img_width
            y1 = (yc - h/2) / img_sz * img_height
            x2 = (xc + w/2) / img_sz * img_width
            y2 = (yc + h/2) / img_sz * img_height
            boxes.append([x1, y1, x2, y2, label, prob])


        boxes.sort(key=lambda x: x[5], reverse=True)
        result = []
        while len(boxes) > 0:
            result.append(boxes[0])
            boxes = [box for box in boxes if intersectionOverUnion(box, boxes[0]) < 0.5]

        result_dict = {}
        for i in range(len(result)):
            res = result[i]
            
            x1 = int(res[0].item())
            y1 = int(res[1].item())
            x2 = int(res[2].item())
            y2 = int(res[3].item())
            m_class = res[4]
            confidence = float(res[5])
            
            result_dict[i] = {"x1":x1,"y1":y1,"x2":x2,"y2":y2,"class":m_class,"confidence":confidence}
            print(f"Detection {i}:")
            print(f"Class: {m_class}")
            print(f"Confidence (%): {confidence}")
            print(f"Point 1: ({x1},{y1})")
            print(f"Point 2: ({x2},{y2})")
            print("\n")
        
        if len(result_dict)>0:
            return {"result":result_dict[0]}
        else:
            print(f"No detections found in the image.")
            return {"result":None}
    except Exception as e:
        error = traceback.format_exc()
        return {"error":str(error)}