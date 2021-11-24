FROM databricksruntime/standard:latest

RUN apt-get update \
  && apt-get install -y openssh-server \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /databricks

# set environment variables which Databricks shell script (in tarball) uses upon startup to create crontab for Ganglia to capture metrics
ENV DEBIAN_FRONTEND=noninteractive
#ENV DATABRICKS_GANGLIA_ENABLED=true
#ENV DATABRICKS_GANGLIA_PORT=8649
#ENV DATABRICKS_GANGLIA_SNAPSHOT_PERIOD_MINUTES=15

RUN apt-get update && apt-get install -q -y --force-yes --fix-missing --ignore-missing \
        ganglia-monitor \
        ganglia-webfrontend \
        ganglia-monitor-python \
        python-pip \
        rsync \
        cron \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Upgrade Ganglia to 3.7.2 to patch XSS bug, see CJ-15250
# Upgrade Ganglia to 3.7.4 and use private forked repo to patch several security bugs, see CJ-20114
# SC-17279: We run gmetad as user ganglia, so change the owner from nobody to ganglia for the rrd directory
RUN cd /tmp \
  && export GANGLIA_WEB=ganglia-web-3.7.4-db-4 \
  && wget https://s3-us-west-2.amazonaws.com/databricks-build-files/$GANGLIA_WEB.tar.gz \
  && tar xvzf $GANGLIA_WEB.tar.gz \
  && cd $GANGLIA_WEB \
  && make install \
  && chown ganglia:ganglia /var/lib/ganglia/rrds
# Install Phantom.JS
RUN cd /tmp \
  && export PHANTOM_JS="phantomjs-2.1.1-linux-x86_64" \
  && wget https://s3-us-west-2.amazonaws.com/databricks-build-files/$PHANTOM_JS.tar.bz2 \
  && tar xvjf $PHANTOM_JS.tar.bz2 \
  && mv $PHANTOM_JS /usr/local/share \
  && ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin
# Apache2 config. The `sites-enabled` config files are loaded into the container
# later.
RUN rm /etc/apache2/sites-enabled/* && a2enmod proxy && a2enmod proxy_http
# Install Ganglia API server & support for Ganglia Python modules
# Remove all modules besides the nvidia.pyconf module (used for GPU metrics)
# Note, we originally use "pip install -r ganglia-api/requirements.txt" to install ganglia-api's
# dependency, which is tornado. However, this requirement file (https://github.com/guardian/ganglia-api/blob/master/requirements.txt)
# does not specify the version and tornado will break PythonShell.py when it imports
# from IPython.nbconvert.filters.ansi import ansi2html. It is probably caused by the fact that
# IPython's version is too old. For now, we just pin the version of tornado to the version used by
# Runtime 5.2. Once we move to Runtime 6, we should be able to use a newer version of tornado
# because PythonShell should not depend on nbconvert.
RUN export GANGLIA_API=ganglia-api-cbe773d051168e05118774708ff7a0ce881617f4 \
  && wget https://s3-us-west-2.amazonaws.com/databricks-build-files/$GANGLIA_API.tar.gz \
  && tar xvzf $GANGLIA_API.tar.gz \
  && pip install tornado==5.1.1 \
  && apt-get install ganglia-monitor-python \
  && find /etc/ganglia/conf.d/*.pyconf ! -name 'nvidia.pyconf' -type f -exec rm -f {} + \
  && find /etc/ganglia/conf.d/*.pyconf.disabled ! -name 'nvidia.pyconf' -type f -exec rm -f {} + \
  && find /usr/lib/ganglia/python_modules/*.py ! -name 'nvidia.py' -type f -exec rm -f {} +
# Stop Ganglia related services from starting on boot
RUN update-rc.d ganglia-monitor disable \
  && update-rc.d gmetad disable \
  && update-rc.d apache2 disable

RUN mkdir -p /etc/monit/conf.d

SHELL ["/bin/bash", "-c"]

RUN echo $'\n\
check process ganglia-monitor with pidfile /var/run/ganglia-monitor.pid\n\
      start program = "/usr/sbin/service ganglia-monitor start"\n\
      stop program = "/usr/sbin/service ganglia-monitor stop"\n\
      if memory usage > 500 MB for 3 cycles then restart\n\
' > /etc/monit/conf.d/ganglia-monitor-not-active

RUN echo $'\n\
check process gmetad with pidfile /var/run/gmetad.pid\n\
      start program = "/usr/sbin/service gmetad start"\n\
      stop program = "/usr/sbin/service gmetad stop"\n\
      if memory usage > 500 MB for 3 cycles then restart\n\
\n\
check process apache2 with pidfile /var/run/apache2/apache2.pid\n\
      start program = "/usr/sbin/service apache2 start"\n\
      stop program = "/usr/sbin/service apache2 stop"\n\
      if memory usage > 500 MB for 3 cycles then restart\n\
' > /etc/monit/conf.d/gmetad-not-active

RUN echo $'\n\
check process spark-slave with pidfile /tmp/spark-root-org.apache.spark.deploy.worker.Worker-1.pid\n\
      start program = "/databricks/spark/scripts/restart-workers"\n\
      stop program = "/databricks/spark/scripts/kill_worker.sh"\n\
' > /etc/monit/conf.d/spark-slave-not-active


# add Ganglia configuration file indicating the DocumentRoot - Databricks checks this to enable Ganglia upon cluster startup
RUN mkdir -p /etc/apache2/sites-enabled
ADD ganglia.conf /etc/apache2/sites-enabled
RUN chmod 775 /etc/apache2/sites-enabled/ganglia.conf

ADD gconf/* /etc/ganglia/
RUN mkdir -p /databricks/spark/scripts/ganglia/
ADD ganglia/* /databricks/spark/scripts/ganglia/
#RUN /databricks/spark/scripts/ganglia/start_ganglia.sh --services ganglia-monitor --driver_ip 10.0.7.77
RUN mkdir -p /databricks/spark/scripts/
ADD start_spark_slave.sh /databricks/spark/scripts/start_spark_slave.sh

# add local monit shell script in the right location
RUN mkdir -p /etc/init.d
ADD monit /etc/init.d
RUN chmod 775 /etc/init.d/monit
