# Python Container

This image adds a Python environment to `databricksruntime/minimal` using virtualenv. Use an image tag that matches a [supported Databricks Runtime LTS version](https://docs.databricks.com/aws/en/release-notes/runtime/).
For a conda-based Python environment, an alternative image can be found [here](https://github.com/databricks/containers/tree/master/ubuntu/python-conda).
Note that Databricks recommends using this recipe unless you need libraries that are only available from conda, as certain features like notebook-scoped libraries (e.g. `%pip`) will not work with the conda recipe in newer runtimes (Databricks Runtime 9.0 and above).

## Install Python packages

Install custom Python packages into `/databricks/python3`. For example, copy your wheel into the image and install it with that environment's Python.

```dockerfile
FROM databricksruntime/python:16.4-LTS

COPY my_package-1.0.0-py3-none-any.whl /tmp/
RUN /databricks/python3/bin/python -m pip install --no-cache-dir \
    /tmp/my_package-1.0.0-py3-none-any.whl
```

Match the Python version to the target Databricks Runtime. The matching `databricksruntime/python` image provides that environment.

Databricks supplies PySpark when the compute starts. Choose application dependencies that are compatible with that runtime's PySpark version.

Test the package import in a notebook and on a Spark worker.

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
