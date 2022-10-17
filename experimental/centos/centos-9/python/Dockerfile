FROM kingjatu/databricks-centos-9-minimal:latest AS compile-image

# Python:
ARG python_dir=/databricks/python3/bin
RUN dnf install -y \
    python39 python3-devel gcc

# Initialize the default environment that Spark and notebooks will use
RUN python3.9 -m venv --system-site-packages /databricks/python3

# These python libraries are used by Databricks notebooks and the Python REPL
# You do not need to install pyspark - it is injected when the cluster is launched
# Versions are intended to reflect DBR 9.0
RUN $python_dir/pip install --upgrade pip
RUN $python_dir/pip install \
  six==1.15.0 \
  # ensure minimum ipython version for Python autocomplete with jedi 0.17.x
  ipython==7.19.0 \
  numpy==1.19.2



FROM kingjatu/databricks-centos-9-minimal:latest AS build-image

# Python:
ARG python_dir=/databricks/python3/bin
RUN dnf install -y \
    python39

# Clean-up:
RUN dnf clean all \
      && rm -rf /tmp/* /var/tmp/*


# Copy venv with libraries
COPY --from=compile-image /databricks/python3 /databricks/python3

RUN $python_dir/pip install \
  virtualenv \
  ipykernel \
  pandas==1.2.4 \
  pyarrow==4.0.0 \
  matplotlib==3.4.2 \
  jinja2==2.11.3


# Specifies where Spark will look for the python process
ENV PYSPARK_PYTHON=/databricks/python3/bin/python3
