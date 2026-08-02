from apod import fetch_apod
from providers.common import ObservationItem


def fetch_latest() -> ObservationItem:
    """Fetch the current NASA Astronomy Picture of the Day."""

    metadata = fetch_apod()

    media_type = metadata.get("media_type")

    if media_type == "image":
        preview_url = metadata.get("url")
        full_url = metadata.get("hdurl") or preview_url

    elif media_type == "video":
        preview_url = metadata.get("thumbnail_url")
        full_url = preview_url

    else:
        raise RuntimeError(
            f"Unsupported NASA APOD media type: {media_type}"
        )

    if not preview_url or not full_url:
        raise RuntimeError(
            "NASA did not provide a usable image"
        )

    date = metadata.get("date", "")

    return ObservationItem(
        provider_id="nasa",
        source_name="NASA Astronomy Picture of the Day",
        item_id=f"nasa-{date}",
        title=metadata.get(
            "title",
            "Untitled NASA Observation",
        ),
        date=date,
        description=metadata.get("explanation", ""),
        preview_url=preview_url,
        full_url=full_url,
        page_url=(
            f"https://apod.nasa.gov/apod/"
            f"ap{date.replace('-', '')[2:]}.html"
            if date
            else "https://apod.nasa.gov/apod/"
        ),
    )
