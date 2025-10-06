# NEW_FILE_PATH: PurpleLlama/CybersecurityBenchmarks/benchmark/llms/databricks.py

from __future__ import annotations

import logging
from typing import List, Optional

import openai

from typing_extensions import override

from .llm_base import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    LLM,
    LLMConfig,
)


class DATABRICKS(LLM):
    """Accessing DATABRICKS"""

    def __init__(self, config: LLMConfig) -> None:
        super().__init__(config)
        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    def model_accepts_response_format(self) -> bool:
        """Return True if the current model supports the response_format argument."""
        disallowed_models = {
            "databricks-claude-sonnet-4",
            "databricks-claude-opus-4databricks-claude-3-7-sonnet",
        }
        return self.model not in disallowed_models

    @override
    def chat(
        self,
        prompt_with_history: List[str],
        guided_decode_json_schema: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        top_p: float = DEFAULT_TOP_P,
    ) -> str:
        if (
            not self.model_accepts_response_format()
            and guided_decode_json_schema is not None
        ):
            raise ValueError(
                f"The model {self.model} does not support the response_format argument."
            )

        messages = []
        for i in range(len(prompt_with_history)):
            if i % 2 == 0:
                messages.append({"role": "user", "content": prompt_with_history[i]})
            else:
                messages.append(
                    {"role": "assistant", "content": prompt_with_history[i]}
                )

        level = logging.getLogger().level
        logging.getLogger().setLevel(logging.WARNING)
        params = {
            "model": self.model,
            "messages": messages,
            "max_tokens": DEFAULT_MAX_TOKENS,
            "temperature": temperature,
            "top_p": top_p,
        }
        if (
            self.model_accepts_response_format()
            and guided_decode_json_schema is not None
        ):
            params["response_format"] = guided_decode_json_schema
        response = self.client.chat.completions.create(**params)
        logging.getLogger().setLevel(level)
        return response.choices[0].message.content

    @override
    def chat_with_system_prompt(
        self,
        system_prompt: str,
        prompt_with_history: List[str],
        guided_decode_json_schema: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        top_p: float = DEFAULT_TOP_P,
    ) -> str:
        if (
            not self.model_accepts_response_format()
            and guided_decode_json_schema is not None
        ):
            raise ValueError(
                f"The model {self.model} does not support the response_format argument."
            )

        messages = [{"role": "system", "content": system_prompt}]
        for i in range(len(prompt_with_history)):
            if i % 2 == 0:
                messages.append({"role": "user", "content": prompt_with_history[i]})
            else:
                messages.append(
                    {"role": "assistant", "content": prompt_with_history[i]}
                )

        level = logging.getLogger().level
        logging.getLogger().setLevel(logging.WARNING)

        params = {
            "model": self.model,
            "messages": messages,
            "max_tokens": DEFAULT_MAX_TOKENS,
            "temperature": temperature,
            "top_p": top_p,
        }
        if (
            self.model_accepts_response_format()
            and guided_decode_json_schema is not None
        ):
            params["response_format"] = guided_decode_json_schema

        response = self.client.chat.completions.create(**params)
        logging.getLogger().setLevel(level)
        return response.choices[0].message.content

    @override
    def query(
        self,
        prompt: str,
        guided_decode_json_schema: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        top_p: float = DEFAULT_TOP_P,
    ) -> str:
        if (
            not self.model_accepts_response_format()
            and guided_decode_json_schema is not None
        ):
            raise ValueError(
                f"The model {self.model} does not support the response_format argument."
            )

        level = logging.getLogger().level
        logging.getLogger().setLevel(logging.WARNING)

        params = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": DEFAULT_MAX_TOKENS,
            "temperature": temperature,
            "top_p": top_p,
        }
        if (
            self.model_accepts_response_format()
            and guided_decode_json_schema is not None
        ):
            params["response_format"] = guided_decode_json_schema

        response = self.client.chat.completions.create(**params)
        logging.getLogger().setLevel(level)
        return response.choices[0].message.content

    @override
    def query_with_system_prompt(
        self,
        system_prompt: str,
        prompt: str,
        guided_decode_json_schema: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        top_p: float = DEFAULT_TOP_P,
    ) -> str:
        if (
            not self.model_accepts_response_format()
            and guided_decode_json_schema is not None
        ):
            raise ValueError(
                f"The model {self.model} does not support the response_format argument."
            )

        level = logging.getLogger().level
        logging.getLogger().setLevel(logging.WARNING)

        params = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": DEFAULT_MAX_TOKENS,
            "temperature": temperature,
            "top_p": top_p,
        }
        if (
            self.model_accepts_response_format()
            and guided_decode_json_schema is not None
        ):
            params["response_format"] = guided_decode_json_schema

        response = self.client.chat.completions.create(**params)
        logging.getLogger().setLevel(level)
        return response.choices[0].message.content

    @override
    def valid_models(self) -> list[str]:
        return [
            "databricks-claude-sonnet-4",
            "databricks-llama-4-maverick",
            "databricks-claude-opus-4",
            "databricks-claude-3-7-sonnet",
            "databricks-meta-llama-3-3-70b-instruct",
            "databricks-meta-llama-3-1-8b-instruct",
            "databricks-meta-llama-3-1-405b-instruct",
        ]
