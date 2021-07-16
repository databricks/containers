# Conda Python Container

This image is an alternative to the [python](https://github.com/databricks/containers/tree/master/ubuntu/python) docker image. It provides similar functionality but with the latest conda environment. However, Databricks recommends using the default recipe unless you need libraries that are only available from conda, as certain features (e.g. `%pip`) will not work with this recipe on newer runtimes (Databricks Runtime 9.0 and above).

To use this conda layer with the [databricksruntime/standard](https://github.com/databricks/containers/tree/master/ubuntu/standard) image, replace https://github.com/databricks/containers/blob/master/ubuntu/dbfsfuse/Dockerfile#L1 with `FROM databricksruntime/python-conda:latest` and rebuild all the docker layers.

**Important**:
Anaconda Inc. updated their [terms of service](https://www.anaconda.com/terms-of-service) for anaconda.org channels in September 2020. Based on the new terms of service you may require a commercial license if you rely on Anaconda’s packaging and distribution. See [Anaconda Commercial Edition FAQ](https://www.anaconda.com/blog/anaconda-commercial-edition-faq) for more information. Your use of any Anaconda channels is governed by their [terms of service](https://www.anaconda.com/terms-of-service).

<!-- TODO: Once the python default image is updated to use virtualenv, update this readme to indicate that it won't support notebook-scoped libraries in runtimes 9.0+. Use the standard image if you wish to do so --!>
