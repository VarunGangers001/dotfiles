import json
from pathlib import Path
from typing import Any

from apod import fetch_apod
from cache import (
    FULL_IMAGE_PATH,
    METADATA_PATH,
    PREVIEW_IMAGE_PATH,
    download_file,
    save_metadata,
)
from renderer import PLAIN_RENDER_PATH, render_observation


def read_cached_metadata() -> dict[str, Any]:
    """Read the existing cached metadata, if available."""

    if not METADATA_PATH.exists():
        return {}

    try:
        return json.loads(
            METADATA_PATH.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError):
        return {}


def cached_files_are_complete() -> bool:
    """Check whether all files needed by Observation exist."""

    return (
        PREVIEW_IMAGE_PATH.exists()
        and FULL_IMAGE_PATH.exists()
        and PLAIN_RENDER_PATH.exists()
    )


def choose_image_urls(
    metadata: dict[str, Any],
) -> tuple[str, str]:
    """Choose suitable preview and full-resolution URLs."""

    media_type = metadata.get("media_type")

    if media_type == "image":
        preview_url = metadata.get("url")
        full_url = metadata.get("hdurl") or preview_url
    elif media_type == "video":
        preview_url = metadata.get("thumbnail_url")
        full_url = preview_url
    else:
        raise RuntimeError(
            f"Unsupported APOD media type: {media_type}"
        )

    if not preview_url or not full_url:
        raise RuntimeError(
            "NASA did not provide a usable image URL"
        )

    return preview_url, full_url


def refresh_observation() -> bool:
    """
    Refresh the cached observation when necessary.

    Returns True when files were updated and False when the
    existing cache was already current.
    """

    remote_metadata = fetch_apod()
    cached_metadata = read_cached_metadata()

    remote_date = remote_metadata.get("date")
    cached_date = cached_metadata.get("date")

    needs_download = (
        remote_date != cached_date
        or not cached_files_are_complete()
    )

    if not needs_download:
        print(
            f"Observation is already current: {remote_date}"
        )
        return False

    preview_url, full_url = choose_image_urls(
        remote_metadata
    )

    print(
        f"Refreshing Observation for {remote_date}..."
    )

    download_file(
        preview_url,
        PREVIEW_IMAGE_PATH,
    )
    download_file(
        full_url,
        FULL_IMAGE_PATH,
    )
    save_metadata(remote_metadata)

    render_observation("engraved")

    print(
        f"Observation updated: "
        f"{remote_metadata.get('title', 'Untitled')}"
    )

    return True


if __name__ == "__main__":
    try:
        refresh_observation()
    except RuntimeError as error:
        print(f"Observation refresh failed: {error}")
        raise SystemExit(1)
    except OSError as error:
        print(f"Observation file error: {error}")
        raise SystemExit(1)
