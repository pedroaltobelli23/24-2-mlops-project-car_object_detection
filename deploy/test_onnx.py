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

load_dotenv()

def startup_event():    
    """Download model.onnx that is inside S3 bucket and load the model. If it is already dowloaded, just load the model.

    Returns:
        InferenceSession: onnx model. more information in https://onnxruntime.ai/
    """
    
    model_path = "/home/pedro/Documents/mlops/24-2-mlops-project-car_object_detection/models/runs/detect/train3/weights/best.onnx"
            
    model = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    model_input = model.get_inputs()
    img_sz = model_input[0].shape[-1] 
        
    return model, img_sz


def intersection(box1,box2):
    box1_x1,box1_y1,box1_x2,box1_y2 = box1[:4]
    box2_x1,box2_y1,box2_x2,box2_y2 = box2[:4]
    x1 = max(box1_x1,box2_x1)
    y1 = max(box1_y1,box2_y1)
    x2 = min(box1_x2,box2_x2)
    y2 = min(box1_y2,box2_y2)
    return (x2-x1)*(y2-y1)

def union(box1,box2):
    box1_x1,box1_y1,box1_x2,box1_y2 = box1[:4]
    box2_x1,box2_y1,box2_x2,box2_y2 = box2[:4]
    box1_area = (box1_x2-box1_x1)*(box1_y2-box1_y1)
    box2_area = (box2_x2-box2_x1)*(box2_y2-box2_y1)
    return box1_area + box2_area - intersection(box1,box2)

def iou(box1,box2):
    return intersection(box1,box2)/union(box1,box2)


def make_prediction(event, context):
    try:
        # Encode part
        data = open("test_image.jpg","rb").read()
        data = base64.b64encode(data).decode("utf8")
        
        # Decode part
        data = data.encode("utf-8")
        img_b64dec = base64.b64decode(data)
        img_byteIO = BytesIO(img_b64dec)
        
        model, img_sz = startup_event()
        
        img = Image.open(img_byteIO)
        
        img = img.resize((img_sz,img_sz))
        img = img.convert("RGB")
        img_width, img_height = img.size
        inputer = np.array(img) / 255.0
        inputer = inputer.transpose(2, 0, 1)
        inputer = inputer.reshape(1, 3, img_sz, img_sz).astype(np.float32)
        
        
        outputs = model.run(["output0"], {"images":inputer})
        
        return {"result":"worked here"}
    
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
            boxes = [box for box in boxes if iou(box, boxes[0]) < 0.5]

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
        
        confidence_first_detect = str(result_dict[0]["confidence"])
        
        return {"result":"end"}
    except Exception as e:
        error = traceback.format_exc()
        return {"error":str(error)+str(sys.version)}
    
if __name__=="__main__":
    print(make_prediction("a","b"))