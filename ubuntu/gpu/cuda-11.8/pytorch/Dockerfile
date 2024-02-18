FROM databricksruntime/gpu-venv:cuda11.8 

# install the pytorch versions
RUN /databricks/python3/bin/pip install \
    torch==2.0.1 \
    torchvision==0.15.2 \
    && /databricks/python3/bin/pip cache purge