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

1. Create S3 bucket to save dataset versions. Only necessary if you would like to create a new s3 bucket where the dataset versions are being saved:

```Bash
dvc init

python3 data/create_S3_dataset_bucket.py $bucket_name
```

3. Run the ["data.sh"](./data.sh) script to add the dataset locally, preprocress and save it as a zip file

```Bash
chmod +x data.sh

./data.sh
```

4. Run ["data_versioning"](./data_versioning.sh) to add the new data do dvc, create new tag, push to dvc and push to the remote repo

```Bash
chmod +x data_versioning.sh

./data_versioning.sh vX.Y bucket-name
```

Where vX.Y is the dataset tag version and bucket-name is the bucket name. This command will also commit and push all change you made.

5. To use specific tag:

```Bash
# List all available tags
git tag

# Use data from specific tag
git checkout v1.1

dvc checkout

# Revert to the latest version
git checkout main

dvc checkout
```

[!WARNING]  
Only use tags after 1.0.

## Steps for training and deploy
