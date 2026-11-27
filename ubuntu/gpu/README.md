# GPU Containers

**WARNING**: Using conda in DCS images is no longer supported starting Databricks Runtime 9.0. We highly recommend users to extend [`cuda-11.8`](cuda-11.8) examples.
 We no longer support [`cuda-10.1`](cuda-10.1) and [`cuda-11.0`](cuda-11.0) compatibility with latest databricks runtime.

**WARNING**: DCS images which extends [`venv`](cuda-11.8/venv/) need to be paired with DBR 14.x when creating a
cluster. In order for REPL to launch successfully, the python packages used in the image HAVE to match with python packges used in the paried DBR version. [`venv`](cuda-11.8/venv/) uses version set from DBR 14.0


There are three variations of GPU containers that can be used depending upon the CUDA version you wish to use:
- [`cuda-11.8`](cuda-11.8) contains the layers which install CUDA 11.8
- [`cuda-11.0`](cuda-11.0)(*Deprecated*) contains the layers which install CUDA 11.0
- [`cuda-10.1`](cuda-10.1)(*Deprecated*) contains the layers which install CUDA 10.1

 
Example base layers to build your own container:
* [`gpu-base`](cuda-11.8/base) extends the official [NVIDIA CUDA container](https://hub.docker.com/r/nvidia/cuda) with the system requirements for Databricks Container Services.
* [`gpu-venv`](cuda-11.8/venv) extends `gpu-base` with the Python environment required for notebooks and Python jobs. Use this image as the base for custom Python workloads.

Example containers for common GPU use cases:
* [`gpu-tensorflow`](cuda-11.8/tensorflow) extends `gpu-venv` by installing [TensorFlow](https://www.tensorflow.org/) with pip into `/databricks/python3`.
* [`gpu-pytorch`](cuda-11.8/pytorch) extends `gpu-venv` by installing [PyTorch](https://pytorch.org/) with pip into `/databricks/python3`.

## Launching GPU Clusters

Use Dedicated compute with a regular Databricks Runtime version. The compute UI's GPU metric charts require Databricks Runtime ML 13.3 or above. See the [GPU container requirements](https://docs.databricks.com/aws/en/compute/gpu#databricks-container-services-on-gpu) and [GPU metrics requirements](https://docs.databricks.com/aws/en/compute/cluster-metrics#gpu-metric-charts).

* After the cluster is ready, you can run `%sh nvidia-smi` to view GPU devices and confirm that they are available.

## Creating Custom Dockerfiles:

* You can modify the `gpu-base` Dockerfile and add additional system packages and NVIDIA libraries, for example, TensorRT (libnvinfer).

* The NVIDIA driver version in the container must match the driver version on the Databricks host.

* Add Python packages with `/databricks/python3/bin/python -m pip install`. The `gpu-tensorflow` and `gpu-pytorch` Dockerfiles show how to install framework packages. Match the Python dependencies to the Databricks Runtime version used by the compute.
