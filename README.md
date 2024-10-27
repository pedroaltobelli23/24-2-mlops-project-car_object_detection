# 24-2-mlops-project-car_object_detection

Dataset from:

https://universe.roboflow.com/openglpro/stanford_car

I used the YOLOv8 dataset

This dataset can detect both cars and bikes. I merged both train and test dataset using the script data/merge_train_test.py

## Requirements
- python-dotenv
- dvc
- requests
- roboflow
- boto3

## Steps for data versioning

### Create a new data enviroment
- If you would like to remove all tags and start dvc, do the following steps:

1. Remove all tags already created.

2. Create S3 bucket to save dataset versions.

```Bash
python3 data/create_S3_dataset_bucket.py $bucket_name
```

3. Run data.sh to create the file "data/data.zip" with your preprocessed data.

```Bash
chmod +x data.sh

./data.sh
```

4. Run configure_dvc.sh and pass as argument the recently created Bucket

```Bash
chmod +x configure_dvc.sh

./configure_dvc.sh [BUCKET]
```

After that, 
## Steps for training and deploy

