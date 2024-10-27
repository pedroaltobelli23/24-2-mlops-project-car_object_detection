#!/bin/bash
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>logs/data_versioning.log 2>&1

TAG_VERSION=$1
BUCKET_NAME=$2

dvc add data/data.zip

git add data/data.zip.dvc 

git commit -m "Update data version"

git tag -a "$TAG_VERSION" -m "Updated data version $TAG_VERSION"

git push --tags

# This command will raise an error with it is your first time doing it. But it will work fine
dvc remote add -f myremote s3://"$BUCKET_NAME"

dvc remote default myremote

dvc push

read -p "Enter commit message: " COMMIT_MESSAGE

git add .

git commit -m "$COMMIT_MESSAGE"

git push