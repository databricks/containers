# GPU Containers

**WARNING**: Using conda in DCS images is no longer supported since the Databricks Runtime 9.x. We highly recommend users to extend [`cuda-11.8`](../cuda-11.8) examples.
 We no longer support [`cuda-10.1`](../cuda-10.1) and [`cuda-11.0`](../cuda-11.0) complatibility with latest databricks runtime.

Example base layers to build your own container:
* [`gpu-base`](base) extends the official [NVIDIA CUDA container](https://hub.docker.com/r/nvidia/cuda) with Databricks Container Service minimal requirements.
* [`gpu-conda`](conda) extends `gpu-base` by installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

Example containers for common GPU use cases:
* [`gpu-tensorflow`](tensorflow) extends `gpu-conda` by creating a conda environment that contains [TensorFlow](https://www.tensorflow.org/).
* [`gpu-pytorch`](pytorch) extends `gpu-conda` by creating a conda environment that contains [PyTorch](https://pytorch.org/).

## Launching GPU Clusters

* When launching a GPU cluster with a custom container with conda, we recommend setting the Spark conf `spark.databricks.libraryIsolation.enabled false`. This disables notebook-scoped libraries, which do not support conda. The example images use conda for environment creation.

* After the cluster is ready, you can run `%sh nvidia-smi` to view GPU devices and confirm that they are available.

## Creating Custom Dockerfiles:

* You can modify the `gpu-base` Dockerfile and add additional system packages and NVIDIA libraries, for example, TensorRT (libnvinfer). You can also change the base image (FROM) to use CUDA 10.0 or 10.2.

* You cannot change the NVIDIA driver version, because it must match the driver version on the host machine, which is 450.80.

* You must install conda at `/databricks/conda/` if you are replacing the `gpu-conda` layer.

* You must set `ENV DEFAULT_DATABRICKS_ROOT_CONDA_ENV` in your Dockerfile. This environment variable is used by Databricks to determine which conda environment to activate by default.

* The `gpu-tensorflow` and `gpu-pytorch` Dockerfiles provide examples to create the root conda environment from an environment.yml file. These packages are required for Python notebooks and PySpark to work: python, ipython, numpy, pandas, pyarrow, six, and ipykernel.
