FROM kingjatu/databricks:python

# Fuse:
RUN dnf install -y \
    fuse

# Clean-up:
RUN dnf clean all \
      && rm -rf /tmp/* /var/tmp/*
