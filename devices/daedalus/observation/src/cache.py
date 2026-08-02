import json
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


CACHE_DIR = Path.home() / ".cache" / "daedalus" / "observation"
METADATA_PATH = CACHE_DIR / "metadata.json"
PREVIEW_IMAGE_PATH = CACHE_DIR / "preview.jpg"
FULL_IMAGE_PATH = CACHE_DIR / "full.jpg"


def ensure_cache_directory() -> None:
    """Create the Observation cache directory if it does not exist."""

    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def save_metadata(metadata: dict[str, Any]) -> None:
    """Save APOD metadata as readable JSON."""

    ensure_cache_directory()

    METADATA_PATH.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )


def download_file(url: str, destination: Path) -> None:
    """Download a file to the requested cache location."""

    ensure_cache_directory()

    try:
        with urlopen(url, timeout=30) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"Image download returned HTTP status {response.status}"
                )

            destination.write_bytes(response.read())

    except HTTPError as error:
        raise RuntimeError(
            f"Image download failed with HTTP status {error.code}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"Could not download image: {error.reason}"
        ) from error
