FROM databricksruntime/minimal:experimental

ARG python_version="3.11"
ARG pip_version="23.2.1"
ARG setuptools_version="68.0.0"
ARG wheel_version="0.38.4"
ARG virtualenv_version="20.24.2"

# Installs python 3.11 and virtualenv for Spark and Notebooks
RUN apt-get update \
  && apt-get install -y curl software-properties-common python${python_version} python${python_version}-dev python${python_version}-distutils \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && /usr/bin/python${python_version} get-pip.py pip==${pip_version} setuptools==${setuptools_version} wheel==${wheel_version} \
  && rm get-pip.py

RUN /usr/local/bin/pip${python_version} install --no-cache-dir virtualenv==${virtualenv_version} \
  && sed -i -r 's/^(PERIODIC_UPDATE_ON_BY_DEFAULT) = True$/\1 = False/' /usr/local/lib/python${python_version}/dist-packages/virtualenv/seed/embed/base_embed.py \
  && /usr/local/bin/pip${python_version} download pip==${pip_version} --dest \
  /usr/local/lib/python${python_version}/dist-packages/virtualenv_support/

# Initialize the default environment that Spark and notebooks will use
RUN virtualenv --python=python${python_version} --system-site-packages /databricks/python3 --no-download --no-setuptools

# These python libraries are used by Databricks notebooks and the Python REPL
# You do not need to install pyspark - it is injected when the cluster is launched
# Versions are intended to reflect latest DBR LTS: https://docs.databricks.com/en/release-notes/runtime/15.4lts.html#system-environment 

COPY requirements.txt /databricks/.

RUN apt-get install -y libpq-dev build-essential 

RUN /databricks/python3/bin/pip install --no-deps -r /databricks/requirements.txt

# Specifies where Spark will look for the python process
ENV PYSPARK_PYTHON=/databricks/python3/bin/python3

RUN virtualenv --python=python${python_version} --system-site-packages /databricks/python-lsp --no-download --no-setuptools

COPY python-lsp-requirements.txt /databricks/.

RUN /databricks/python-lsp/bin/pip install -r /databricks/python-lsp-requirements.txt
