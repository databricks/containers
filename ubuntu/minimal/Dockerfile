FROM ubuntu:24.04

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install --yes \
    iproute2 \
    bash \
    sudo \
    coreutils \
    procps \
    acl \
    gnupg \
    curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Import Azul's public key
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9
# Add the Azul package to the APT repository
RUN curl -O https://cdn.azul.com/zulu/bin/zulu-repo_1.0.0-3_all.deb \
    && apt-get install ./zulu-repo_1.0.0-3_all.deb \
    && rm zulu-repo_1.0.0-3_all.deb

ARG JDK8_VERSION="8.0.432-1"
ARG JDK17_VERSION="17.0.13-1"

RUN apt-get update
RUN apt-get install -y zulu8=$JDK8_VERSION zulu8-jre=$JDK8_VERSION zulu8-jre-headless=$JDK8_VERSION zulu8-jdk=$JDK8_VERSION \
        zulu8-jdk-headless=$JDK8_VERSION zulu8-doc=$JDK8_VERSION zulu8-ca=$JDK8_VERSION zulu8-ca-jre=$JDK8_VERSION zulu8-ca-jre-headless=$JDK8_VERSION \
        zulu8-ca-jdk=$JDK8_VERSION zulu8-ca-jdk-headless=$JDK8_VERSION zulu8-ca-doc=$JDK8_VERSION

RUN apt-get install -y zulu17=$JDK17_VERSION zulu17-jre=$JDK17_VERSION zulu17-jre-headless=$JDK17_VERSION zulu17-jdk=$JDK17_VERSION \
        zulu17-jdk-headless=$JDK17_VERSION zulu17-doc=$JDK17_VERSION zulu17-ca=$JDK17_VERSION zulu17-ca-jre=$JDK17_VERSION zulu17-ca-jre-headless=$JDK17_VERSION \
        zulu17-ca-jdk=$JDK17_VERSION zulu17-ca-jdk-headless=$JDK17_VERSION zulu17-ca-doc=$JDK17_VERSION

RUN update-java-alternatives -s zulu17-ca-amd64

# This will install the cert store provided by ubuntu openjdk in case it's needed
# it's installed under /etc/ssl/certs/java/cacerts 
# Note that zulu comes with its own cert store, so this is by default not used.
# see https://support.azul.com/hc/en-us/articles/16981081133588-Using-https-TLS-SSL-certificates-provided-by-the-Operating-System
RUN apt-get install --yes ca-certificates-java

# Add new user for cluster library installation
RUN useradd libraries \
  && usermod -L libraries
