# NEW_FILE_PATH: PyRIT/pyrit/prompt_target/databricks_chat_target.py

import logging
from typing import MutableSequence

from pyrit.prompt_target import OpenAIChatTarget
from pyrit.models import (
    PromptRequestResponse,
)

logger = logging.getLogger(__name__)


class DatabricksChatTarget(OpenAIChatTarget):
    """
    A chat target for interacting with Databricks' OpenAI-compatible API.

    This class extends `OpenAIChatTarget` and ensures compatibility with Databricks' API.
    """

    def __init__(
        self,
        *,
        model_name: str = None,
        endpoint: str = None,
        api_key: str = None,
        api_version: str = None,
        **kwargs,
    ):
        """
        Initializes DatabricksChatTarget with the correct API settings.

        Args:
            model_name (str, optional): The model to use. Defaults to `DATABRICKS_MODEL_NAME` env variable.
            endpoint (str, optional): The API base URL. Defaults to `DATABRICKS_ENDPOINT` env variable.
            api_key (str, optional): The API key for authentication. Defaults to `DATABRICKS_API_KEY` env variable.
            max_requests_per_minute (int, optional): Rate limit for requests.
        """
        super().__init__(
            model_name=model_name,
            endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
            **kwargs,
        )

    def _set_openai_env_configuration_vars(self) -> None:
        self.model_name_environment_variable = "DATABRICKS_MODEL_NAME"
        self.endpoint_environment_variable = "DATABRICKS_ENDPOINT"
        self.api_key_environment_variable = "DATABRICKS_API_KEY"

    async def _construct_request_body(
        self,
        conversation: MutableSequence[PromptRequestResponse],
        is_json_response: bool,
    ) -> dict:
        messages = await self._build_chat_messages_async(conversation)

        # If requesting a JSON response, ensure the last message mentions "json" as required by Databricks
        if is_json_response:
            messages[-1]["content"] += (
                "\n\nEnsure your response is structured as valid JSON."
            )

        body_parameters = {
            "model": self._model_name,
            "max_completion_tokens": self._max_completion_tokens,
            "max_tokens": self._max_tokens,
            "temperature": self._temperature,
            "top_p": self._top_p,
            "frequency_penalty": self._frequency_penalty,
            "presence_penalty": self._presence_penalty,
            "stream": False,
            "seed": self._seed,
            "n": self._n,
            "messages": messages,
            "response_format": {"type": "json_object"} if is_json_response else None,
        }

        if self._extra_body_parameters:
            for key, value in self._extra_body_parameters.items():
                body_parameters[key] = value

        # Filter out None values
        return {k: v for k, v in body_parameters.items() if v is not None}
