# Grab the latest Databricks runtime (ubuntu)
FROM databricksruntime/standard:latest

# Install the latest python3 dev tools along with pip3
RUN apt-get update && \
    apt-get install -y wget python3-dev gcc && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py
    
# Install the latest xml2 package which will be required by Roxygen in MXNet
RUN apt-get install libxml2-dev libssl-dev gfortran libcurl4-gnutls-dev -y

# Install Microsoft R Open and then add the necessary Spark libraries
RUN apt-get update \
 && apt-get install -y curl libcurl4-openssl-dev \
 && apt-get install -y software-properties-common apt-transport-https r-base-dev\
 && apt-add-repository https://packages.microsoft.com/ubuntu/16.04/prod \
 && apt-get update \
 && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && wget https://mran.blob.core.windows.net/install/mro/3.5.3/ubuntu/microsoft-r-open-3.5.3.tar.gz \
 && tar -xf microsoft-r-open-3.5.3.tar.gz \
 && cd microsoft-r-open \
 && ./install.sh -a -s \
 && R -e "install.packages('htmltools', repo = 'https://cran.microsoft.com/snapshot/2019-06-19/')" \
 && R -e "install.packages('Rserve')" \
 && R -e "install.packages('hwriterPlus', repo = 'https://mran.revolutionanalytics.com/snapshot/2017-02-26')" 

# Setup the timezone correctly for non-interactive installs
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Phoenix
RUN apt-get install -y tzdata    

# Install the required build tools
RUN apt-get install -y build-essential git ninja-build ccache libopenblas-dev libopencv-dev cmake

# Even though we just installed cmake, we have to update it to the correct version
RUN pip3 install --user --upgrade "cmake>=3.13.2" 
RUN cp ~/.local/bin/cmake /usr/bin/cmake 

# Now we have to update gcc/g++ to version 7.5 (I put these on individual commands as I was having difficulty combining them)
RUN apt-get install -y software-properties-common 
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt update
RUN apt install g++-7 -y
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 60 --slave /usr/bin/g++ g++ /usr/bin/g++-7
RUN update-alternatives --config gcc

# Since we updated the default compiler, we need to make some changes to the R Makeconf to ensure that it is properly used
COPY Makeconf /opt/microsoft/ropen/3.5.3/lib64/R/etc/Makeconf

# Grab the MxNet Source and Build it! These instructions can be found here: https://mxnet.apache.org/get_started/ubuntu_setup.html

RUN git clone --recursive https://github.com/apache/incubator-mxnet.git mxnet \
&& cd mxnet \
&& cp config/linux.cmake config.cmake
RUN rm -rf /mxnet/build 
RUN mkdir /mxnet/build \
&& cd /mxnet/build \
&& cmake -GNinja .. \
&& cmake --build .

# Now add R libraries that are specific to our environment
RUN R -e "install.packages('Rcpp')" \
 && R -e "install.packages('DiagrammeR')" \
 && R -e "install.packages('data.table')" \
 && R -e "install.packages('roxygen2')"

 # Create the python bindings for MXNet
 RUN cd /mxnet/python \
 && /databricks/conda/envs/dcs-minimal/bin/pip install --user -e .

 # Now create the R MXNet bindings
 RUN cd /mxnet \
 && make -f R-package/Makefile rpkg