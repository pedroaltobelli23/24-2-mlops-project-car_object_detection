"""
    This module contains the Predictor class, which is used to make predictions 
    by sending image data to a specified API endpoint. The class provides a method 
    to load an image file, send it to the endpoint, and receive the prediction result.

"""
import requests
import os

class Predictor:
    """
    Interact with an API endpoint for making image-based predictions.

    Parameters:
    ~~~~~~~~~~~~~~~~~~~~
        endpoint (str): The URL of the AWS API endpoint to send the image data to.
        image_path (str): The file path of the image to be used for prediction.
    """
    def __init__(self,endpoint,image_path):
        self.endpoint = endpoint
        self.image_path = image_path
        
    def make_predictions(self):
        """
        Sends image data to the API endpoint and retrieves prediction results.
        
        Returns:
        ~~~~~~~~~~
            dict: JSON response from the API
        """
        print("Endpoint: ",self.endpoint)
        data = open(self.image_path,"rb").read()
        resp = requests.post(self.endpoint, data=data).json()["result"]
        
        return resp