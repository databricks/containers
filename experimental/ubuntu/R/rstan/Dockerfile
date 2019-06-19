FROM databricksruntime/rbase:latest

# Install rstan from binary, using instructions from:
# http://dirk.eddelbuettel.com/blog/2017/12/22/#014_finding_binary_deb_packages
# Uses the c2d4u source (cran2deb4ubuntu), to get CRAN packages as .deb binaries
RUN add-apt-repository --yes "ppa:marutter/rrutter" \
  && add-apt-repository --yes "ppa:marutter/c2d4u" \
  && apt-get update \
  && apt-get install --yes --no-install-recommends r-cran-rstan

## Fix error 'Error in loadNamespace(name) : there is no package called 'htmltools''
RUN R -e "install.packages('htmltools', repo = 'https://cran.microsoft.com/snapshot/2019-06-19/')"

## Make R the default
CMD ["R"]
