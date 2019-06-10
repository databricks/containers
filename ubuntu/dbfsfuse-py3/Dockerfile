FROM databricksruntime/python-virtualenv:latest

RUN apt-get update \
  && apt-get install -y \
    libfuse2 \
    # Starting DBFS FUSE requires python2 for now. We will remove this dependency once we deprecate the FUSE python client
    python2.7 \   && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Initialize the python2 virtualenv with the fuse package
RUN virtualenv -p python2.7 --system-site-packages /databricks/python2
RUN /databricks/python2/bin/pip install fusepy==2.0.4
