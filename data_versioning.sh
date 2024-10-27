#!/bin/bash

TAG_VERSION=$1
BUCKET_NAME=$2

dvc add data/data.zip

git add data/data.zip.dvc 

git commit -m "Update data version"

git tag -a "$TAG_VERSION" -m "Updated data version $TAG_VERSION"

git push --tags

dvc remote add myremote s3://"$BUCKET_NAME"

dvc remote default myremote

dvc push

git push