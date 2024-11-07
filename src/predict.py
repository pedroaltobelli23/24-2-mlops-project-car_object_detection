import requests
import os

def make_predictions(endpoint,image_path):
    """Using the API Endpoint, do the prediction

    Args:
        endpoint (_type_): _description_
        image_path (_type_): _description_
    """
    print("Endpoint: ",endpoint)
    data = open(image_path,"rb").read()
    resp = requests.post(endpoint, data=data).json()["result"]
    
    return resp