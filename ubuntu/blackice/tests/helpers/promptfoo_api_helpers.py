import tempfile

PROMPTFOO_CONFIG = """\
# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: 'Getting started'
prompts:
  - 'Convert this English to {{language}}: {{input}}'
  - 'Translate to {{language}}: {{input}}'

providers:
  - id: databricks:databricks-meta-llama-3-3-70b-instruct
    config:
      temperature: 0.7
      max_tokens: 256

tests:
  - vars:
      language: French
      input: Hello world
    assert:
      - type: contains
        value: 'Bonjour le monde'
"""


def create_temp_promptfoo_config():
    """Creates a temporary YAML config file for promptfoo, returns its path, and ensures cleanup."""
    temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
    temp_file.write(PROMPTFOO_CONFIG)
    temp_file.close()
    return temp_file.name
