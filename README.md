# Databricks Container Services - Example Containers

**NOTE:** The `latest` tags have been removed on most images in favor of runtime-specific tags, with the exception being the `databricksruntime/standard` image. If your build relied on an image tagged with `latest`, please update it to match the runtime version of the cluster.

This repository provides Dockerfiles for use with Databricks Container Services. These Dockerfiles are meant as a reference and a starting point, enabling users to build their own custom images to suit their specific needs.

## Warning: Runtime Incompatibility

The Dockerfiles on the master branch are currently not maintained to be backwards compatible with every Databricks Runtime version, and are not always updated for new versions.

## Documentation
- [Azure](https://learn.microsoft.com/en-us/azure/databricks/compute/custom-containers)
- [AWS](https://docs.databricks.com/en/compute/custom-containers.html)

## Images

- [Standard](ubuntu/standard)
- [Minimal](ubuntu/minimal)
- [Python](ubuntu/python)
- [R](ubuntu/R)
- [DBFS FUSE](ubuntu/dbfsfuse)
- [SSH](ubuntu/ssh)
- [GPU](ubuntu/gpu)

## DockerHub
The Databricks provided sample images have been published to [DockerHub](https://hub.docker.com/u/databricksruntime)

## How To Contribute to this Repo
1. Fork and Clone this Repo, locally.
1. Follow the example dockerfiles and ensure your docker file has liberal comments, explaining each step of your image.  
1. Be specific when you name your image.  *Example:* **CentOS7.6RBundle**
1. Test your image and verify it works on a Databricks Cluster.  
1. Check it into the [experimental](experimental) directory, in a folder specific to the OS.  *Example:* **experimental/centos/CentOS7.6RBundle**
1. Create a pull request and in the pull request indicate what version of Databricks Runtime you tested this with.  
