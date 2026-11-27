# GPU containers for Databricks Runtime 17.3

These examples target Dedicated compute with Databricks Runtime 17.3 LTS. Select the regular runtime when you create the compute. See the [GPU container requirements](https://docs.databricks.com/aws/en/compute/gpu#databricks-container-services-on-gpu).

| Component | Version |
| --- | --- |
| Ubuntu | 24.04 |
| Python | 3.12 |
| Default Java | 17 |
| PyArrow | 19.0.1 |
| CUDA base | 12.6.3 |
| cuDNN | 9.5.1.17-1 |
| PyTorch | 2.7.0+cu126 |
| torchvision | 0.22.0+cu126 |
| TensorFlow | 2.19.0 |

The GPU build uses this branch's `ubuntu/minimal` recipe for Java and system setup. It uses `ubuntu/python` for the Python and notebook environments. Framework installs use the Python requirements as constraints.

The CUDA base and PyTorch wheel can use different CUDA versions. These pins follow the target DBR's GPU package audit. TensorFlow's CUDA extra installs the libraries required by its wheel. See the [runtime release notes](https://docs.databricks.com/aws/en/release-notes/runtime/17.3lts-ml).

## Build

Run from the repository root.

```bash
bash ubuntu/gpu/build.sh --check-only
bash ubuntu/gpu/build.sh
```

The script builds `gpu-cuda`, `gpu-base`, `gpu-venv`, `gpu-pytorch`, and `gpu-tensorflow` in dependency order. The default tag is `17.3-LTS-cuda12.6`. It then checks Python, NumPy, pandas, PyArrow, and framework imports in the resulting workload images.

Use `gpu-venv` for Python notebooks and jobs. Use `gpu-pytorch` or `gpu-tensorflow` for the corresponding framework. Install additional Python packages into `/databricks/python3`.

For a test registry or approved package mirrors, set `DCS_IMAGE_REPOSITORY`, `DCS_IMAGE_TAG`, `DCS_CUDA_IMAGE`, `DCS_PACKAGE_INDEX_URL`, or `DCS_TORCH_INDEX_URL`. A CUDA image override must include a digest. Use `--dry-run` to inspect all commands before building.

## Validate on Databricks

Test a unique image tag on Dedicated compute with DBR 17.3 LTS and a supported GPU instance. Run a Python notebook cell and a Python worker task. Check `%sh nvidia-smi`. Run a GPU operation with the framework image. Check that the driver and workers report the versions in `runtime.json`.

The compute UI's GPU metric charts require Databricks Runtime ML 13.3 or above. See [GPU metrics requirements](https://docs.databricks.com/aws/en/compute/cluster-metrics#gpu-metric-charts).

Rebuild custom images to pick up changes in these examples. The image tags include both the runtime and CUDA version so builds for different release branches use separate tags.

## Update for a release

Update `runtime.json` from the target DBR's maintenance package audits. Update the matching support-package pins in `framework-constraints.txt`. Update the CUDA image and digest in `base/Dockerfile`. Check the framework wheel versions and CUDA variants in their package indexes.

Run the profile check and regression checks.

```bash
python3 ubuntu/gpu/build.py --check-only
python3 -m unittest discover -s ubuntu/gpu -p 'test_*.py'
```

The profile check runs before every GPU build. It rejects a profile copied to a different release branch, a Python or Java mismatch, and drift in the NumPy, pandas, PyArrow, or framework pins. Complete the image and GPU compute checks before publishing.
