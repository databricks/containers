import os
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
GIT_TOOLS = {
    "cyberseceval": "/venvs/cyberseceval/source/PurpleLlama",
    "lm-eval-harness": "/venvs/lm-eval-harness/source/lm-evaluation-harness",
    "promptmap": "/venvs/promptmap/source/promptmap",
    "fuzzyai": "/venvs/fuzzyai/source/FuzzyAI",
    "easyedit": "/venvs/easyedit/source/EasyEdit",
    "cleverhans": "/venvs/cleverhans/source/cleverhans",
}


@pytest.mark.parametrize("tool", ALL_TOOLS)
def test_tool_setup(tool):
    if tool not in SYSTEM_TOOLS and tool not in NODEJS_TOOLS:
        assert os.path.isdir(f"/venvs/{tool}"), (
            f"Virtual environment for '{tool}' missing at '/venvs/{tool}'"
        )
    if tool in GIT_TOOLS:
        repo_path = GIT_TOOLS[tool]
        assert os.path.isdir(repo_path), (
            f"Git repository '{tool}' not cloned at '{repo_path}'"
        )
    if tool in NODEJS_TOOLS:
        assert os.path.isdir(f"/venvs/{tool}"), (
            f"node_modules directory for '{tool}' missing at '/venvs/{tool}'"
        )
