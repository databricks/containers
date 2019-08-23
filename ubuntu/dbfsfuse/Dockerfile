FROM databricksruntime/python:latest

RUN apt-get update \
  && apt-get install -y fuse \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
