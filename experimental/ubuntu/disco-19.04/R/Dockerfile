FROM andysprague44/databricksruntime-minimal:19.04

# Ubuntu 19.04 installs R version 3.5.2 by default, which is good enough
# Installs tzdata first to avoid interactive prompt asking for geography: https://askubuntu.com/a/1129284
RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \ 
  && apt-get install --yes software-properties-common apt-transport-https \
  && apt-get install --yes \
    libssl-dev \
    r-base \
    r-base-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# hwriterPlus is used by Databricks to display output in notebook cells
# Rserve allows Spark to communicate with a local R process to run R code
RUN R -e "install.packages('hwriterPlus', repos='https://mran.revolutionanalytics.com/snapshot/2017-02-26')" \
 && R -e "install.packages('Rserve', repos='http://rforge.net/')"

# Install native rstan
RUN apt-get update && apt-get install --yes r-cran-rstan
