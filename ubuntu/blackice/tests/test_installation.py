#!/usr/bin/env python3
import os
import subprocess
import pytest

PYTHON_TOOLS = [
    "pyrit",
    "fickling",
    "rigging",
    "judges",
    "garak",
    "giskard",
    "adversarial-robustness-toolbox",
    "cyberseceval",
    "lm-eval-harness",
    "promptmap",
    "fuzzyai",
    "easyedit",
    "cleverhans",
]
NODEJS_TOOLS = ["promptfoo"]
ALL_TOOLS = PYTHON_TOOLS + NODEJS_TOOLS
SYSTEM_TOOLS = ["pyrit", "fickling", "rigging", "judges"]
GIT_IMPORT_NAMES = {
    "cyberseceval": "CybersecurityBenchmarks",
    "promptmap": "promptmap2",
    "fuzzyai": "fuzzyai",
    "lm-eval-harness": "lm_eval",
    "easyedit": "steer",
    "cleverhans": "cleverhans",
    "adversarial-robustness-toolbox": "art",
}


class TestVirtualEnvironments:
    """Tests related to Python virtual environments."""

    @pytest.mark.parametrize("tool", PYTHON_TOOLS)
    def test_python_version(self, tool):
        if tool not in SYSTEM_TOOLS:
            python_executable = os.path.join(f"/venvs/{tool}", "bin/python")
            result = subprocess.run(
                [python_executable, "--version"], capture_output=True, text=True
            )
            assert result.returncode == 0, (
                f"Python executable failed to run in {python_executable}: {result.stderr}"
            )

    @pytest.mark.parametrize("tool", PYTHON_TOOLS)
    def test_uv_available(self, tool):
        if tool not in SYSTEM_TOOLS:
            cmd = f"source /venvs/{tool}/bin/activate && uv --help && deactivate"
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, executable="/bin/bash"
            )
            assert result.returncode == 0, (
                f"'uv' cannot be called from {tool} virtual environment: {result.stderr}"
            )


class TestImports:
    """Tests related to package imports."""

    @pytest.mark.parametrize("tool", PYTHON_TOOLS)
    def test_python_tool_importable(self, tool):
        import_name = GIT_IMPORT_NAMES[tool] if tool in GIT_IMPORT_NAMES else tool

        if tool in SYSTEM_TOOLS:
            # Test with system-level python3
            cmd = f'python3 -c "import {import_name}"'
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, executable="/bin/bash"
            )
            assert result.returncode == 0, (
                f"tool '{tool}' import as '{import_name}' failed (system python): {result.stderr}"
            )

            # Also test with /databricks/python3 venv
            cmd = (
                f"source /databricks/python3/bin/activate && "
                f'python3 -c "import {import_name}" && deactivate'
            )
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, executable="/bin/bash"
            )
            assert result.returncode == 0, (
                f"tool '{tool}' import as '{import_name}' failed (databricks venv): {result.stderr}"
            )
        else:
            cmd = (
                f"source /venvs/{tool}/bin/activate && "
                f'python3 -c "import {import_name}" && deactivate'
            )
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, executable="/bin/bash"
            )
            assert result.returncode == 0, (
                f"tool '{tool}' import as '{import_name}' failed: {result.stderr}"
            )

    @pytest.mark.parametrize("tool", NODEJS_TOOLS)
    def test_js_tool_importable(self, tool):
        result = subprocess.run(
            [
                "node",
                "-r",
                f"/venvs/{tool}/node_modules/{tool}",
                "-e",
                "process.exit(0)",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"JS tool '{tool}' import failed: {result.stderr}"
        )

    @pytest.mark.parametrize(
        "tool", ["pyrit", "garak", "lm-eval-harness", "fuzzyai", "easyedit"]
    )
    def test_torch_version_matches_constraint(self, tool):
        """Check that installed torch version matches the one pinned in the constraint file."""
        constraint_file = f"/opt/torch_constraints/{tool}.txt"
        with open(constraint_file) as f:
            for line in f:
                if line.strip().startswith("torch=="):
                    expected_version = line.strip().split("==")[1]
                    break
            else:
                pytest.skip(f"No torch== entry found in {constraint_file}")

        python_exec = "python3" if tool in SYSTEM_TOOLS else f"/venvs/{tool}/bin/python"

        result = subprocess.run(
            [
                python_exec,
                "-c",
                "import torch; print(torch.__version__)",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"{tool}: torch import failed: {result.stderr}"

        installed_version = result.stdout.strip()
        assert installed_version == expected_version, (
            f"{tool}: torch version mismatch (installed {installed_version}, expected {expected_version})"
        )


class TestGitToolDependencies:
    """Tests related to dependencies for Git-based tools."""

    @pytest.mark.parametrize("tool", ALL_TOOLS)
    def test_git_venv_tool_dependencies_installed(self, tool):
        if tool in GIT_IMPORT_NAMES:
            cmd = f"source /venvs/{tool}/bin/activate && pip freeze"
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, executable="/bin/bash"
            )
            assert result.returncode == 0 and result.stdout.strip(), (
                f"Dependencies check failed for {tool}: {result.stderr}"
            )
