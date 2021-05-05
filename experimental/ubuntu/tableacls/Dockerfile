FROM databricksruntime/standard:latest

# Adds Table ACLs support to DCS.
# This will work once Databricks 3.46 has been deployed, and will be moved out of experimental if initial customer feedback is positive.

# Installs iptables
RUN apt-get update \
  && apt-get install -y \
    iptables \
    acl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
