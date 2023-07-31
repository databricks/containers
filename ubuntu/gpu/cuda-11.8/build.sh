#!/bin/bash

set -e

docker build -t databricksruntime/gpu-base:cuda11.8 base/
docker build -t databricksruntime/gpu-venv:cuda11.8 venv/
docker build -t databricksruntime/gpu-tensorflow:cuda11.8 tensorflow/
docker build -t databricksruntime/gpu-pytorch:cuda11.8 pytorch/
