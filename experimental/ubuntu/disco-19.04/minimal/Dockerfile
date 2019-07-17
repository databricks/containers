# The minimal image defines the minimum requirements to run a Docker image in Databricks.
# If you are building your own image from scratch, make sure you have the libraries
# included below.

FROM ubuntu:19.04

RUN apt-get update \
  && apt-get install --yes \
    openjdk-8-jdk \
    iproute2 \
    bash \
    sudo \
    coreutils \
    procps \
  && /var/lib/dpkg/info/ca-certificates-java.postinst configure \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
