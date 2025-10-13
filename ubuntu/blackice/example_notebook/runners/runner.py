import os
import json
import subprocess
from abc import ABC, abstractmethod

from utils.garak.scan import gen_json, get_sanity_check_dir_log_file, evaluate_jsonl
from utils.cyberseceval.eval import stat_json_to_success_rate


# Abstract base class approach
class ToolRunner(ABC):
    @abstractmethod
    def run(
        self, url: str, api_key: str, base_dir: str, model_name: str, **kwargs
    ) -> float:
        """Run the tool and return success rate. Returns -1 on failure."""
        pass


def check_or_set_env_var(var_name: str, var_value: str):
    """
    Checks if the environment variable `var_name` is set to `var_value`.
    If it is not, it sets it to `var_value`.
    """
    if var_name in os.environ:
        if os.environ[var_name] != var_value:
            os.environ[var_name] = var_value
    else:
        os.environ[var_name] = var_value


class GarakRunner(ToolRunner):
    def __init__(self, probe_name: str):
        self.probe_name = probe_name

    def run(
        self, base_url: str, api_key: str, save_dir: str, model_name: str, **kwargs
    ) -> float:
        endpoint_url = f"{os.path.join(base_url, model_name)}/invocations"
        check_or_set_env_var("XDG_DATA_HOME", save_dir)
        env = os.environ.copy()
        rest_json = gen_json(model_name, endpoint_url, api_key)
        rest_filename = os.path.join(save_dir, f"garak-rest-{model_name}.json")
        json.dump(rest_json, open(rest_filename, "w"))
        #
        cmd = f"garak --model_name {model_name} --model_type rest -G {rest_filename} \
            --probes {self.probe_name} --report_prefix {self.probe_name}"
        if "parallel_attempts" in kwargs:
            cmd += f" --parallel_attempts {kwargs['parallel_attempts']}"
        if "generations" in kwargs:
            cmd += f" --generations {kwargs['generations']}"
        try:
            subprocess.run(cmd, shell=True, check=True, env=env)
        except Exception as e:
            print(f"Run failed with error {e}.")
            return -1
        report_filepath = os.path.join(
            save_dir, "garak/garak_runs/", f"{self.probe_name}.report.jsonl"
        )
        result_dict = get_sanity_check_dir_log_file(report_filepath)
        if not result_dict["completion"]:
            print(f"{self.probe_name} did not exit normally.")
            return -1
        else:
            results_pd = evaluate_jsonl(report_filepath)
            average_success_rate = (
                results_pd["successful_attacks"].sum()
                / results_pd["total_attacks"].sum()
            )
            return average_success_rate


class PromptmapRunner(ToolRunner):
    def __init__(self, probe_name: str):
        self.probe_name = probe_name

    def run(
        self, base_url: str, api_key: str, save_dir: str, model_name: str, **kwargs
    ) -> float:
        check_or_set_env_var("DATABRICKS_BASE_URL", base_url)
        check_or_set_env_var("DATABRICKS_API_KEY", api_key)
        output_file = os.path.join(
            save_dir, f"promptmap/promptmap_output_{model_name}.json"
        )
        if not os.path.isdir(os.path.join(save_dir, "promptmap")):
            os.makedirs(os.path.join(save_dir, "promptmap"))
        if self.probe_name == "promptmap":
            cmd = f"promptmap --target-model {model_name} --target-model-type databricks --output {output_file}"
        else:
            cmd = f"promptmap --target-model {model_name} --target-model-type databricks --output {output_file} --rules {self.probe_name}"
        if "iterations" in kwargs:
            cmd += f" --iterations {kwargs['iterations']}"
        try:
            print(f"Running command: {cmd}")
            subprocess.run(cmd, shell=True, check=True)
        except Exception as e:
            print(f"Run failed with error {e}.")
            return -1
        result_dict = json.load(open(output_file))
        passes = [v["passed"] for v in result_dict.values()]
        success_rate = (len(result_dict) - sum(passes)) / len(passes)
        return success_rate


