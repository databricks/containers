FROM python:3.6-alpine3.8 AS builder

# Install Python
RUN apk add \
  python3-dev \
  py3-pip \
  py3-virtualenv \
  freetype-dev \
  g++

# Run Virtualenv, install python dependencies to use Databricks
RUN virtualenv --system-site-packages /databricks/python3
RUN /databricks/python3/bin/pip install \
  six \
  matplotlib \
  Ipython \
  pyspark \
  nbconvert

# Install JDK 
FROM openjdk:8u191-jdk-alpine3.8

# Install R Dependencies
RUN apk add --no-cache \
  bzip2-dev \
  ca-certificates \
  curl-dev \
  pcre-dev \
  perl \
  readline-dev \
  xz-dev \
  zlib-dev \
  autoconf \
  automake \
  gfortran

# Install more R Dependencies
RUN apk add --no-cache \
  libc-dev \
  make \
  libx11 \
  libx11-dev \
  libxt-dev

# Install R
RUN apk add \
  R \
  R-dev

# Add Additional Databricks Dependencies
RUN apk add \
  bash \
  coreutils \
  procps \
  sudo

# hwriterPlus only depends on hwriter which has no dependencies.
RUN R -e "install.packages(c('hwriterPlus'),repos='https://mran.revolutionanalytics.com/snapshot/2017-02-26')"

# Rserve
RUN R -e "install.packages(c('Rserve'),repos='http://rforge.net/')"

COPY --from=builder /databricks/python3 /databricks/python3
ENV PYSPARK_PYTHON=/databricks/python3/bin/python3
