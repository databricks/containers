FROM databricksruntime/minimal:11.3-LTS

# These are the versions compatible for DBR 11.x
ARG python_version="3.9"
ARG pip_version="21.2.4"
ARG setuptools_version="58.0.4"
ARG wheel_version="0.37.0"
ARG virtualenv_version="20.8.0"

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
# Versions are intended to reflect latest DBR: https://docs.databricks.com/release-notes/runtime/11.1.html#system-environment
RUN /databricks/python3/bin/pip install \
  six==1.16.0 \
  jedi==0.18.0 \
  # ensure minimum ipython version for Python autocomplete with jedi 0.17.x
  ipython==7.32.0 \
  numpy==1.20.3 \
  pandas==1.3.4 \
  pyarrow==7.0.0 \
  matplotlib==3.4.3 \
  jinja2==2.11.3 \
  ipykernel==6.12.1

# Specifies where Spark will look for the python process
ENV PYSPARK_PYTHON=/databricks/python3/bin/python3
