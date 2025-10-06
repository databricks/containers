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
SYSTEM_TOOLS = ["pyrit", "fickling", "rigging", "judges"]
NODEJS_TOOLS = ["promptfoo"]
STUB_TOOLS = ["llm-security-scripts", "gpt-fuzzer"]
CUSTOM_TOOLS = ["biasforge"]
ALL_TOOLS = PYTHON_TOOLS + NODEJS_TOOLS + CUSTOM_TOOLS + STUB_TOOLS


class TestCLIScripts:
    """Tests related to CLI script availability and permissions."""

    @pytest.mark.parametrize("tool", ALL_TOOLS)
    def test_cli_exists_and_executable(self, tool):
        cli_path = os.path.join("/usr/local/bin", tool)
        assert os.path.exists(cli_path), f"CLI script {cli_path} does not exist."
        assert os.access(cli_path, os.X_OK), f"CLI script {cli_path} is not executable."


class TestCLIExecution:
    """Tests related to CLI command execution."""

    @pytest.mark.parametrize("tool", ALL_TOOLS)
    def test_global_cli_alias_execution(self, tool):
        cmd = f"bash -l -c 'set -e; set -o pipefail; {tool} --help'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        assert result.returncode == 0, (
            f"Global alias execution failed for {tool}: {result.stderr}"
        )

    @pytest.mark.parametrize("tool", PYTHON_TOOLS)
    def test_cli_execution_in_venv(self, tool):
        if tool not in SYSTEM_TOOLS:
            venv_path = f"/venvs/{tool}/bin"
            cmd = f"bash -l -c 'set -e; set -o pipefail; source {venv_path}/activate && {tool} --help && deactivate'"
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, executable="/bin/bash"
            )
            assert result.returncode == 0, (
                f"CLI command '{tool} --help' failed within venv: {result.stderr}"
            )
