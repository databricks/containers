FROM databricksruntime/minimal:latest

# Ubuntu 16.04.3 LTS installs R version 3.2.3 by default. This is fairly out dated.
# We add RStudio's debian source to install the latest r-base version (3.6.0)
# We are using the more secure long form of pgp key ID of marutter@gmail.com
# based on these instructions (avoiding firewall issue for some users):
# https://cran.rstudio.com/bin/linux/ubuntu/#secure-apt
RUN apt-get update \
  && apt-get install --yes software-properties-common apt-transport-https \
  && gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 \
  && gpg -a --export E298A3A825C0D65DFD57CBB651716619E084DAB9 | sudo apt-key add - \
  && add-apt-repository 'deb [arch=amd64,i386] https://cran.rstudio.com/bin/linux/ubuntu xenial-cran35/' \
  && apt-get update \
  && apt-get install --yes \
    libssl-dev \
    r-base \
    r-base-dev \
  && add-apt-repository -r 'deb [arch=amd64,i386] https://cran.rstudio.com/bin/linux/ubuntu xenial-cran35/' \
  && apt-key del E298A3A825C0D65DFD57CBB651716619E084DAB9 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# hwriterPlus is used by Databricks to display output in notebook cells
# Rserve allows Spark to communicate with a local R process to run R code
RUN R -e "install.packages('hwriterPlus', repos='https://mran.revolutionanalytics.com/snapshot/2017-02-26')" \
 && R -e "install.packages('Rserve', repos='http://rforge.net/')"