class CybersecevalRunner(ToolRunner):
    def __init__(self, probe_name: str):
        self.probe_name = probe_name
        self.dataset_dir = (
            "/venvs/cyberseceval/source/PurpleLlama/CybersecurityBenchmarks/datasets/"
        )

    def run(
        self, base_url: str, api_key: str, base_dir: str, model_name: str, **kwargs
    ) -> float:
        judge_model_name = kwargs.get("judge_model_name")
        json_path = kwargs.get("json_path")
        dataset_dir = self.dataset_dir
        json_path_full = os.path.join(dataset_dir, json_path)
        assert os.path.exists(json_path_full), f"Dataset {json_path_full} not found."
        json_path_wo_ext = json_path.split(".")[0]
        savedir = os.path.join(base_dir, "cyberseceval", json_path_wo_ext)
        if not os.path.isdir(savedir):
            os.makedirs(savedir)
        command = f'''
                cyberseceval \
                --benchmark="{self.probe_name}" \
                --prompt-path="{json_path_full}" \
                --response-path="{savedir}/responses.json" \
                --stat-path="{savedir}/stats.json" \
                --judge-response-path="{savedir}/judge_responses.json" \
                --judge-llm="DATABRICKS::{judge_model_name}::{api_key}::{base_url}" \
                --expansion-llm="DATABRICKS::{judge_model_name}::{api_key}::{base_url}" \
                --llm-under-test="DATABRICKS::{model_name}::{api_key}::{base_url}" \
                '''
        if "run_llm_in_parallel" in kwargs:
            command += f"--run-llm-in-parallel {kwargs['run_llm_in_parallel']}"
        try:
            print(f"Running command: {command}")
            subprocess.run(command, shell=True, check=True)
            json_stat = json.load(open(os.path.join(savedir, "stats.json")))
            success_rate = stat_json_to_success_rate(json_stat, model_name, json_path)
            if success_rate is None:
                print(f"Could not find success rate for {model_name} in {json_path}.")
                return -1
            return success_rate
        except Exception as e:
            print(f"Run failed with error {e}.")
            return -1


class fuzzyaiRunner(ToolRunner):
    def __init__(self, probe_name: str):
        self.probe_name = probe_name
        self.root_dir = "/venvs/fuzzyai/source/FuzzyAI"

    def save_configfile_template(
        self, base_url: str, model_name: str, api_key: str, save_path: str
    ) -> str:
        config_str = f"""POST serving-endpoints/{model_name}/invocations HTTP/1.1
Content-Type: application/json
Authorization: Bearer {api_key}

{{
"messages": [
    {{
    "role": "user",
    "content": "<PROMPT>"
    }}
]
}}"""
        with open(save_path, "w") as f:
            f.write(config_str)

    def run(
        self, base_url: str, api_key: str, save_dir: str, model_name: str, **kwargs
    ) -> float:
        check_or_set_env_var("DATABRICKS_API_KEY", api_key)
        # As describes in the readme, fuzzyai build the url as {protocol}://{base_url}:{port}/{path_from_config}
        # so we need to make sure that base_url ends with .com and has no http or https prefix
        # Normalize base_url to remove protocol and keep only the netloc (host[:port])
        from urllib.parse import urlparse

        parsed = urlparse(
            base_url if base_url.startswith("http") else "https://" + base_url
        )
        netloc = (
            parsed.netloc or parsed.path
        )  # netloc if URL has protocol, else take path (host)
        base_url = netloc.split("/")[0]  # remove anything after first '/'
        if not base_url:
            raise ValueError(f"Could not determine host from base_url: {base_url}")
        config_file_path = os.path.join(self.root_dir, "rest-config")
        self.save_configfile_template(base_url, model_name, api_key, config_file_path)
        command = (
            f"fuzzyai fuzz "
            f"-a {self.probe_name} "
            f"-m rest/rest-config "
            f"-e scheme=https "
            f"-e host={base_url}"
        )
        if "params" in kwargs:
            for key, value in kwargs["params"].items():
                command += f" {key} {value}"
        if "extra_args" in kwargs:
            for key, value in kwargs["extra_args"].items():
                command += f" -e {key}={value}"
        try:
            print(f"Running command: {command}")
            subprocess.run(command, shell=True, check=True)
        except Exception as e:
            print(f"Run failed with error {e}.")
            return -1

        # Find the newest folder in the results directory
        results_dir = os.path.join(self.root_dir, "results")
        if not os.path.exists(results_dir):
            print(f"Results directory {results_dir} does not exist.")
            return -1

        # List all subdirectories in results_dir and get the newest one. That's the folder where the results are saved.
        subdirs = [
            d
            for d in os.listdir(results_dir)
            if os.path.isdir(os.path.join(results_dir, d))
        ]
        if not subdirs:
            print(f"No subdirectories found in {results_dir}.")
            return -1
        newest_folder = max(
            subdirs, key=lambda d: os.path.getmtime(os.path.join(results_dir, d))
        )
        report_path = os.path.join(results_dir, newest_folder, "report.json")
        if not os.path.exists(report_path):
            print(
                f"report.json not found in {os.path.join(results_dir, newest_folder)}."
            )
            return -1

        try:
            with open(report_path, "r") as f:
                report = json.load(f)
            # Assume the report contains a "success_rate" field at the top level
            for technique in report["attacking_techniques"]:
                attack_mode = technique["attack_mode"]
                success_rate = technique["success_rate"]
                if attack_mode == self.probe_name:
                    return success_rate
        except Exception as e:
            print(f"Failed to read or parse report.json: {e}")
            return -1
