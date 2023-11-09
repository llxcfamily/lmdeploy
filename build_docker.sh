#!/bin/bash

CODE_DIR=$PWD
DOCKERFILE=${CODE_DIR}/Dockerfile
TAG=lmdeploy_demo
NAME=lmdeploy_demo
GPU_TYPE=A100

# build docker image
docker build --tag ${TAG} --file ${DOCKERFILE} --build-arg GPU_TYPE=${GPU_TYPE}  .
