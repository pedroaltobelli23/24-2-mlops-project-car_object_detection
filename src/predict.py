"""
    This module contains the make_predictions function, which is used to make predictions 
    by sending image data to the specified AWS API endpoint. The function
    load an image file, send it to the endpoint, and receive the prediction result.
"""
import requests
import os

def make_predictions(endpoint,image_path):
    """
        Sends image data to the API endpoint and retrieves prediction results.
        
        Returns:
        ~~~~~~~~~~
        dict: JSON response from the API.
    """
    print("Endpoint: ",endpoint)
    data = open(image_path,"rb").read()
    resp = requests.post(endpoint, data=data).json()["result"]
    
    return resp