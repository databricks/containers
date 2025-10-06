import json


def gen_fuzzyai_rest_config(save_path, endpoint, base_url):
    rest_config = "\n".join(
        [
            f"POST {endpoint} HTTP/1.1",
            f"Host: {base_url}",
            "Content-Type: application/json",
            "\n",
        ]
    )
    data = {"messages": [{"role": "user", "content": "<PROMPT>"}]}
    with open(save_path, "w") as f:
        f.write(rest_config + "\n" + json.dumps(data, indent=2))
