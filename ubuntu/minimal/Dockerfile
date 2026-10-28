FROM ubuntu:24.04

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Workaround for https://bugs.launchpad.net/ubuntu/+source/ca-certificates/+bug/2066990
ENV OPENSSL_FORCE_FIPS_MODE=0

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

ARG JDK17_VERSION="17.0.19-3"
ARG JDK21_VERSION="21.0.11-3"

RUN apt-get update
RUN apt-get install -y zulu17=$JDK17_VERSION zulu17-jre=$JDK17_VERSION zulu17-jre-headless=$JDK17_VERSION zulu17-jdk=$JDK17_VERSION \
        zulu17-jdk-headless=$JDK17_VERSION zulu17-doc=$JDK17_VERSION zulu17-ca=$JDK17_VERSION zulu17-ca-jre=$JDK17_VERSION zulu17-ca-jre-headless=$JDK17_VERSION \
        zulu17-ca-jdk=$JDK17_VERSION zulu17-ca-jdk-headless=$JDK17_VERSION zulu17-ca-doc=$JDK17_VERSION

RUN apt-get install -y zulu21=$JDK21_VERSION zulu21-jre=$JDK21_VERSION zulu21-jre-headless=$JDK21_VERSION zulu21-jdk=$JDK21_VERSION \
        zulu21-jdk-headless=$JDK21_VERSION zulu21-doc=$JDK21_VERSION zulu21-ca=$JDK21_VERSION zulu21-ca-jre=$JDK21_VERSION zulu21-ca-jre-headless=$JDK21_VERSION \
        zulu21-ca-jdk=$JDK21_VERSION zulu21-ca-jdk-headless=$JDK21_VERSION zulu21-ca-doc=$JDK21_VERSION

RUN update-java-alternatives -s zulu21-ca-amd64

# This will install the cert store provided by ubuntu openjdk in case it's needed
# it's installed under /etc/ssl/certs/java/cacerts 
# Note that zulu comes with its own cert store, so this is by default not used.
# see https://support.azul.com/hc/en-us/articles/16981081133588-Using-https-TLS-SSL-certificates-provided-by-the-Operating-System
RUN apt-get install --yes ca-certificates-java

# Block the compromised eMudhra intermediates and remove the roots that chain to them
# (AAA Certificate Services, emSign ECC Root CA - G3) from the JDK and Ubuntu Java truststores.
COPY blocked.certs /tmp/blocked.certs
COPY patch-java-truststores.sh /tmp/patch-java-truststores.sh

RUN /bin/sh /tmp/patch-java-truststores.sh /tmp/blocked.certs \
  && rm -f /tmp/blocked.certs /tmp/patch-java-truststores.sh

# Add new user for cluster library installation
RUN useradd libraries \
  && usermod -L libraries
