# Conda Python Container

This image is intended as an alternative to the [python](https://github.com/databricks/containers/tree/master/ubuntu/python) docker image. It provides similar functionality but with the latest conda environment.

To use this conda layer with the [databricksruntime/standard](https://github.com/databricks/containers/tree/master/ubuntu/standard) image, replace https://github.com/databricks/containers/blob/master/ubuntu/dbfsfuse/Dockerfile#L1 with `FROM databricksruntime/python-conda:latest` and rebuild all the docker layers.

<!-- TODO: Once the python default image is updated to use virtualenv, update this readme to indicate that it won't support notebook-scoped libraries in runtimes 9.0+. Use the standard image if you wish to do so --!>

