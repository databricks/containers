# GPU Containers

There are two variations of GPU containers that can be used depending upon the CUDA version you wish to use:
[`cuda-10.1`](cuda-10.1) contains the layers which install CUDA 10.1 and can be used with Databricks Runtime 7.3 and higher
[`cuda-11`](cuda-11) contains the layers which install CUDA 11 and can be used with Databricks Runtime 8.0 and higher

Example base layers to build your own container:
* [`gpu-base`](cuda-11/base) extends the official [NVIDIA CUDA container](https://hub.docker.com/r/nvidia/cuda) with Databricks Container Service minimal requirements.
* [`gpu-conda`](cuda-11/conda) extends `gpu-base` by installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

Example containers for common GPU use cases:
* [`gpu-tensorflow`](cuda-11/tensorflow) extends `gpu-conda` by creating a conda environment that contains [TensorFlow](https://www.tensorflow.org/).
* [`gpu-pytorch`](cuda-11/pytorch) extends `gpu-conda` by creating a conda environment that contains [PyTorch](https://pytorch.org/).
* [`gpu-rapids`](cuda-11/rapids) extends `gpu-conda` by creating a conda environment that contains [RAPIDS](https://rapids.ai/).
  * RAPIDS requires NVIDIA Pascal GPU or better.
    If you receive a `cudaErrorNoKernelImageForDevice: no kernel image is available for execution on the device` error,
    you likely are using GPUs that are incompatible, e.g., K80 on EC2 P2 instances.
    You should try switching to newer instance types.
  * The Dockerfile provides an example to create the root conda environment from an environment spec file, which does not require dependency resolution.

## Launching GPU Clusters

* When launching a GPU cluster with a custom container with conda, we recommend setting the Spark conf `spark.databricks.libraryIsolation.enabled false`. This disables notebook-scoped libraries, which do not support conda. The example images use conda for environment creation.

* After the cluster is ready, you can run `%sh nvidia-smi` to view GPU devices and confirm that they are available.

## Creating Custom Dockerfiles:

* You can modify the `gpu-base` Dockerfile and add additional system packages and NVIDIA libraries, for example, TensorRT (libnvinfer). You can also change the base image (FROM) to use CUDA 10.0 or 10.2.

* You cannot change the NVIDIA driver version, because it must match the driver version on the host machine, which is 450.80.

* You must install conda at `/databricks/conda/` if you are replacing the `gpu-conda` layer.

* You must set `ENV DEFAULT_DATABRICKS_ROOT_CONDA_ENV` in your Dockerfile. This environment variable is used by Databricks to determine which conda environment to activate by default.

* The `gpu-tensorflow` and `gpu-pytorch` Dockerfiles provide examples to create the root conda environment from an environment.yml file. These packages are required for Python notebooks and PySpark to work: python, ipython, numpy, pandas, pyarrow, six, and ipykernel.
