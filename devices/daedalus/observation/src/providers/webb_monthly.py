import re

from providers.common import (
    ObservationItem,
    choose_largest_image,
    extract_page_metadata,
    find_latest_entry,
)


INDEX_URL = "https://esawebb.org/images/potm/"


def extract_item_id(page_url: str) -> str:
    """Extract an identifier such as potm2606 from the URL."""

    match = re.search(
        r"/images/(potm\d+[a-z]?)/?",
        page_url,
        flags=re.IGNORECASE,
    )

    if not match:
        raise RuntimeError(
            f"Could not determine the Webb item ID: {page_url}"
        )

    return match.group(1).lower()


def extract_date(parser) -> str:
    """Find the best available publication date."""

    raw_date = (
        parser.meta.get("article:published_time")
        or parser.meta.get("date")
        or parser.time_value
    )

    if raw_date:
        return raw_date[:10]

    return ""


def fetch_latest() -> ObservationItem:
    """Fetch the latest ESA/Webb Picture of the Month."""

    page_url = find_latest_entry(
    INDEX_URL,
    r"/images/potm\d+[a-z]?/?$",
)

    item_id = extract_item_id(page_url)
    parser = extract_page_metadata(page_url)
    preview_url, full_url = choose_largest_image(parser)

    title = (
        parser.meta.get("og:title")
        or parser.meta.get("twitter:title")
        or item_id
    )

    title = title.replace(
        " | ESA/Webb",
        "",
    ).strip()

    description = (
        parser.meta.get("og:description")
        or parser.meta.get("description")
        or ""
    )

    return ObservationItem(
        provider_id="webb",
        source_name="ESA/Webb Picture of the Month",
        item_id=item_id,
        title=title,
        date=extract_date(parser),
        description=description,
        preview_url=preview_url,
        full_url=full_url,
        page_url=page_url,
    )

