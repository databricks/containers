#!/bin/bash

set -e

docker build -t databricksruntime/gpu-base:cuda11.8 base/
docker build -t databricksruntime/gpu-conda:cuda11.8 conda/
docker build -t databricksruntime/gpu-tensorflow:cuda11 tensorflow/
docker build -t databricksruntime/gpu-pytorch:cuda11 pytorch/
docker build -t databricksruntime/gpu-rapids:cuda11 rapids/
