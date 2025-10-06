#!/usr/bin/env python3
import os
import subprocess


class TestCyberseceval:
    """Tests related to Cyberseceval/PurpleLlama modifications."""

    def test_databricks_file_exists(self):
        TARGET_FILE = "/venvs/cyberseceval/source/PurpleLlama/CybersecurityBenchmarks/benchmark/llms/databricks.py"
        assert os.path.exists(TARGET_FILE), f"{TARGET_FILE} not found."

    def test_base_llm_file_is_patched(self):
        TARGET_FILE = "/venvs/cyberseceval/source/PurpleLlama/CybersecurityBenchmarks/benchmark/llms/llm_base.py"
        with open(TARGET_FILE, encoding="utf-8") as f:
            content = f.read()
        assert "self.base_url: str | None = config.base_url" in content, (
            f"Incomplete patching in {TARGET_FILE}."
        )

    def test_llm_file_is_patched(self):
        TARGET_FILE = "/venvs/cyberseceval/source/PurpleLlama/CybersecurityBenchmarks/benchmark/llm.py"
        with open(TARGET_FILE, encoding="utf-8") as f:
            content = f.read()
        assert "provider, name, api_key, base_url = split" in content, (
            f"Incomplete patching in {TARGET_FILE}."
        )

    def test_run_file_is_patched(self):
        TARGET_FILE = "/venvs/cyberseceval/source/PurpleLlama/CybersecurityBenchmarks/benchmark/run.py"
        with open(TARGET_FILE, encoding="utf-8") as f:
            content = f.read()
        assert "--system-prompt" in content, f"Incomplete patching in {TARGET_FILE}"

    def test_benchmark_files_are_patched(self):
        TARGET_FILES = [
            os.path.join(
                "/venvs/cyberseceval/source/PurpleLlama/CybersecurityBenchmarks/benchmark",
                file,
            )
            for file in [
                "autonomous_uplift_benchmark.py",
                "autopatching_benchmark.py",
                "benchmark.py",
                "canary_exploit_benchmark.py",
                "mitre_frr_benchmark.py",
                "instruct_or_autocomplete_benchmark.py",
                "interpreter_benchmark.py",
                "mitre_benchmark.py",
                "multiturn_phishing_benchmark.py",
                "prompt_injection_benchmark.py",
                "query_llm.py",
                "visual_prompt_injection_benchmark.py",
            ]
        ]
        for file in TARGET_FILES:
            with open(file, encoding="utf-8") as f:
                content = f.read()
            assert "system_prompt: Optional[str] = None" in content, (
                f"Incomplete patching in {file}"
            )


class TestPyRIT:
    """Tests related to PyRIT integration."""

    def test_databricks_chat_target_importable(self):
        """Ensure DatabricksChatTarget is included in the installed pyrit package."""
        from pyrit.prompt_target import DatabricksChatTarget

        assert DatabricksChatTarget is not None, (
            "DatabricksChatTarget is not importable"
        )


class TestPromptmap:
    """Tests related to Promptmap integration."""

    def test_promptmap_has_databricks_option(self):
        """Checks if databricks is an option for model_type."""
        command = "source ~/.bashrc && promptmap --help"
        result = subprocess.run(["bash", "-c", command], capture_output=True, text=True)
        output = result.stdout

        assert "databricks" in output, "'databricks' is not an option for model_type."


class TestLMEvalHarness:
    """Tests related to lm-eval-harness integration."""

    TARGET_FILE = "/venvs/lm-eval-harness/source/lm-evaluation-harness/lm_eval/models/openai_completions.py"

    def test_lm_eval_harness_has_databricks_option(self):
        """Checks if databricks appears in file that has been modified."""
        with open(self.TARGET_FILE, encoding="utf-8") as f:
            content = f.read()
        assert "databricks" in content, "'databricks' is not in the modified file."
