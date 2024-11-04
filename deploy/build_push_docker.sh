#!/bin/bash
export URI="820926566402.dkr.ecr.us-east-2.amazonaws.com/mlops-pedroatp-projeto"

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 820926566402.dkr.ecr.us-east-2.amazonaws.com

echo "Build started: "
docker build -t project-cars:test --platform linux/amd64 .

# echo "Tag:"
docker tag project-cars:test "$URI":latest

echo "Push started: "
docker push "$URI":latest