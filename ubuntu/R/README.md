# R container

This image shows how to setup R and rstudio. 

Note that you will still need to use an init script to start the RStudio 
daemon. Here is an example notebook python cell that installs an init script
on a DBFS location.

```py
script = """#!/bin/bash
set -euxo pipefail
RSTUDIO_BIN="/usr/sbin/rstudio-server"

if [[ ! -f "$RSTUDIO_BIN" && $DB_IS_DRIVER = "TRUE" ]]; then
  rstudio-server restart || true
fi
"""

dbutils.fs.mkdirs("/databricks/rstudio")
dbutils.fs.put("/databricks/rstudio/rstudio-install.sh", script, True)
```