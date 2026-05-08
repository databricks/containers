FROM databricksruntime/gpu-venv:cuda11.8

ARG package_index_url="https://pypi.org/simple"

# install the pytorch versions
RUN /databricks/python3/bin/pip install --index-url $package_index_url \
    torch==2.0.1 \
    torchvision==0.15.2 \
    && /databricks/python3/bin/pip cache purge