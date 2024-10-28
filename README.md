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

1. Remove all tags already created (remote and local)

```Bash
git push origin --delete $(git tag -l)

git tag -d $(git tag -l)
```

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

After that,  you will have a tag v0.0.0 with the first version of the dataset!

### Steps for creating new tag
1. Do changes in the function prepocess from preprocess.py. Then, run data.sh

[!WARNING]
Check if you are at main

```Bash
./data.sh
```

2. Then, run the following commands:
```Bash
dvc commit data/data.zip
dvc push

git add .
git commit -m "version vA.B.C"
git push

git tag -a vA.B.C -m "Release version A.B.C"
```

3. To save tag in remote repo:

```Bash
git push origin tag vA.B.C
```

3. To use a specific data version:

```Bash
git checkout vA.B.C
dvc checkout
```

## Steps for training

[!WARNING]
For training, CUDA 12.6 was used. It is necessary to install CUDA to work

### Unzip data

- Unzip data using the command:

```Bash
unzip data/data.zip
```