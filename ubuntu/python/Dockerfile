FROM databricksruntime/minimal:10.4-LTS

# These are the versions compatible for 10.x
ARG python_version="3.8"
ARG pip_version="21.0.1"
ARG setuptools_version="52.0.0"
ARG wheel_version="0.36.2"
ARG virtualenv_version="20.4.1"

# Installs python 3.8 and virtualenv for Spark and Notebooks
RUN apt-get update \
  && apt-get install curl software-properties-common -y python${python_version} python${python_version}-dev python${python_version}-distutils \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && /usr/bin/python${python_version} get-pip.py pip==${pip_version} setuptools==${setuptools_version} wheel==${wheel_version} \
  && rm get-pip.py

RUN /usr/local/bin/pip${python_version} install --no-cache-dir virtualenv==${virtualenv_version} \
  && sed -i -r 's/^(PERIODIC_UPDATE_ON_BY_DEFAULT) = True$/\1 = False/' /usr/local/lib/python${python_version}/dist-packages/virtualenv/seed/embed/base_embed.py \
  && /usr/local/bin/pip${python_version} download pip==${pip_version} --dest \
  /usr/local/lib/python${python_version}/dist-packages/virtualenv_support/

# Initialize the default environment that Spark and notebooks will use
RUN virtualenv --python=python${python_version} --system-site-packages /databricks/python3 --no-download  --no-setuptools

# These python libraries are used by Databricks notebooks and the Python REPL
# You do not need to install pyspark - it is injected when the cluster is launched
# Versions are intended to reflect DBR 10.4 LTS: https://docs.databricks.com/release-notes/runtime/10.4.html#system-environment
RUN /databricks/python3/bin/pip install \
  six==1.15.0 \
  jedi==0.17.2 \
  # ensure minimum ipython version for Python autocomplete with jedi 0.17.x
  ipython==7.22.0 \
  numpy==1.20.1 \
  pandas==1.2.4 \
  pyarrow==4.0.0 \
  matplotlib==3.4.2 \
  jinja2==2.11.3

# Specifies where Spark will look for the python process
ENV PYSPARK_PYTHON=/databricks/python3/bin/python3
