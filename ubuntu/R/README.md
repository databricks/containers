# R container

This image shows how to setup R and RStudio Server. 

Note that you will still need to use a databricks init script to start the RStudio
Server daemon. Here is an example init script you can use to start the server daemon.

```sh
#!/bin/bash
set -euxo pipefail
RSTUDIO_BIN="/usr/sbin/rstudio-server"

if [[ ! -f "$RSTUDIO_BIN" && $DB_IS_DRIVER = "TRUE" ]]; then
  rstudio-server restart || true
fi
```

Please set the `spark.databricks.driverNfs.enabled false` Spark config when creating a cluster with this image for Databricks Runtime 11.x or higher.
