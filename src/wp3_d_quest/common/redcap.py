import os
from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal

import requests


@dataclass
class APIConfig:
    """Configuration for the REDCap API."""

    env_key: str
    url: str


class Center(Enum):
    """The centers in the study."""

    Open = APIConfig(
        env_key="REDCAP_OPEN_API_KEY", url="https://open.rsyd.dk/redcap/api/"
    )


def get(
    request_data: dict[str, str],
    center: Center = Center.Open,
) -> requests.Response:
    """Send a request to the REDCap API."""
    token = os.environ.get(center.value.env_key)
    if not token:
        raise RuntimeError(f"{center.value.env_key} environment variable is not set.")

    request_data["token"] = token

    response = requests.post(center.value.url, data=request_data, timeout=60)
    response.raise_for_status()

    return response


def get_json(
    content: Literal["metadata", "repeatingFormsEvents", "formEventMapping"],
    center: Center = Center.Open,
) -> Any:
    """Send a request to the REDCap API and return the JSON response."""
    request_data = {
        "content": content,
        "format": "json",
        "returnFormat": "json",
    }
    response = get(request_data, center)
    return response.json()
