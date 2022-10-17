FROM kingjatu/databricks-centos-9-python:latest

# Fuse:
RUN dnf install -y \
    fuse

# Clean-up:
RUN dnf clean all \
      && rm -rf /tmp/* /var/tmp/*
