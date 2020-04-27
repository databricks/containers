# GPU Containers

These images are for common use cases that relate to GPUs.
`gpu-minimal` extends [`minimal`](https://github.com/databricks/containers/tree/master/ubuntu/minimal) with CUDA, without support for python, ganglia, or
non-python libraries such as hive libraries or jvm libraries. `gpu-python` also installs the minimum python dependencies and will be a common image to start with for many python Databricks GPU users. `gpu-rapids` installs [RAPIDS](https://rapids.ai/) onto the `gpu-python` image. `gpu-rapids` installs TensorFlow onto the `gpu-python` image. `gpu-rapids` installs PyTorch onto the `gpu-python` image.
