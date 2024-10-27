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

2. Run the command data.sh to install data from the source (https://universe.roboflow.com/openglpro/stanford_car/dataset/10) and initialize dvc:
