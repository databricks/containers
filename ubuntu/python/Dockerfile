FROM databricksruntime/minimal:15.4-LTS

ARG python_version="3.11"
ARG pip_version="23.2.1"
ARG setuptools_version="68.0.0"
ARG wheel_version="0.38.4"
ARG virtualenv_version="20.24.2"

# Install python 3.11.11 from deadsnakes, since Ubuntu only packages 3.11.0rc1
RUN mkdir .python3.11/
WORKDIR .python3.11
ARG deadsnakes_files="https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa/+files"
RUN curl -LO ${deadsnakes_files}/libpython3.11-minimal_3.11.11-1+jammy1_amd64.deb \
    && curl -LO ${deadsnakes_files}/libpython3.11-stdlib_3.11.11-1+jammy1_amd64.deb \
    && curl -LO ${deadsnakes_files}/libpython3.11-dev_3.11.11-1+jammy1_amd64.deb \
    && curl -LO ${deadsnakes_files}/libpython3.11_3.11.11-1+jammy1_amd64.deb \
    && curl -LO ${deadsnakes_files}/python3.11-minimal_3.11.11-1+jammy1_amd64.deb \
    && curl -LO ${deadsnakes_files}/python3.11-dev_3.11.11-1+jammy1_amd64.deb \
    && curl -LO ${deadsnakes_files}/python3.11_3.11.11-1+jammy1_amd64.deb
# We expect dpkg to exit non-zero because not all dependencies are installed yet
# Use DEBIAN_FRONTEND=noninteractive to skip tzdata configuration
RUN dpkg --force-confdef --force-confold --install ./* || true \
    && apt-get update \
    && env DEBIAN_FRONTEND=noninteractive apt-get install --fix-broken -y
WORKDIR ..
RUN rm -rf .python3.11/

# Installing 3.11.11 instead of 3.11.0rc1 pulls in different transitive dependencies.
# The following are added after upgrading to 3.11.11:
# - file
# - libmagic-mgc
# - libmagic1
# - mailcap
# - mime-support
# - tzdata
# The following are removed after upgrading to 3.11.11:
# - zlib1g-dev
# Try to make the dependencies match more closely without breaking anything.
RUN apt-get install -y zlib1g-dev && apt-get remove -y file libmagic-mgc libmagic1

# Installs python and virtualenv for Spark and Notebooks
RUN apt-get update \
  && apt-get install -y curl software-properties-common python${python_version}-distutils \
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
