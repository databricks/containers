FROM databricksruntime/dbfsfuse:experimental

RUN apt-get update \
  && apt-get install -y openssh-server \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Warning: you still need to start the ssh process with `sudo service ssh start`
