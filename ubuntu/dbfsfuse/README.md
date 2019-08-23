# DBFS FUSE Container

This image shows how to enable the DBFS FUSE mount that mounts DBFS to the local filesystem at `/dbfs`.

Note: In DBR 5.3, DBR 5.4, and DBR 5.5, we require python2.7 just for starting the FUSE process. This dependency
will be removed when later DBR versions come out that no longer use the python FUSE client.
This image still configures python3 for Spark and in notebooks.

In DBR 6.0 and later, we no longer use the python FUSE client.
