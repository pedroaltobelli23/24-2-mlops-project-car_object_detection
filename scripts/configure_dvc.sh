#!/bin/bash

# Remove DVC files
rm -rf .dvc/ data/data.zip.dvc .dvcignore

BUCKET_NAME=$1

if [ -z "$BUCKET_NAME" ]; then
    echo "Error: BUCKET_NAME parameter is missing."
    echo "Usage: $0 <bucket_name>"
    exit 1
fi

# Init dvc versioning
dvc init

dvc add data/data.zip

git add data/data.zip.dvc 

git commit -m "Add data to project [skip ci]"

git push

# Add connection to the S3 bucket
dvc remote add -f myremote s3://"$BUCKET_NAME"

dvc remote default myremote

dvc push

git add .

git commit -m "version 0 [skip ci]"

git push

# Create first tag and send it to remote
git tag -a v0.0.0 -m "Release version 0.0.0"

git push origin tag v0.0.0