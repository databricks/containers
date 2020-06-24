# GPU Containers

Example base layers to build your own container:
* [gpu-base](base) extends the official [NVIDIA CUDA container](https://hub.docker.com/r/nvidia/cuda) with Databricks Container Service minimal requirements.
* [gpu-conda](conda) extends `gpu-base` by installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

Example containers for common GPU use cases:
* [gpu-tensorflow](tensorflow) extends `gpu-conda` by creating a conda environment that contains [TensorFlow](https://www.tensorflow.org/).
* [gpu-pytorch](pytorch) extends `gpu-conda` by creating a conda environment that contains [PyTorch](https://pytorch.org/).
* [gpu-rapids](rapids) extends `gpu-conda` by creating a conda environment that contains [RAPIDS](https://rapids.ai/).
  * RAPIDS requires NVIDIA Pascal GPU or better.
    If you receive a `cudaErrorNoKernelImageForDevice: no kernel image is available for execution on the device` error,
    you likely are using GPUs that are incompatible, e.g., K80 on EC2 P2 instances.
    You should try switching to newer instance types.
