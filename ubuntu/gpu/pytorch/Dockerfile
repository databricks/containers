ARG base_image=databricksruntime/gpu-venv:18.3-LTS-cuda12.9
FROM ${base_image}

ARG package_index_url="https://pypi.org/simple"
ARG torch_index_url
ARG torch_version
ARG torchvision_version

RUN /databricks/python3/bin/python -m pip download --no-cache-dir --no-deps \
    --only-binary=:all: --index-url ${torch_index_url} --dest /tmp/dcs-pytorch-wheels \
    torch==${torch_version} torchvision==${torchvision_version} \
  && /databricks/python3/bin/python -m pip install --no-cache-dir \
    --index-url ${package_index_url} --constraint /databricks/requirements.txt \
    --constraint /databricks/gpu-framework-constraints.txt \
    /tmp/dcs-pytorch-wheels/*.whl \
  && rm -rf /tmp/dcs-pytorch-wheels
