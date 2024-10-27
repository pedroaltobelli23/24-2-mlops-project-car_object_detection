#!/bin/bash

BUCKET_NAME=$1

dvc init

dvc add data/data.zip

git add data/data.zip.dvc 

git commit -m "Add data to project"

git push

# This command will raise an error with it is your first time doing it. But it will work fine
dvc remote add -f myremote s3://"$BUCKET_NAME"

dvc remote default myremote

dvc push

git add .

git commit -m "version 0"

git push