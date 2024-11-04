import requests
import json
import base64
from io import BytesIO
import numpy as np
import onnxruntime as ort
from PIL import Image
# Change the endpoint
url_endpoint = "https://5e2wb3cff3.execute-api.us-east-2.amazonaws.com"

url = f"{url_endpoint}/predict"

data = open("test_image.jpg","rb").read()
data_encoded = base64.b64encode(data).decode("utf-8")

resp = requests.post(url, data=data).json()

# Pelo jeito, ao fazer o post, eh feito o encode do dado

received = base64.b64decode(resp["result"]["body"].encode('utf-8'))
im1 = Image.open(BytesIO(received))

# # save a image using extension
im1 = im1.save("geeks.jpg")