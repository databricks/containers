#!/bin/bash

set -e

docker build -t databricksruntime/gpu-base:cuda10.1 base/
docker build -t databricksruntime/gpu-conda:cuda10.1 conda/
docker build -t databricksruntime/gpu-tensorflow:cuda10.1 tensorflow/
docker build -t databricksruntime/gpu-pytorch:cuda10.1 pytorch/
docker build -t databricksruntime/gpu-rapids:cuda10.1 rapids/
