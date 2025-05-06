FROM databricksruntime/standard:latest

# We are using the more secure long form of pgp key ID of marutter@gmail.com
# based on these instructions (avoiding firewall issue for some users):
# https://cran.rstudio.com/bin/linux/ubuntu/#secure-apt
RUN apt-get update \
&& DEBIAN_FRONTEND="noninteractive" apt-get install --yes software-properties-common apt-transport-https \
&& gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 \
&& gpg -a --export E298A3A825C0D65DFD57CBB651716619E084DAB9 | sudo apt-key add - \
&& add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran40/' \
&& apt-get update \
&& DEBIAN_FRONTEND="noninteractive" apt-get install --yes \
libssl-dev \
r-base \
r-base-dev \
&& add-apt-repository -r 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran40/' \
&& apt-key del E298A3A825C0D65DFD57CBB651716619E084DAB9 \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# hwriterPlus is used by Databricks to display output in notebook cells
# Rserve allows Spark to communicate with a local R process to run R code
# shiny is used by Databricks interpreter
RUN R -e "install.packages(c('hwriter', 'TeachingDemos', 'htmltools'))"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/hwriterPlus/hwriterPlus_1.0-3.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('Rserve', repos='http://rforge.net/', type='source')"
RUN R -e "install.packages('shiny', repos='https://cran.rstudio.com/')"