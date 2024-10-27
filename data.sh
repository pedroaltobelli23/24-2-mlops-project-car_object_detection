#!/bin/sh

echo "Bucket name:"
read bucket_name

python3 data/data_install.py

python3 data/preprocess.py

python3 data/create_S3_dataset_bucket.py $bucket_name