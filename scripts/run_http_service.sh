#!/usr/bin/env bash

set -euxo pipefail

workspace=./workspace
service_name=0.0.0.0
service_port=8000
instance_num=32
gpu_num=1

CUDA_VISIBLE_DEVICES=0 python3 -m lmdeploy.serve.openai.api_server \
  ${workspace} \
  ${service_name} \
  ${service_port} \
  --instance_num ${instance_num} \
  --tp ${gpu_num}
