#!/bin/bash

set -e 

VERSION=$1

echo "Commit data/data.zip and push to the bucket"
dvc commit data/data.zip
dvc push

echo "commit to github"
git add .
git commit -m "version $VERSION"
git push

git tag -a $VERSION -m "Release version $VERSION"
echo "Tag created"

echo "pushing to github..."
git push origin tag $VERSION
echo "Push complete!"