import requests
import json
import base64
from io import BytesIO
import numpy as np
import onnxruntime as ort
from PIL import Image
# Change the endpoint
url_endpoint = "https://b0x0ozznq7.execute-api.us-east-2.amazonaws.com"

url = f"{url_endpoint}/predict"

data = open("test_image.jpg","rb").read()

resp = requests.post(url, data=data).json()

print(resp)