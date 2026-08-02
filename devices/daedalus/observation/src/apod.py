import json
import os
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


APOD_ENDPOINT = "https://api.nasa.gov/planetary/apod"

ENV_PATH = (
    Path.home()
    / ".config"
    / "daedalus"
    / "observation.env"
)


def load_api_key() -> str:
    """Load the NASA API key from the environment or local config."""

    environment_key = os.environ.get("NASA_API_KEY")

    if environment_key:
        return environment_key.strip()

    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(
            encoding="utf-8"
        ).splitlines():
            key, separator, value = line.partition("=")

            if (
                separator
                and key.strip() == "NASA_API_KEY"
                and value.strip()
            ):
                return value.strip()

    return "DEMO_KEY"


def fetch_apod(
    api_key: str | None = None,
) -> dict[str, Any]:
    """Fetch today's Astronomy Picture of the Day metadata."""

    resolved_key = api_key or load_api_key()

    query = urlencode(
        {
            "api_key": resolved_key,
            "thumbs": "true",
        }
    )

    request_url = f"{APOD_ENDPOINT}?{query}"

    try:
        with urlopen(request_url, timeout=30) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"NASA returned HTTP status "
                    f"{response.status}"
                )

            return json.load(response)

    except HTTPError as error:
        if error.code == 429:
            raise RuntimeError(
                "NASA API rate limit reached. "
                "The existing cached NASA observation "
                "will remain available."
            ) from error

        raise RuntimeError(
            f"NASA request failed with HTTP status "
            f"{error.code}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"Could not connect to NASA: {error.reason}"
        ) from error

    except TimeoutError as error:
        raise RuntimeError(
            "NASA request timed out"
        ) from error

    except json.JSONDecodeError as error:
        raise RuntimeError(
            "NASA returned invalid JSON"
        ) from error
