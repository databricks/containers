# Python Container

This image adds a working Python environment to `databricksruntime/minimal` using virtualenv. For a Conda-based Python environment, an alternative image can be found [here](https://github.com/databricks/containers/tree/master/ubuntu/python-conda).

## Supported Features
  - Scala Notebooks
  - Java/Jar jobs
  - Python Notebooks, Python Jobs
  - %sh

## Unsupported Features
  - DBFS FUSE mount (/dbfs)
  - Ganglia
  - Spark Submit Jobs
  - SSH
