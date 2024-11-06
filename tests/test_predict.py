import os
from PIL import Image
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from predict import make_predictions
from dotenv import load_dotenv


load_dotenv()

def test_predict():
    endpoint = os.getenv("ENDPOINT","default_endpoint")+"/predict"
    region = os.getenv("AWS_REGION")
    
    endpoint = endpoint.replace("REGION",region)
    print(endpoint)
    img_path = "tests/img.jpg"
    label_path = "tests/label.txt"
    
    tolerance = 20 
    
    with open(label_path, 'r') as file:
        line = file.readline().strip()
        true_values = line.split()
        
    yolo_classes = ["motorbike","vehicle"]
    true_label = yolo_classes[int(true_values[0])]
    img = Image.open(img_path)
    x,y = img.size
    center_x = x*float(true_values[1])
    center_y = y*float(true_values[2])
    width = x*float(true_values[3])
    height = y*float(true_values[4])
    
    x1_true = center_x-(width/2)
    x2_true = center_x+(width/2)
    y1_true = center_y-(height/2)
    y2_true = center_y+(height/2)
    

    resp = make_predictions(endpoint,img_path)

    assert resp["class"] == true_label, f"Expected class {true_label}, got {resp['class']}"
    print(resp["class"], true_label)
    assert abs(resp["x1"] - x1_true) <= tolerance, f"x1 mismatch: expected {x1_true}, got {resp['x1']}"
    print(resp['x1'], x1_true)
    assert abs(resp["x2"] - x2_true) <= tolerance, f"x2 mismatch: expected {x2_true}, got {resp['x2']}"
    print(resp['x2'], x2_true)
    assert abs(resp["y1"] - y1_true) <= tolerance, f"y1 mismatch: expected {y1_true}, got {resp['y1']}"
    print(resp['y1'], y1_true)
    assert abs(resp["y2"] - y2_true) <= tolerance, f"y2 mismatch: expected {y2_true}, got {resp['y2']}"
    print(resp['y2'], y2_true)
