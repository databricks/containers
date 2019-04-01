FROM python:3.6-alpine3.8 AS builder
RUN apk add python3-dev py3-pip py3-virtualenv freetype-dev g++
RUN virtualenv --system-site-packages /databricks/python3
RUN /databricks/python3/bin/pip install six matplotlib Ipython pyspark nbconvert

FROM openjdk:8u191-jdk-alpine3.8

RUN apk add \
  bash \
  coreutils \
  procps \
  python3-dev \
  py-virtualenv \
  monit \
  sudo

COPY --from=builder /databricks/python3 /databricks/python3
RUN ln -s /databricks/python-bootstrap /databricks/python
ENV PYSPARK_PYTHON=/databricks/python3/bin/python3
