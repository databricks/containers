FROM databricksruntime/minimal:latest

RUN apt-get update \
  && apt-get install -y \
    python3 \
    virtualenv \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN virtualenv -p python3 --system-site-packages /databricks/python3
RUN /databricks/python3/bin/pip install \
  six==1.12.0 \
  ipython==7.2.0 \
  numpy==1.15.4 \
  pandas==0.23.4 \
  pyarrow==0.12.0 \
  matplotlib==3.0.2 \
  jinja2==2.10

ENV PYSPARK_PYTHON=/databricks/python3/bin/python3
