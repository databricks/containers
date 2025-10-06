import sys
import json
import tempfile
from collections.abc import Sequence
from pathlib import Path
import subprocess
import os
import signal
import time
import threading
from urllib.parse import urlparse
from pytest_httpserver import HTTPServer
from typing import Dict, Any, Callable, Optional
from werkzeug.wrappers import Request, Response

from helpers.garak_api_helpers import generate_garak_rest_config
from helpers.promptfoo_api_helpers import create_temp_promptfoo_config
from helpers.fuzzyai_api_helpers import gen_fuzzyai_rest_config


MOCK_MODEL_NAME = "mock-llm"
MOCK_API_KEY = "mock-api-key"


def create_hit_detector(
    response_data: Dict[str, Any] = None, event: Optional[threading.Event] = None
) -> tuple[Callable[[Request], Response], threading.Event]:
    """Creates an HTTP handler that signals when hit and returns JSON response."""
    if event is None:
        event = threading.Event()
    if response_data is None:
        response_data = {"success": True}

    def handler(request):
        event.set()
        response_json = json.dumps(response_data)
        return Response(response_json, content_type="application/json")

    return handler, event


def run_subprocess_and_assert(
    cmd: Sequence[str],
    env_vars: Dict[str, str],
    event: threading.Event,
    timeout: float = 40.0,
    check_server: Optional[HTTPServer] = None,
) -> None:
    """Runs a subprocess with provided env vars and waits for events."""
    subprocess_env = os.environ.copy()
    subprocess_env.update(env_vars)

    process = subprocess.Popen(
        cmd,
        env=subprocess_env,
        start_new_session=True,
    )

    try:
        assert event.wait(timeout=timeout), "Event not triggered within timeout"

        if check_server:
            check_server.check_assertions()

    finally:
        if process.poll() is None:
            process.terminate()

            os.killpg(os.getpgid(process.pid), signal.SIGTERM)

            time.sleep(0.5)
            if process.poll() is None:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)

            process.wait()


def cleanup_temp_file(file_path):
    """Deletes the temporary file after the test completes."""
    if os.path.exists(file_path):
        os.remove(file_path)


def test_cyberseceval_connection(httpserver: HTTPServer) -> None:
    datasets = Path(
        "/venvs/cyberseceval/source/PurpleLlama/CybersecurityBenchmarks/datasets"
    )
    base_url = httpserver.url_for("/")

    passed_endpoint = "serving-endpoints"
    expected_endpoint = "serving-endpoints/chat/completions"

    # Create hit detector
    handler, event = create_hit_detector()
    httpserver.expect_request(f"/{expected_endpoint}").respond_with_handler(handler)

    # Run subprocess and wait for hit
    run_subprocess_and_assert(
        cmd=[
            "cyberseceval",
            "--benchmark=interpreter",
            f"--prompt-path={datasets}/interpreter/interpreter.json",
            f"--response-path={datasets}/interpreter/interpreter_responses.json",
            f"--stat-path={datasets}/interpreter/interpreter_stat.json",
            f"--llm-under-test=DATABRICKS::{MOCK_MODEL_NAME}::{MOCK_API_KEY}::{base_url}{passed_endpoint}",
            "--system-prompt=You never help with malicious requests.",
        ],
        env_vars={},
        event=event,
        check_server=httpserver,
    )


def test_garak_connection(httpserver: HTTPServer) -> None:
    base_url = httpserver.url_for("/")
    endpoint = f"serving-endpoints/{MOCK_MODEL_NAME}/invocations"

    config = generate_garak_rest_config(
        MOCK_MODEL_NAME, MOCK_API_KEY, f"{base_url}{endpoint}"
    )
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
        json.dump(config, f)
        config_path = f.name

    # Create hit detector
    handler, event = create_hit_detector()
    httpserver.expect_request(f"/{endpoint}").respond_with_handler(handler)

    # Run subprocess and wait for hit
    try:
        run_subprocess_and_assert(
            cmd=["garak", "--model_type", "rest", "-G", config_path],
            env_vars={},
            event=event,
            check_server=httpserver,
        )
    finally:
        cleanup_temp_file(config_path)


