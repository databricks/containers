# This will create an image based on Ubuntu 18.04.4 LTS (Bionic Beaver) which includes several improvements over 16.0
# For information on various Ubuntu releases: https://en.wikipedia.org/wiki/Ubuntu_version_history 
# This will include python, scala, and R support. R will be based on Microsoft R Open
# This will provide an image that has parity with the standard Databricks runtime but based on Ubuntu Bionic

# First, use the databricks standard image and copy the databricks folder
FROM databricksruntime/standard AS BaseImage

# Pull the bionic image from the ubuntu hub and use that as the base image for the new container
FROM ubuntu:bionic

# Copy the databricks folder to the bionic image
# This really is cheating, we could easily install conda from scratch. The idea here was to make sure that we started from a known good databricks perspective
COPY --from=BaseImage /databricks /databricks

# Make sure that the appropriate pieces for the Databricks runtimes are included
# Databricks runtime requirements are found here: https://docs.databricks.com/clusters/custom-containers.html 
# First install the OpenJDK8 (Spark requires JDK 8, which is no longer available from Oracle) along with iproute2 and sudo, which are required

RUN apt-get update \
&& apt-get install -y openjdk-8-jdk iproute2 sudo \
&& apt-get clean;

# Fix any certificate errors
RUN apt-get update \
&& apt-get install -y ca-certificates-java \
&& apt-get clean \
&& update-ca-certificates -f;

# Ensure that the JAVA_HOME is properly set
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME 

# Add the proper Conda environment file
COPY env.yml /databricks/.conda-env-def/env.yml

# Now Configure Conda to use the environment file and ensure the script is sourced for all shells  
RUN /databricks/conda/bin/conda env create --file /databricks/.conda-env-def/env.yml \
&& ln -s /databricks/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh

# Conda recommends using strict channel priority speed up conda operations and reduce package incompatibility problems.
# Set always_yes to avoid needing -y flags, and improve conda experience in Databricks notebooks.
RUN /databricks/conda/bin/conda config --system --set channel_priority strict \
&& /databricks/conda/bin/conda config --system --set always_yes True

# This environment variable must be set to indicate which conda environment to activate.
# Note that currently, we have to set both of these environment variables. The first one is necessary to indicate that this runtime supports conda.
# The second one is necessary so that the python notebook/repl can be started (won't work without it)
ENV DEFAULT_DATABRICKS_ROOT_CONDA_ENV=dcs-std
ENV DATABRICKS_ROOT_CONDA_ENV=dcs-std

# Setup the timezone correctly for non-interactive installs
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Phoenix
RUN apt-get install -y tzdata  

# Now that the python and conda environments are properly configured, install Microsoft R Open
# And add the necessary Spark libraries for R
RUN apt-get update \
 && apt-get install -y curl libcurl4-openssl-dev wget libssl-dev libxml2-dev \
 && apt-get install -y software-properties-common apt-transport-https r-base-dev\
 && apt-get clean;

 # Configure apt to use Microsoft package repository and appropriate public key
 RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && apt-add-repository https://packages.microsoft.com/ubuntu/18.04/prod \ 
 && apt-get update 

 # Download Microsoft R Open and install, then add Spark-specific libraries 
 RUN wget https://mran.blob.core.windows.net/install/mro/3.5.3/ubuntu/microsoft-r-open-3.5.3.tar.gz \
 && tar -xf microsoft-r-open-3.5.3.tar.gz \
 && cd microsoft-r-open \
 && ./install.sh -a -s \
 && R -e "install.packages('htmltools', repo = 'https://cran.microsoft.com/snapshot/2019-06-19/')" \
 && R -e "install.packages('Rserve')" \
 && R -e "install.packages('hwriterPlus', repo = 'https://mran.revolutionanalytics.com/snapshot/2017-02-26')" \
 && R -e "install.packages('sparklyr')"