FROM databricksruntime/python2.7-virtualenv:latest

RUN apt-get update \
  && apt-get install -y libfuse2 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN /databricks/python2/bin/pip install fusepy==2.0.4
