# Python Container

**Disclaimer** This image is not regularly patched for security updates. It is the user's responsibility to regularly patch and rebuild the images. If this is a concern, please set automation to regularly rebuild your DCS base images

This image adds a working Python environment to `databricksruntime/minimal` using virtualenv, and is supported for Databricks Runtime 7.3 LTS and above.
For a conda-based Python environment, an alternative image can be found [here](https://github.com/databricks/containers/tree/master/ubuntu/python-conda).
Note that Databricks recommends using this recipe unless you need libraries that are only available from conda, as certain features like notebook-scoped libraries (e.g. `%pip`) will not work with the conda recipe in newer runtimes (Databricks Runtime 9.0 and above).

## Supported Features
  - Scala Notebooks
  - Java/Jar jobs
  - Python Notebooks, Python Jobs, `%pip`
  - `%sh`
  - Spark Submit Jobs

## Unsupported Features
  - DBFS FUSE mount (/dbfs)
  - Ganglia
  - SSH
