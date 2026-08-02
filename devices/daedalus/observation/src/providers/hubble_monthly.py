import re

from providers.common import (
    ObservationItem,
    choose_largest_image,
    extract_page_metadata,
    extract_release_date,
    find_latest_entry,
)


INDEX_URL = "https://esahubble.org/images/potm/"


def extract_item_id(page_url: str) -> str:
    match = re.search(
        r"/images/(potm\d+[a-z]?)/?",
        page_url,
        flags=re.IGNORECASE,
    )

    if not match:
        raise RuntimeError(
            f"Could not determine the Hubble item ID: {page_url}"
        )

    return match.group(1).lower()


def fetch_latest() -> ObservationItem:
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
        " | ESA/Hubble",
        "",
    ).strip()

    description = (
        parser.meta.get("og:description")
        or parser.meta.get("description")
        or ""
    )

    return ObservationItem(
        provider_id="hubble",
        source_name="ESA/Hubble Picture of the Month",
        item_id=item_id,
        title=title,
        date=extract_release_date(parser),
        description=description,
        preview_url=preview_url,
        full_url=full_url,
        page_url=page_url,
    )
