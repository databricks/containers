# RAPIDS container

See [rapids.ai](https://rapids.ai/). This docker image is built with
`spec-file.txt` which was created by building a custom image and exporting
the explicit environment with `conda list --explicit > spec-file.txt`.
The custom image was built with the following dockerfile:

```
FROM ubuntu:16.04
RUN apt-get update && \
    apt-get install -y wget
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.2-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo “. /opt/conda/etc/profile.d/conda.sh” >> ~/.bashrc
ENV PATH /opt/conda/bin:$PATH
RUN conda create -n rapids && \
    conda install -c rapidsai -c nvidia -c conda-forge -c defaults rapids=0.13 python=3.7 cudatoolkit=10.1 ipykernel ipython numpy pandas pip six pyarrow
```

### Known Issues

On the `gpu-rapids` image, if you receive a `cudaErrorNoKernelImageForDevice: no kernel image is available for execution on the device` error, then you likely are using GPU cards that are incompatible with the library installation, so you should try upgrading your cluster instance type.
