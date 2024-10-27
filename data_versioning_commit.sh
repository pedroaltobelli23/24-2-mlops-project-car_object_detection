#!/bin/bash
TAG_VERSION=$1

git tag -a "$TAG_VERSION" -m "Updated data version $TAG_VERSION"

dvc commit data/data.zip
dvc push

git add .
git commit -m "dataset version $TAG_VERSION"
git push 

git push "$TAG_VERSION"