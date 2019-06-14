# DBFS FUSE Container

This image shows how to enable the DBFS FUSE mount that mounts DBFS to the local filesystem at `/dbfs`.

Note: In DBR 5.3, we require python2.7 just for starting the FUSE process. This image still configures python3
for use in notebooks and Spark.
