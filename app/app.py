import streamlit as st
import requests
import numpy as np
import cv2

def main():
    endpoint = "https://er5wx1be71.execute-api.us-east-2.amazonaws.com/predict"
    with open("index.md") as f:
        st.markdown(f.read())
    
    uploaded_file = st.file_uploader("Upload car image",type=["png","jpg"])
    
    if uploaded_file is not None:
        bytes_img = uploaded_file.getvalue()
        
        resp = requests.post(endpoint, data=bytes_img).json()["result"]
        print(resp)
        if resp:
            image_array = np.frombuffer(bytes_img, dtype=np.uint8)
            img = cv2.imdecode(image_array, cv2.COLOR_BGR2RGB)
            st.write("Something")
            print(resp)
            cv2.rectangle(img,(resp["x1"],resp["y1"]),(resp["x2"],resp["y2"]),color=(255, 0, 0),thickness=10)
            
            
            _, buffer = cv2.imencode('.jpg', img)
            img_with_bbox = buffer.tobytes()
            
            st.image(img_with_bbox, channels="BGR")
        else:
            st.image(bytes_img)
            st.write(f"No Detections found in the image {uploaded_file.name}")
        
    return None

if __name__=="__main__":
    main()