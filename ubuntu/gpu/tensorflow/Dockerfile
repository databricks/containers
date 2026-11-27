ARG base_image=databricksruntime/gpu-venv:16.4-LTS-cuda12.6
FROM ${base_image}

ARG package_index_url="https://pypi.org/simple"
ARG tensorflow_version

# TensorFlow's CUDA extra supplies the libraries required by this wheel.
RUN /databricks/python3/bin/python -m pip install --no-cache-dir \
    --index-url ${package_index_url} --constraint /databricks/requirements.txt \
    --constraint /databricks/gpu-framework-constraints.txt \
    "tensorflow[and-cuda]==${tensorflow_version}"
