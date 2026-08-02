from dataclasses import asdict
from pathlib import Path

from cache import (
    download_file,
    provider_paths,
    read_metadata,
    save_metadata,
)
from providers.common import ObservationItem
from providers.registry import PROVIDERS
from renderers.contour import render_contour
from renderers.presets import PRESETS


DEFAULT_RENDERER = "engraved"


def cache_is_complete(provider_id: str) -> bool:
    paths = provider_paths(provider_id)

    return all(
        paths[key].exists()
        for key in (
            "metadata",
            "preview",
            "full",
            "render_plain",
        )
    )


def refresh_provider(
    provider_id: str,
    force: bool = False,
) -> bool:
    """
    Refresh one provider.

    Returns True when its cache changed.
    """

    if provider_id not in PROVIDERS:
        raise ValueError(
            f"Unknown provider: {provider_id}"
        )

    item = PROVIDERS[provider_id]()
    paths = provider_paths(provider_id)
    cached = read_metadata(paths["metadata"])

    already_current = (
        cached.get("item_id") == item.item_id
        and cache_is_complete(provider_id)
    )

    if already_current and not force:
        print(
            f"{provider_id}: already current "
            f"({item.item_id})"
        )
        return False

    print(
        f"{provider_id}: downloading {item.item_id}..."
    )

    download_file(item.preview_url, paths["preview"])
    download_file(item.full_url, paths["full"])

    metadata = asdict(item)
    save_metadata(metadata, paths["metadata"])

    settings = PRESETS[DEFAULT_RENDERER]

    render_contour(
        input_image=paths["preview"],
        output_text=paths["render"],
        plain_output=paths["render_plain"],
        working_image=paths["render_source"],
        **settings,
    )

    print(f"{provider_id}: updated — {item.title}")
    return True


def refresh_all() -> None:
    """Refresh every configured provider independently."""

    failures: list[str] = []

    for provider_id in PROVIDERS:
        try:
            refresh_provider(provider_id)
        except (RuntimeError, ValueError, OSError) as error:
            failures.append(
                f"{provider_id}: {error}"
            )
            print(f"{provider_id}: failed — {error}")

    if failures:
        print()
        print("Some sources could not be refreshed:")
        for failure in failures:
            print(f"  {failure}")


def load_provider(
    provider_id: str,
) -> tuple[dict, Path, Path]:
    """
    Load cached metadata, rendered artwork and full image.
    """

    paths = provider_paths(provider_id)
    metadata = read_metadata(paths["metadata"])

    if not metadata:
        raise RuntimeError(
            f"No cached metadata for {provider_id}"
        )

    if not paths["render_plain"].exists():
        raise RuntimeError(
            f"No cached render for {provider_id}"
        )

    if not paths["full"].exists():
        raise RuntimeError(
            f"No cached full image for {provider_id}"
        )

    return (
        metadata,
        paths["render_plain"],
        paths["full"],
    )


if __name__ == "__main__":
    refresh_all()
