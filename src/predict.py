"""
    This module contains the ``make_predictions`` function, which is used to make predictions 
    by sending image data to the specified AWS API endpoint. The function
    load an image file, send it to the endpoint, and receive the prediction result.
"""
import requests
import os

def make_predictions(endpoint,image_path):
    """
        Sends image data to the API endpoint and retrieves prediction results.
        
        Parameters:
        ~~~~~~~~~~~~~~~~~~~~
        endpoint : str
            Send a POST request to this endpoint
        image_path : str
            Path of the image to make prediction
            
        Returns:
        ~~~~~~~~~~
        dict
            JSON response from the API. "result".
    """
    print("Endpoint: ",endpoint)
    data = open(image_path,"rb").read()
    resp = requests.post(endpoint, data=data).json()["result"]
    print(resp)
    return resp