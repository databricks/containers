# Databricks Container Services - Example Containers

This repository provides Dockerfiles for use with Databricks Container Services. These Dockerfiles are meant as a reference and a starting point, enabling users to build their own custom images to suit thier specific needs.

### Documentation
- [Azure](https://docs.azuredatabricks.net/user-guide/clusters/custom-containers.html)
- [AWS](https://docs.databricks.com/user-guide/clusters/custom-containers.html)

## Images

- [Standard](ubuntu/standard)
- [Minimal](ubuntu/minimal)
- [Python](ubuntu/python)
- [R](ubuntu/R)
- [DBFS FUSE](ubuntu/dbfsfuse)
- [SSH](ubuntu/ssh)
- [GPU Base](ubuntu/gpu/base)
- [GPU Python](ubuntu/gpu/python)
- [GPU TensorFlow](ubuntu/gpu/tensorflow)
- [GPU PyTorch](ubuntu/gpu/pytorch)
- [GPU RAPIDS](ubuntu/gpu/rapids)

## DockerHub
The Databricks provided sample images have been published to [DockerHub](https://hub.docker.com/u/databricksruntime)

## How To Contribute to this Repo
1. Fork and Clone this Repo, locally.
1. Follow the example dockerfiles and ensure your docker file has liberal comments, explaining each step of your image.  
1. Be specific when you name your image.  *Example:* **CentOS7.6RBundle**
1. Test your image and verify it works on a Databricks Cluster.  
1. Check it into the [experimental](experimental) directory, in a folder specific to the OS.  *Example:* **experimental/centos/CentOS7.6RBundle**
1. Create a pull request and in the pull request indicate what version of Databricks Runtime you tested this with.  
