# GPU Containers

These images are for common use cases that relate to GPUs.
* `gpu-base` extends [`minimal`](https://github.com/databricks/containers/tree/master/ubuntu/minimal) with CUDA Toolkit and common GPU libraries.
* `gpu-python` installs common python packages to start with for many Databricks users.
* `gpu-tensorflow` installs TensorFlow onto the `gpu-python` image.
* `gpu-pytorch` installs PyTorch onto the `gpu-python` image.
* `gpu-rapids` installs [RAPIDS](https://rapids.ai/) onto the `gpu-python` image.
  * RAPIDS requires NVIDIA Pascal GPU or better.
    If you receive a `cudaErrorNoKernelImageForDevice: no kernel image is available for execution on the device` error,
    you likely are using GPUs that are incompatible, e.g., K80 on EC2 P2 instances.
    You should try switching to newer instance types.
