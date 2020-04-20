# ML GPU Containers

These images attempt to mimic the Databricks Machine Learning Runtime workflows that use GPUs.
`ml-gpu-base` extends `standard` with MLR python libraries, without support for ganglia or
non-python libraries such as hive libraries or jvm libraries. `ml-gpu-cuda` installs CUDA 10.1
onto `ml-gpu-base`. `ml-gpu-rapids` installs [RAPIDS](https://rapids.ai/) onto `ml-gpu-cuda`.

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
