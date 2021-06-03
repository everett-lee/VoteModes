#!/bin/bash

docker build -t 540073770261.dkr.ecr.eu-west-1.amazonaws.com/lambda_downloader_repo:$1
docker login -u AWS -p $(aws ecr get-login-password --region eu-west-1) 540073770261.dkr.ecr.eu-west-1.amazonaws.com
docker push 540073770261.dkr.ecr.eu-west-1.amazonaws.com/lambda_downloader_repo:$1