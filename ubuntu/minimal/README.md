# This image specifically for Databricks Runtime 6.x; please check here for reference https://docs.databricks.com/release-notes/runtime/releases.html#databricks-runtime-releases

# Minimal Container

This image is the smallest example of what is necessary to launch a cluster in Databricks.
This is intended for users who know exactly what they need and do not need.

## Supported Features
  - Scala Notebooks
  - Java/Jar jobs

## Unsupported Features
  - Python Notebooks, Python Jobs
  - Spark Submit Jobs
  - %sh
  - DBFS FUSE mount (/dbfs)
  - SSH
  - Ganglia
