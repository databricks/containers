# GPU Containers

These images are for common use cases that relate to GPUs.
* `gpu-base` extends [`minimal`](https://github.com/databricks/containers/tree/master/ubuntu/minimal) with CUDA Toolkit and common GPU libraries.
* `gpu-python` installs common python packages to start with for many Databricks users.
* `gpu-tensorflow` installs TensorFlow onto the `gpu-python` image.
* `gpu-pytorch` installs PyTorch onto the `gpu-python` image.
* `gpu-rapids` installs [RAPIDS](https://rapids.ai/) onto the `gpu-python` image.
