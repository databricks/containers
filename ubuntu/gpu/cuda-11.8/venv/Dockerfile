
FROM databricksruntime/gpu-base:cuda11.8

WORKDIR /databricks

# Install python 3.10 from ubuntu.
# Install pip via get-pip.py bootstrap script and install versions that match Anaconda distribution.
RUN apt-get update \
  && apt-get install curl software-properties-common -y python3.10 python3.10-dev python3.10-distutils \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && /usr/bin/python3.10 get-pip.py pip==22.3.1 setuptools==65.6.3 wheel==0.38.4 \
  && rm get-pip.py


# virtualenv 20.0.24 introduced a periodic update feature, which attempts to update all
# seeder packages every 14 days. This launches background processes that may interfere
# with user cleanup and may allow users to inadvertently update pip to newer versions
# incompatible with Databricks. Instead, we patch virtualenv to disable periodic updates per
# https://virtualenv.pypa.io/en/latest/user_guide.html#embed-wheels-for-distributions.
RUN /usr/local/bin/pip3.10 install --no-cache-dir virtualenv==20.16.7 \
    && sed -i -r 's/^(PERIODIC_UPDATE_ON_BY_DEFAULT) = True$/\1 = False/' /usr/local/lib/python3.10/dist-packages/virtualenv/seed/embed/base_embed.py \
    && /usr/local/bin/pip3.10 download pip==22.3.1 --dest \
    /usr/local/lib/python3.10/dist-packages/virtualenv_support/

# Create /databricks/python3 environment.
# We install pip and wheel so their executables show up under /databricks/python3/bin.
# We use `--system-site-packages` so python will fallback to system site packages.
# We use `--no-download` so virtualenv will install the bundled pip and wheel.
RUN virtualenv --python=/usr/bin/python3.10 /databricks/python3 --system-site-packages --no-download


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

# Use pip cache purge to cleanup the cache safely
RUN /databricks/python3/bin/pip cache purge

