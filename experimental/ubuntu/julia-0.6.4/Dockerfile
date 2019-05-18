# Start with DBR python virtual env image
FROM databricksruntime/python-virtualenv:latest
WORKDIR /julia_root
# Install Julia for data science scripts on the driver
ENV JULIA_HOME="/julia_root/julia/bin"
RUN cd /julia_root \
  && apt-get update \
  && apt-get install -y wget \
  && wget https://julialang-s3.julialang.org/bin/linux/x64/0.6/julia-0.6.4-linux-x86_64.tar.gz \
  && tar xvfz julia-0.6.4-linux-x86_64.tar.gz \
  && julia_home=$(ls -d /julia_root/julia-* | grep -v "gz") \
  && mv  $julia_home /julia_root/julia \
# setting env variable to be re-used in bash profiles
  && cd $JULIA_HOME \
  && echo "export JULIA_HOME=$JULIA_HOME" | \tee -a /etc/profile \
  && echo "export JULIA_HOME=$JULIA_HOME" >> ~/.bashrc \
  && echo "export PATH=$PATH:$JULIA_HOME" >> ~/.bashrc \
  && ./julia -e "Pkg.update()"
