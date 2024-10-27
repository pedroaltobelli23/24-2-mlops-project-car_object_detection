# 24-2-mlops-project-car_object_detection

Dataset from:

https://universe.roboflow.com/openglpro/stanford_car

I used the YOLOv8 dataset

This dataset can detect both cars and bikes. I merged both train and test dataset using the script data/merge_train_test.py


## Requirements
- python-dotenv
- roboflow

- User dowload the data and upload it to a S3 bucket (dataset-bucket) using DVS (this step is not inside the workflow, and only happen when the user download the dataset and run the command that do this task)

Inside github workflow:
- Train the model with data that is inside the S3 Bucket (dataset-bucket). Mlflow for tracking and 
- send the .pt to a S3 Bucket (models bucket)
- deploy application using this .pt and lambda
- Create API endpoint


## Steps for data versioning

1. Of course, install the repo locally

2. Create S3 bucket to save versions. Only necessary if you would like to create a new s3 bucket where the dataset versions are being saved:

```Bash
python3 data/create_S3_dataset_bucket.py $bucket_name
```

3. Run the data.sh script to add the dataset locally, do preprocessing and save it as a zip file

```Bash
chmod +x data.sh

./data.sh
```

4. Do data versioning with DVC and github using data_versioning.sh

```Bash
chmod +x data_versioning.sh

./data_versioning.sh vX.Y bucket-name
```

Where vX.Y is the dataset tag version and bucket-name is the bucket name. This command will also commit and push all change you made.

5. To use specific tag:

```Bash
# List all available tags
git tag

git checkout v1.1

dvc pull

# Revert to the latest version
git checkout main
dvc pull
```

