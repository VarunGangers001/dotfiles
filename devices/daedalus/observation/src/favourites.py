import re
import shutil
from pathlib import Path


FAVOURITES_ROOT = (
    Path.home()
    / "Pictures"
    / "Observation"
    / "Favourites"
)


def safe_name(value: str) -> str:
    """Convert text into a filesystem-safe filename."""

    cleaned = re.sub(
        r"[^A-Za-z0-9._-]+",
        "-",
        value.strip(),
    )

    return cleaned.strip("-") or "observation"


def favourite_path(metadata: dict, full_image: Path) -> Path:
    """Return the saved image path for one favourite."""

    provider_id = safe_name(
        metadata.get("provider_id", "unknown")
    )

    title = safe_name(
        metadata.get("title", "observation")
    )

    suffix = full_image.suffix or ".jpg"

    return (
        FAVOURITES_ROOT
        / provider_id
        / f"{title}{suffix}"
    )


def is_favourite(
    metadata: dict,
    full_image: Path | None = None,
) -> bool:
    """Check whether this observation image has been saved."""

    if full_image is None:
        return False

    return favourite_path(
        metadata,
        full_image,
    ).exists()


def save_favourite(
    metadata: dict,
    full_image: Path,
    render_path: Path | None = None,
) -> Path:
    """Save only the full-resolution image."""

    if not full_image.exists():
        raise RuntimeError(
            "The full-resolution image is unavailable."
        )

    destination = favourite_path(
        metadata,
        full_image,
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(
        full_image,
        destination,
    )

    return destination
