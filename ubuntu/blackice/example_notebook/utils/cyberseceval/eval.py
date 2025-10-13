def stat_json_to_success_rate(eval_dict: dict, model_name: str, json_path: str) -> str:
    """
    The cyberseceval tools save the results in a JSON file that is not standardized.
    Each benchmark has its own key in the JSON file that we need to extract the success rate from.
    This function returns the key for the given model and benchmark.
    """
    if json_path == "prompt_injection/prompt_injection.json":
        return eval_dict[model_name]["stat_per_model"][
            "injection_successful_percentage"
        ]
    elif json_path == "frr/frr.json":
        return eval_dict[model_name]["refusal_rate"]
    elif json_path == "instruct/instruct.json":
        total_vulnerable, total_snippets = 0, 0
        for language in eval_dict[model_name]:
            total_vulnerable += eval_dict[model_name][language][
                "vulnerable_suggestion_count"
            ]
            total_snippets += eval_dict[model_name][language]["total_count"]
        return total_vulnerable / total_snippets
    elif json_path == "mitre/mitre_benchmark_100_per_category_with_augmentation.json":
        total_malicious, total_snippets = 0, 0
        for category in eval_dict[model_name]:
            total_snippets += eval_dict[model_name][category]["total_count"]
            total_malicious += eval_dict[model_name][category]["malicious_count"]
        return total_malicious / total_snippets
    else:
        raise ValueError(f"Unknown json path: {json_path}")
