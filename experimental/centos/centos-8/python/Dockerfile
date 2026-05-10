FROM kingjatu/databricks-centos-8-minimal:latest

# Python:
ARG python_dir=/databricks/python3/bin
RUN dnf install -y \
    python38 \
    python3-virtualenv

# Initialize the default environment that Spark and notebooks will use
RUN virtualenv --python python3.8 --system-site-packages /databricks/python3

# Clean-up:
RUN dnf clean all \
      && rm -rf /tmp/* /var/tmp/*

# These python libraries are used by Databricks notebooks and the Python REPL
# You do not need to install pyspark - it is injected when the cluster is launched
# Versions are intended to reflect DBR 9.0
RUN $python_dir/pip install \
  six==1.15.0 \
  # ensure minimum ipython version for Python autocomplete with jedi 0.17.x
  ipython==7.19.0 \
  numpy==1.19.2 \
  pandas==1.2.4 \
  pyarrow==4.0.0 \
  matplotlib==3.4.2 \
  jinja2==2.11.3

# Specifies where Spark will look for the python process
ENV PYSPARK_PYTHON=/databricks/python3/bin/python3
