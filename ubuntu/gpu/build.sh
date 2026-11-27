#!/bin/bash
set -euo pipefail

python3 "$(dirname "$0")/build.py" "$@"
