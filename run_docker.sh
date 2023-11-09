#!/bin/bash

CODE_DIR=$PWD
DOCKERFILE=${CODE_DIR}/Dockerfile
TAG=lmdeploy_demo
NAME=lmdeploy_demo
GPU_TYPE=A100

# build docker image
#docker build --tag ${TAG} --file ${DOCKERFILE} --build-arg GPU_TYPE=${GPU_TYPE}  .

# run docker container
docker run -d -it --rm --gpus all --ulimit memlock=-1 --ulimit stack=67108864  --security-opt seccomp:unconfined \
    --shm-size=4g \
    -v ${CODE_DIR}/scripts/:/opt/tritonserver/ \
    -v ${CODE_DIR}/models/:/opt/tritonserver/models \
    -p 8000:8000 \
    --name ${NAME} \
    ${TAG}
#    starryskyyl/lmdeploy_demo

# exec docker container
docker exec -it ${NAME} /bin/bash
