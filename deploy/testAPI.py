import requests
import cv2
import os

def save_prediction(image_path):
    data = open("test_images/img_2.jpg","rb").read()
    resp = requests.post(url, data=data).json()["result"]
    
    img = cv2.imread(image_path)
    cv2.rectangle(img,(resp["x1"],resp["y1"]),(resp["x2"],resp["y2"]),color=(0, 0, 255),thickness=10)
    
    base, ext = os.path.splitext(image_path)
    save_path = f"{base}_prediction{ext}"
    cv2.imwrite(save_path,img)
    

if __name__=="__main__":
    
    url_endpoint = "https://q6vvrh22dk.execute-api.us-east-2.amazonaws.com"
    url = f"{url_endpoint}/predict"
    
    save_prediction("test_images/img_2.jpg")
