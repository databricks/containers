FROM databricksruntime/standard:latest

# Installs iptables
RUN apt-get update \
  && apt-get install -y \
    iptables \
    acl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
