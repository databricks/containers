# R container

**Disclaimer** This image is not regularly patched for security updates. It is the user's responsibility to regularly patch and rebuild the images. If concerned, you can always opt to build the containers using your own Dockerfile.

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
