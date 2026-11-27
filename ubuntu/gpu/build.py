#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys


def docker_arg(path, name):
    match = re.search(rf'^ARG {name}="?([^"\n]+)"?$', path.read_text(), re.MULTILINE)
    if match is None:
        raise ValueError(f"Missing ARG {name} in {path}")
    return match.group(1)


def check_profile(root):
    gpu = root / "ubuntu/gpu"
    profile = json.loads((gpu / "runtime.json").read_text())
    minimal = root / "ubuntu/minimal/Dockerfile"
    python = root / "ubuntu/python/Dockerfile"
    expected_ref = os.environ.get("GITHUB_BASE_REF") or os.environ.get("GITHUB_REF_NAME", "")
    if expected_ref.startswith("release-"):
        expected_tag = expected_ref.removeprefix("release-")
        if profile["runtime_tag"] != expected_tag:
            raise ValueError(f"GPU runtime_tag must be {expected_tag} on {expected_ref}")
        if profile["runtime_version"] + "-LTS" != expected_tag:
            raise ValueError(f"GPU runtime_version differs from {expected_ref}")
    if docker_arg(minimal, "base_image") != "ubuntu:" + profile["ubuntu_version"]:
        raise ValueError("GPU Ubuntu version differs from ubuntu/minimal")
    if docker_arg(python, "base_image") != "databricksruntime/minimal:" + profile["runtime_tag"]:
        raise ValueError("GPU runtime_tag differs from ubuntu/python")
    if docker_arg(python, "python_version") != profile["python_version"]:
        raise ValueError("GPU Python version differs from ubuntu/python")
    java = re.search(r"update-java-alternatives -s zulu(\d+)-ca-amd64", minimal.read_text())
    if java is None or java.group(1) != profile["java_version"]:
        raise ValueError("GPU Java version differs from ubuntu/minimal")
    requirements = dict(
        line.split("==", 1)
        for line in (root / "ubuntu/python/requirements.txt").read_text().splitlines()
        if "==" in line
    )
    for package, expected in profile["python_packages"].items():
        if requirements.get(package) != expected:
            raise ValueError(f"GPU {package} pin differs from ubuntu/python")
    framework_pins = dict(
        line.split("==", 1) for line in (gpu / "framework-constraints.txt").read_text().splitlines()
    )
    if framework_pins != profile["framework_packages"]:
        raise ValueError("GPU framework constraints differ from runtime.json")
    cuda_image = docker_arg(gpu / "base/Dockerfile", "cuda_image")
    expected_image = f'nvidia/cuda:{profile["cuda_version"]}-runtime-ubuntu{profile["ubuntu_version"]}@sha256:'
    if not cuda_image.startswith(expected_image) or not re.search(r"@sha256:[0-9a-f]{64}$", cuda_image):
        raise ValueError("GPU CUDA base must match runtime.json and have a pinned digest")
    if not profile["torch_version"].endswith("+" + profile["torch_cuda"]):
        raise ValueError("PyTorch wheel version must name the configured CUDA build")
    return profile, cuda_image


def build_commands(root, profile, cuda_image):
    repository = os.environ.get("DCS_IMAGE_REPOSITORY", "databricksruntime")
    cuda_series = ".".join(profile["cuda_version"].split(".")[:2])
    tag = os.environ.get("DCS_IMAGE_TAG", profile["runtime_tag"] + "-cuda" + cuda_series)
    package_index = os.environ.get("DCS_PACKAGE_INDEX_URL", "https://pypi.org/simple")
    torch_index = os.environ.get("DCS_TORCH_INDEX_URL", "https://download.pytorch.org/whl/" + profile["torch_cuda"])
    cuda_image = os.environ.get("DCS_CUDA_IMAGE", cuda_image)
    if not re.search(r"@sha256:[0-9a-f]{64}$", cuda_image):
        raise ValueError("DCS_CUDA_IMAGE must include a pinned digest")
    images = {name: f"{repository}/{name}:{tag}" for name in ("gpu-cuda", "gpu-base", "gpu-venv", "gpu-pytorch", "gpu-tensorflow")}
    steps = [
        ("gpu-cuda", "ubuntu/gpu", "base/Dockerfile", {"cuda_image": cuda_image, "cudnn_version": profile["cudnn_version"]}),
        ("gpu-base", "ubuntu/minimal", "Dockerfile", {"base_image": images["gpu-cuda"]}),
        ("gpu-venv", "ubuntu/python", "Dockerfile", {"base_image": images["gpu-base"], "package_index_url": package_index}),
        ("gpu-pytorch", "ubuntu/gpu/pytorch", "Dockerfile", {
            "base_image": images["gpu-venv"], "package_index_url": package_index,
            "torch_index_url": torch_index, "torch_version": profile["torch_version"],
            "torchvision_version": profile["torchvision_version"],
        }),
        ("gpu-tensorflow", "ubuntu/gpu/tensorflow", "Dockerfile", {
            "base_image": images["gpu-venv"], "package_index_url": package_index,
            "tensorflow_version": profile["tensorflow_version"],
        }),
    ]
    commands = []
    for name, directory, dockerfile, build_args in steps:
        command = ["docker", "build", "--platform", "linux/amd64", "-t", images[name], "-f", str(root / directory / dockerfile)]
        for key, value in build_args.items():
            command += ["--build-arg", key + "=" + value]
        commands.append(command + [str(root / directory)])
    system_checks = []
    for package, expected in {
        profile["cuda_runtime_package"]: profile["cuda_runtime_version"],
        "libcudnn9-cuda-12": profile["cudnn_version"],
    }.items():
        system_checks.append(
            f"test \"$(dpkg-query --show --showformat='${{Version}}' {package})\" = {shlex.quote(expected)}"
        )
    commands.append(["docker", "run", "--rm", "--entrypoint", "/bin/sh", images["gpu-base"], "-eu", "-c", "\n".join(system_checks)])
    version_check = (
        "import sys, pyarrow, numpy, pandas; "
        f"assert sys.version_info[:2] == {tuple(map(int, profile['python_version'].split('.')))!r}; "
        f"assert pyarrow.__version__ == {profile['python_packages']['pyarrow']!r}; "
        f"assert numpy.__version__ == {profile['python_packages']['numpy']!r}; "
        f"assert pandas.__version__ == {profile['python_packages']['pandas']!r}"
    )
    checks = {
        "gpu-venv": version_check,
        "gpu-pytorch": version_check + f"; import torch; assert torch.__version__ == {profile['torch_version']!r}",
        "gpu-tensorflow": version_check + f"; import tensorflow; assert tensorflow.__version__ == {profile['tensorflow_version']!r}",
    }
    for name, code in checks.items():
        commands.append(["docker", "run", "--rm", "--entrypoint", "/databricks/python3/bin/python", images[name], "-c", code])
    return commands


def main():
    parser = argparse.ArgumentParser(description="Build GPU examples from this branch's minimal and Python recipes.")
    parser.add_argument("--check-only", action="store_true", help="Check the GPU profile against the branch without Docker.")
    parser.add_argument("--dry-run", action="store_true", help="Print the checked build and smoke-test commands.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    try:
        profile, cuda_image = check_profile(root)
        print("GPU profile matches the branch's minimal and Python recipes.", flush=True)
        if args.check_only:
            return
        for command in build_commands(root, profile, cuda_image):
            print(shlex.join(command), flush=True)
            if not args.dry_run:
                subprocess.run(command, check=True)
    except (ValueError, subprocess.CalledProcessError) as error:
        sys.exit(str(error))


if __name__ == "__main__":
    main()
