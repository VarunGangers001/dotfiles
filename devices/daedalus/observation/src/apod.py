import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from cache import (
    FULL_IMAGE_PATH,
    PREVIEW_IMAGE_PATH,
    download_file,
    save_metadata,
)

APOD_ENDPOINT = "https://api.nasa.gov/planetary/apod"


def fetch_apod(api_key: str = "DEMO_KEY") -> dict[str, Any]:
    """Fetch today's Astronomy Picture of the Day metadata."""

    query = urlencode(
        {
            "api_key": api_key,
            "thumbs": "true",
        }
    )

    request_url = f"{APOD_ENDPOINT}?{query}"

    try:
        with urlopen(request_url, timeout=15) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"NASA returned HTTP status {response.status}"
                )

            data = json.load(response)

    except HTTPError as error:
        raise RuntimeError(
            f"NASA request failed with HTTP status {error.code}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"Could not connect to NASA: {error.reason}"
        ) from error

    except json.JSONDecodeError as error:
        raise RuntimeError(
            "NASA returned data that could not be read as JSON"
        ) from error

    return data


if __name__ == "__main__":
    try:
        apod = fetch_apod()

        if apod.get("media_type") != "image":
            raise RuntimeError(
                "Today's APOD is not an image"
            )

        preview_url = apod.get("url")
        full_url = apod.get("hdurl") or preview_url

        if not preview_url:
            raise RuntimeError(
                "NASA did not provide an image URL"
            )

        save_metadata(apod)
        download_file(preview_url, PREVIEW_IMAGE_PATH)
        download_file(full_url, FULL_IMAGE_PATH)

        print(f"Saved metadata to: {PREVIEW_IMAGE_PATH.parent}")
        print(f"Preview image: {PREVIEW_IMAGE_PATH}")
        print(f"Full image: {FULL_IMAGE_PATH}")

    except RuntimeError as error:
        print(f"Observation error: {error}")
