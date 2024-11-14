import streamlit as st
import requests
import numpy as np
import cv2
import random

def draw_bbox(img,boxes):
    
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
    

def main():
    endpoint = "https://9kq6eqv1bh.execute-api.us-east-2.amazonaws.com/predict"
    with open("app/index.md") as f:
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
    main()