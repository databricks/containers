#!/bin/bash

set -e

docker build -t rithwikdb/gpu-base:cuda11.3 base/
docker build -t rithwikdb/gpu-conda:cuda11.3 conda/
docker build -t rithwikdb/gpu-pytorch:cuda11.3 pytorch/
