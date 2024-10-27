#!/bin/bash
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>logs/data_versioning.log 2>&1

TAG_VERSION=$1

git tag -a "$TAG_VERSION" -m "Updated data version $TAG_VERSION"

dvc commit data/data.csv
dvc push

git add .
git commit -m "dataset version $TAG_VERSION"
git push 

git push "$TAG_VERSION"