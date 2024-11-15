"""
    Application using streamlit. User upload image and prediction is made. If there are any detections, show the image with the bounding boxes. 
"""
import streamlit as st
import requests
import numpy as np
import cv2
import random
from dotenv import load_dotenv
import os

load_dotenv()

def draw_bbox(img,boxes):
    """
        Draw bounding boxes with random colors in the image for each detection.
        
        Parameters:
        ~~~~~~~~~~~~~~~~~~~~
        img : numpy.ndarray
            The image on which bounding boxes will be drawn.
        boxes : list of dict
            Each dictionary in the list represents a bounding box.
        
        Returns:
        ~~~~~~~~~~
        numpy.ndarray
            Modified image with bounding boxes.
    """
    
    for box in boxes:
        # Use random color for each box
        r1 = random.randint(0, 255)
        r2 = random.randint(0, 255)
        r3 = random.randint(0, 255)
        rand_color = (r1, r2, r3) 
        
        # Set line width for the rectangle and text thickness
        line_width = max(round(sum(img.shape) / 2 * 0.003), 2)
        
        # Draw the box and the confidence
        cv2.rectangle(img, (box["x1"], box["y1"]), (box["x2"], box["y2"]), color=rand_color, thickness=line_width, lineType=cv2.LINE_AA)
        label = f"{box['class']} {box['confidence']:.2f}"
        (text_width, text_height), baseline = cv2.getTextSize(label, cv2.LINE_AA, 0.8, thickness=line_width)
        cv2.rectangle(img, (box["x1"], box["y1"] - 10 - text_height - baseline), (box["x1"] + text_width, box["y1"] - 10 + baseline), color=rand_color, thickness=cv2.FILLED)
        cv2.putText(img, label, (box["x1"], box["y1"] - 10), cv2.LINE_AA, 0.8, color=(255, 255, 255), thickness=line_width, lineType=cv2.LINE_AA)

    return img
    

def main(endpoint):
    """
        Streamlit application main function.
        
        Parameters:
        ~~~~~~~~~~~~~~~~~~~~
        endpoint : str
            The AWS API endpoint.

        Functionality:
        - Displays "index.md" file.
        - `st.file_uploader` allows user to upload an image file (PNG or JPG).
        - Sends the uploaded image to the specified endpoint for object detection.
        - Draws bounding boxes of detected objects on the image, if any.
        - Displays the modified image with bounding boxes or the original image if no detections are found.
    """
    with open("index.md") as f:
        st.markdown(f.read())
    
    uploaded_file = st.file_uploader("Upload car image",type=["png","jpg"])
    
    if uploaded_file is not None:
        bytes_img = uploaded_file.getvalue()
        
        response = requests.post(endpoint, data=bytes_img).json()["result"]
        
        if response:
            image_array = np.frombuffer(bytes_img, dtype=np.uint8)
            img = cv2.imdecode(image_array, cv2.COLOR_BGR2RGB)
            st.write(f"{len(response)} Detection(s) in the image {uploaded_file.name}")
            
            draw_bbox(img, response)
            
            _, buffer = cv2.imencode('.jpg', img)
            img_with_bbox = buffer.tobytes()
            
            st.image(img_with_bbox, channels="BGR")
        else:
            st.image(bytes_img)
            st.write(f"No Detections found in the image {uploaded_file.name}")
        
    return None

if __name__=="__main__":
    endpoint = os.getenv("ENDPOINT","default_endpoint")+"/predict"
    region = os.getenv("AWS_REGION")
    
    endpoint = endpoint.replace("REGION",region)
    main(endpoint)