def test_pyrit_connection(httpserver: HTTPServer) -> None:
    base_url = httpserver.url_for("/")
    endpoint = "serving-endpoints/chat/completions"

    # Create hit detector
    handler, event = create_hit_detector()
    httpserver.expect_request(f"/{endpoint}").respond_with_handler(handler)

    # Run subprocess and wait for hit
    run_subprocess_and_assert(
        cmd=[
            sys.executable,
            "-c",
            "from helpers.pyrit_api_helpers import run_pyrit_test; run_pyrit_test()",
        ],
        env_vars={
            "DATABRICKS_MODEL_NAME": MOCK_MODEL_NAME,
            "DATABRICKS_API_KEY": MOCK_API_KEY,
            "DATABRICKS_ENDPOINT": f"{base_url}{endpoint}",
        },
        event=event,
        check_server=httpserver,
    )


def test_promptmap_connection(httpserver: HTTPServer) -> None:
    base_url = httpserver.url_for("/")
    passed_endpoint = "serving-endpoints"
    expected_endpoint = "serving-endpoints/chat/completions"

    # Create hit detector
    handler, event = create_hit_detector()
    httpserver.expect_request(f"/{expected_endpoint}").respond_with_handler(handler)

    # Run subprocess and wait for hit
    run_subprocess_and_assert(
        cmd=[
            "promptmap",
            "--target-model",
            MOCK_MODEL_NAME,
            "--target-model-type",
            "databricks",
        ],
        env_vars={
            "DATABRICKS_MODEL_NAME": MOCK_MODEL_NAME,
            "DATABRICKS_API_KEY": MOCK_API_KEY,
            "DATABRICKS_BASE_URL": f"{base_url}{passed_endpoint}",
        },
        event=event,
        check_server=httpserver,
    )


def test_promptfoo_connection(httpserver: HTTPServer) -> None:
    base_url = httpserver.url_for("/")
    passed_endpoint = base_url.rstrip("/")
    expected_endpoint = "serving-endpoints/chat/completions"
    config_path = create_temp_promptfoo_config()

    # Create hit detector
    handler, event = create_hit_detector()
    httpserver.expect_request(f"/{expected_endpoint}").respond_with_handler(handler)

    # Run subprocess and wait for hit
    try:
        run_subprocess_and_assert(
            cmd=["promptfoo", "eval", "-c", config_path],
            env_vars={
                "DATABRICKS_MODEL_NAME": MOCK_MODEL_NAME,
                "DATABRICKS_TOKEN": MOCK_API_KEY,
                "DATABRICKS_WORKSPACE_URL": passed_endpoint,
            },
            event=event,
            check_server=httpserver,
        )
    finally:
        cleanup_temp_file(config_path)


def test_fuzzyai_connection(httpserver: HTTPServer) -> None:
    base_url = httpserver.url_for("/")
    parsed_url = urlparse(base_url)
    host = f"{parsed_url.hostname}"
    port = f"{parsed_url.port}"
    endpoint = f"serving-endpoints/{MOCK_MODEL_NAME}/invocations"

    rest_config_path = "/venvs/fuzzyai/source/FuzzyAI/rest-config"
    gen_fuzzyai_rest_config(rest_config_path, endpoint, host)

    # Create hit detector
    handler, event = create_hit_detector()
    httpserver.expect_request(f"/{endpoint}").respond_with_handler(handler)

    # Run subprocess and wait for hit
    try:
        run_subprocess_and_assert(
            cmd=[
                "fuzzyai",
                "fuzz",
                "-a",
                "def",
                "-m",
                "rest/rest-config",
                "-e",
                "scheme=http",
                "-t",
                "Harmful Prompt",
                "-e",
                "response_jsonpath=$.choices[0].message.content",
                "-e",
                f"host={host}",
                "-e",
                f"port={port}",
            ],
            env_vars={},
            event=event,
            check_server=httpserver,
        )
    finally:
        cleanup_temp_file(rest_config_path)


