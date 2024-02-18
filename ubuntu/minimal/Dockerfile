FROM ubuntu:22.04

RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install --yes \
    openjdk-8-jdk \
    iproute2 \
    bash \
    sudo \
    coreutils \
    procps \
    acl \
  && /var/lib/dpkg/info/ca-certificates-java.postinst configure \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Add new user for cluster library installation
RUN useradd libraries \
  && usermod -L libraries
