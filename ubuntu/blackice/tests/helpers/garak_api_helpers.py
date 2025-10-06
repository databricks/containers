def generate_garak_rest_config(model_name, api_key, endpoint):
    req_template = {
        "messages": [
            {"role": "system", "content": "You are an AI assistant"},
            {"role": "user", "content": "$INPUT"},
        ],
        "model": model_name,
        "max_tokens": 256,
    }

    rest_json = {
        "rest": {
            "RestGenerator": {
                "name": model_name,
                "uri": endpoint,
                "method": "post",
                "headers": {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                "req_template_json_object": req_template,
                "response_json": True,
                "response_json_field": "$.choices[0].message.content",
            }
        }
    }

    return rest_json