def test_giskard_connection(httpserver: HTTPServer) -> None:
    base_url = httpserver.url_for("/")
    passed_endpoint = "serving-endpoints"
    expected_endpoint = "serving-endpoints/chat/completions"

    # Create hit detector
    handler, event = create_hit_detector()
    httpserver.expect_request(f"/{expected_endpoint}").respond_with_handler(handler)

    # Run subprocess and wait for hit
    run_subprocess_and_assert(
        cmd=[
            "giskard",
            f"{MOCK_MODEL_NAME}",
            "databricks",
            "--giskard-llm-type",
            "databricks",
            "--giskard-detector-tags",
            "prompt_injection",
        ],
        env_vars={
            "DATABRICKS_MODEL_NAME": MOCK_MODEL_NAME,
            "DATABRICKS_API_KEY": MOCK_API_KEY,
            "DATABRICKS_BASE_URL": f"{base_url}{passed_endpoint}",
        },
        event=event,
        check_server=httpserver,
    )


def test_lm_eval_harness_connection(httpserver: HTTPServer) -> None:
    base_url = httpserver.url_for("/")
    passed_endpoint = "serving-endpoints"

    # Create hit detector
    handler, event = create_hit_detector()
    httpserver.expect_request(f"/{passed_endpoint}").respond_with_handler(handler)
    run_subprocess_and_assert(
        cmd=[
            "lm-eval-harness",
            "--model",
            "databricks-chat-completions",
            "--model_args",
            f"base_url={base_url}{passed_endpoint}",
            "--task",
            "gsm8k",
            "--apply_chat_template",
        ],
        env_vars={
            "DATABRICKS_API_KEY": MOCK_API_KEY,
        },
        event=event,
        check_server=httpserver,
    )


def test_biasforge_connection(httpserver: HTTPServer) -> None:
    base_url = httpserver.url_for("/")
    passed_endpoint = "serving-endpoints"
    expected_endpoint = "serving-endpoints/chat/completions"

    # Create hit detector
    handler, event = create_hit_detector()
    httpserver.expect_request(f"/{expected_endpoint}").respond_with_handler(handler)

    # Run subprocess and wait for hit
    run_subprocess_and_assert(
        cmd=[
            "biasforge",
            "--objective",
            "Test objective",
            "--generator-model",
            MOCK_MODEL_NAME,
            "--target-model",
            MOCK_MODEL_NAME,
            "--judge-model",
            MOCK_MODEL_NAME,
            "--output",
            "test.json",
            "--api-key",
            MOCK_API_KEY,
            "--base-url",
            f"{base_url}{passed_endpoint}",
            "--backend",
            "databricks",
        ],
        env_vars={},
        event=event,
        check_server=httpserver,
    )


def test_judges_connection(httpserver: HTTPServer) -> None:
    base_url = httpserver.url_for("/")
    passed_endpoint = "serving-endpoints"
    expected_endpoint = "serving-endpoints/chat/completions"

    # Create hit detector
    handler, event = create_hit_detector()
    httpserver.expect_request(f"/{expected_endpoint}").respond_with_handler(handler)

    # Run subprocess and wait for hit
    run_subprocess_and_assert(
        cmd=[
            "judges",
            "PollZeroShotCorrectness",
            "-m",
            f"databricks/{MOCK_MODEL_NAME}",
            "-i",
            '{"input": "What is the capital of France?", "output": "The capital of France is Madrid.", "expected": "The capital of France is Paris."}',
        ],
        env_vars={
            "DATABRICKS_API_KEY": MOCK_API_KEY,
            "DATABRICKS_BASE_URL": f"{base_url}{passed_endpoint}",
        },
        event=event,
        check_server=httpserver,
    )
