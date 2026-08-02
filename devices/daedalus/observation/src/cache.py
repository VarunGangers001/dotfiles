import json
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


CACHE_ROOT = Path.home() / ".cache" / "daedalus" / "observation"

# Compatibility paths used by Observation v1.
CACHE_DIR = CACHE_ROOT
METADATA_PATH = CACHE_ROOT / "metadata.json"
PREVIEW_IMAGE_PATH = CACHE_ROOT / "preview.jpg"
FULL_IMAGE_PATH = CACHE_ROOT / "full.jpg"


def provider_cache_dir(provider_id: str) -> Path:
    """Return the dedicated cache directory for one provider."""

    return CACHE_ROOT / provider_id


def provider_paths(provider_id: str) -> dict[str, Path]:
    """Return every cached file path for one provider."""

    cache_dir = provider_cache_dir(provider_id)

    return {
        "directory": cache_dir,
        "metadata": cache_dir / "metadata.json",
        "preview": cache_dir / "preview.jpg",
        "full": cache_dir / "full.jpg",
        "render": cache_dir / "render.txt",
        "render_plain": cache_dir / "render-plain.txt",
        "render_source": cache_dir / "render-source.png",
    }


def ensure_cache_directory(
    provider_id: str | None = None,
) -> Path:
    """Create and return the requested cache directory."""

    directory = (
        provider_cache_dir(provider_id)
        if provider_id
        else CACHE_ROOT
    )

    directory.mkdir(parents=True, exist_ok=True)
    return directory


def save_metadata(
    metadata: dict[str, Any],
    destination: Path | None = None,
) -> None:
    """Save metadata as readable JSON."""

    path = destination or METADATA_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def read_metadata(path: Path) -> dict[str, Any]:
    """Read cached metadata, returning an empty dictionary on failure."""

    if not path.exists():
        return {}

    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError):
        return {}


def download_file(url: str, destination: Path) -> None:
    """Download a remote file into the cache."""

    destination.parent.mkdir(parents=True, exist_ok=True)

    request = Request(
        url,
        headers={
            "User-Agent": (
                "Daedalus-Observation/2.0 "
                "(personal desktop astronomy viewer)"
            )
        },
    )

    try:
        with urlopen(request, timeout=60) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"Download returned HTTP status "
                    f"{response.status}"
                )

            destination.write_bytes(response.read())

    except HTTPError as error:
        raise RuntimeError(
            f"Download failed with HTTP status {error.code}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"Could not download file: {error.reason}"
        ) from error

    except TimeoutError as error:
        raise RuntimeError(
            f"Download timed out: {url}"
        ) from error
