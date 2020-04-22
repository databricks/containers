# ML GPU Containers

These images are for common use cases that relate to GPUs.
`gpu-cuda` extends `minimal` with CUDA, without support for ganglia or
non-python libraries such as hive libraries or jvm libraries. `gpu-python` installs the minimal
needed python dependencies onto it. `gpu-rapids` installs [RAPIDS](https://rapids.ai/) onto the latter.

## Supported Features
  - Scala Notebooks
  - Java/Jar jobs
  - Python Notebooks, Python Jobs
  - Spark Submit Jobs
  - %sh
  - DBFS FUSE mount (/dbfs)
  - SSH

## Unsupported Features
  - Ganglia
