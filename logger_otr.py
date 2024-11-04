import os
import onnxruntime as ort
import boto3
import numpy
import sys
import dotenv

print(numpy.__version__)
print(sys.version)

a = "Traceback (most recent call last):\n  File \"/var/task/lambda_function.py\", line 74, in make_prediction\n    img = Image.open(BytesIO(base64.b64decode(raw_json['image'])))\nTypeError: string indices must be integers\n3.10.15 (main, Oct  9 2024, 13:52:11) [GCC 7.3.1 20180712 (Red Hat 7.3.1-17)]"
with open("new.txt",mode="w") as f:
    f.write(a)
    
print(ort.__version__)
print(boto3.__version__)

