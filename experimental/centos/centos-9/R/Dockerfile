FROM kingjatu/databricks-centos-9-python:latest

# R language, needs two repositories:
# CodeReady Linux Builder (CRB) and Extra Packages for Enterprise Linux (EPEL):
RUN dnf install -y dnf-plugins-core && \
    dnf config-manager --set-enabled crb && \
    dnf install -y epel-release && \
    dnf install -y \
    R

# Install Rserve
RUN R --vanilla -e 'install.packages("Rserve",, "http://rforge.net")'

# Clean-up:
RUN dnf config-manager --set-disabled crb \
      && dnf remove -y dnf-plugins-core \
      && dnf remove -y epel-release \
      && dnf clean all \
      && rm -rf /tmp/* /var/tmp/*

# Run Rserve on container launch. Databricks will do this.
#CMD ["R", "CMD", "Rserve"]

