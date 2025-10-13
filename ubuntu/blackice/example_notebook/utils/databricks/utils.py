import requests
from urllib.parse import urljoin
from pyspark.sql import SparkSession


def get_foundation_model_endpoints(token: str) -> list:
    """
    Returns a list of endpoint names that serve a FOUNDATION_MODEL.

    Args:
        token (str): A valid Databricks personal access token

    Returns:
        List[str]: List of matching endpoint names
    """
    spark = SparkSession.builder.getOrCreate()
    base_url = f"https://{spark.conf.get('spark.databricks.workspaceUrl')}"
    api_url = urljoin(base_url, "/api/2.0/serving-endpoints")

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    endpoints = response.json().get("endpoints", [])
    foundation_models = []

    for endpoint in endpoints:
        try:
            served_type = endpoint["config"]["served_entities"][0]["type"]
            if served_type == "FOUNDATION_MODEL":
                foundation_models.append(endpoint["name"])
        except (KeyError, IndexError):
            continue  # Skip endpoints with unexpected structure

    return foundation_models
