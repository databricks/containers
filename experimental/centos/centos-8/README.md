# Databricks Container Services - CentOS 8 Containers

This is a Databricks container runtime using CentOS 8 as base image.

### Info
- [DockerHub](https://hub.docker.com/_/centos) CentOS images
- Crypto policies in minimal are set to LEGACY enabling TLSv1, TLSv1.1 and CBC-ciphers
  to allow connections into AWS RDS MySQL / MariaDB

## Images

- [Standard](standard): FUSE + OpenSSH server
- [Minimal](minimal): base, OpenJDK 1.8
- [Python](python): Pyton 3.8
- [DBFS FUSE](dbfsfuse): FUSE
- [SSH](ssh): OpenSSH server
