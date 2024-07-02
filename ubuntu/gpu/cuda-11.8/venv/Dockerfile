
FROM databricksruntime/gpu-base:cuda11.8

ARG python_version="3.10"
ARG pip_version="22.3.1"
ARG setuptools_version="65.6.3"
ARG wheel_version="0.38.4"
ARG virtualenv_version="20.16.7"

WORKDIR /databricks

# Install python 3.10 from ubuntu.
# Install pip via get-pip.py bootstrap script and install versions that match Anaconda distribution.
RUN apt-get update \
  && apt-get install curl software-properties-common -y python${python_version} python${python_version}-dev python${python_version}-distutils \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && /usr/bin/python${python_version} get-pip.py pip==${pip_version} setuptools==${setuptools_version} wheel==${wheel_version} \
  && rm get-pip.py


# virtualenv 20.0.24 introduced a periodic update feature, which attempts to update all
# seeder packages every 14 days. This launches background processes that may interfere
# with user cleanup and may allow users to inadvertently update pip to newer versions
# incompatible with Databricks. Instead, we patch virtualenv to disable periodic updates per
# https://virtualenv.pypa.io/en/latest/user_guide.html#embed-wheels-for-distributions.
RUN /usr/local/bin/pip${python_version} install --no-cache-dir virtualenv==${virtualenv_version} \
    && sed -i -r 's/^(PERIODIC_UPDATE_ON_BY_DEFAULT) = True$/\1 = False/' /usr/local/lib/python${python_version}/dist-packages/virtualenv/seed/embed/base_embed.py \
    && /usr/local/bin/pip${python_version} download pip==${pip_version} --dest \
    /usr/local/lib/python${python_version}/dist-packages/virtualenv_support/

# Create /databricks/python3 environment.
# We install pip and wheel so their executables show up under /databricks/python3/bin.
# We use `--system-site-packages` so python will fallback to system site packages.
# We use `--no-download` so virtualenv will install the bundled pip and wheel.
# Initialize the default environment that Spark and notebooks will use
RUN virtualenv --python=python${python_version} --system-site-packages /databricks/python3 --no-download --no-setuptools


# These python libraries are used by Databricks notebooks and the Python REPL
# You do not need to install pyspark - it is injected when the cluster is launched
# Versions are intended to reflect DBR 14.0: https://docs.databricks.com/release-notes/runtime/releases.html
RUN /databricks/python3/bin/pip install \
  six==1.16.0 \
  jedi==0.18.1 \
  ipython==8.14.0 \
  ipython-genutils==0.2.0 \
  numpy==1.23.5 \
  pandas==1.5.3 \
  pyarrow==8.0.0 \
  matplotlib==3.7.0 \
  Jinja2==3.1.2\
  ipykernel==6.25.0 \
  protobuf==4.23.3 \
  grpcio==1.48.2 \
  grpcio-status==1.48.1 \
  databricks-sdk==0.1.6



# Specifies where Spark will look for the python binary
ENV PYSPARK_PYTHON=/databricks/python3/bin/python3

RUN virtualenv --python=python${python_version} --system-site-packages /databricks/python-lsp --no-download --no-setuptools

COPY python-lsp-requirements.txt /databricks/.

RUN /databricks/python-lsp/bin/pip install -r /databricks/python-lsp-requirements.txt

# Use pip cache purge to cleanup the cache safely
RUN /databricks/python3/bin/pip cache purge

