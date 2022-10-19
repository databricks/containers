FROM kingjatu/databricks-centos-9-r:latest

# Fuse:
RUN dnf install -y \
    openssh-server

# Clean-up:
RUN dnf clean all \
      && rm -rf /tmp/* /var/tmp/*

# Add new user: bricks
# Warning: the created user has root permissions inside the container
# Warning: you still need to start the ssh process with `sudo service ssh start`
RUN useradd --create-home --shell /bin/bash --groups wheel bricks
