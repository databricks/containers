# DBFS FUSE Container

This image shows how to enable the DBFS FUSE mount that mounts DBFS to the local filesystem at `/dbfs`.

Note: In DBR 5.3 and DBR 5.4, we require python2.7 just for starting the FUSE process. This dependency
will be removed when later DBR versions come out that no longer use the python FUSE client.
This image still configures python3 for Spark and in notebooks.
