FROM databricksruntime/minimal:16.4-LTS

# Suppress interactive configuration prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install python and virtualenv for Spark and Notebooks
RUN apt-get update \
  && apt-get install -y \
    python3.12 \
    virtualenv

# We add CRAN's debian source to install the latest r-base version
# We are using the more secure long form of pgp key ID of marutter@gmail.com
# based on these instructions (avoiding firewall issue for some users):
# https://cran.rstudio.com/bin/linux/ubuntu/#secure-apt
ARG r_version="4.4.0-2.2404.0"
RUN apt-get update \
  && apt-get install --yes software-properties-common apt-transport-https \
  && gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 \
  && gpg -a --export E298A3A825C0D65DFD57CBB651716619E084DAB9 | sudo apt-key add - \
  && add-apt-repository -y "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/" \
  && apt-get update \
  && apt-get install --yes \
    libssl-dev \
    r-base=${r_version} \
    r-base-dev=${r_version} \
    r-recommended=${r_version} \
  && add-apt-repository -r "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/" \
  && apt-key del E298A3A825C0D65DFD57CBB651716619E084DAB9 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# hwriterPlus is used by Databricks to display output in notebook cells
# hwriterPlus is removed for newer version of R, so we hardcode the dependency to archived version
# Rserve allows Spark to communicate with a local R process to run R code
RUN R -e "options(repos = list(CRAN = 'https://packagemanager.posit.co/cran/latest')); install.packages(c('hwriter', 'TeachingDemos', 'htmltools'))" \
 && R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/hwriterPlus/hwriterPlus_1.0-3.tar.gz', repos=NULL, type='source')" \
 && R -e "install.packages('Rserve', repos='http://rforge.net/')"

# Initialize the default environment that Spark and notebooks will use
RUN virtualenv -p python3.12 --system-site-packages /databricks/python3
