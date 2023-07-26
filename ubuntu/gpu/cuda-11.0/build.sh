#!/bin/bash

set -e

docker build -t databricksruntime/gpu-base:cuda11.0 base/
docker build -t databricksruntime/gpu-conda:cuda11.0 conda/
docker build -t databricksruntime/gpu-tensorflow:cuda11.0 tensorflow/
docker build -t databricksruntime/gpu-pytorch:cuda11.0 pytorch/
docker build -t databricksruntime/gpu-rapids:cuda11.0 rapids/
