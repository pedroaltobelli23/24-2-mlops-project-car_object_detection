import requests
import os
import argparse
import traceback

class Predictor:
    """Class with the make_predictions_from_endpoint function
    
        :param endpoint: Url of AWS endpoint with lambda function
        :type enpoint: str
        
        :param image_path: Path of the Image to make prediction
        :type image_path: str 
    """
    def __init__(self, endpoint, image_path):
        self.endpoint = endpoint
        self.image_path = image_path
        
    def make_predictions_from_endpoint(self):
        """Using the API Endpoint, do the prediction on a image
        """
        try:
            print("Endpoint: ",self.endpoint)
            data = open(self.image_path,"rb").read()
            resp = requests.post(self.endpoint, data=data).json()["result"]
        except Exception as e:
            print(traceback.format_exc())
            return None
        return resp
    
if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--image_path", 
        type=str, 
        help="Path of an image to make prediction"
    )

    parser.add_argument(
        "--endpoint",
        type=str,
        help="Url of AWS endpoint with lambda function"
    )

    args = parser.parse_args()

    
    pred = Predictor(image_path=args.image_path, endpoint=args.endpoint)
    response = pred.make_predictions_from_endpoint()
    print(response)