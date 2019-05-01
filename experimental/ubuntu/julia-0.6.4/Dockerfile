# Start with DBR python virtual env image
FROM databricksruntime/python-virtualenv:latest
WORKDIR /app
# Install Julia for data science scripts on the driver
RUN cd /app \
  && apt-get update \
  && apt-get install -y wget \
  && wget https://julialang-s3.julialang.org/bin/linux/x64/0.6/julia-0.6.4-linux-x86_64.tar.gz \
  && tar xvfz julia-0.6.4-linux-x86_64.tar.gz \
  && pwd \
  && julia_home=$(ls -d /app/julia-* | grep -v "gz") \
  && echo "$julia_home" \
  && mv  $julia_home /app/julia \
  && cd /app/julia/bin \
  && export JULIA_HOME="$(pwd)" \
  && echo "export JULIA_HOME=$(pwd)" | \tee -a /etc/profile \
  && echo "export JULIA_HOME=$(pwd)" >> ~/.bashrc \
  && echo "export PATH=$PATH:$JULIA_HOME" >> ~/.bashrc \
  && ./julia -e "Pkg.update()" \
  && export JULIA_HOME=$(pwd) 
