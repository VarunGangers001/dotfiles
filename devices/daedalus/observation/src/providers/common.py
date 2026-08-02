from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin
from urllib.request import Request, urlopen


USER_AGENT = (
    "Daedalus-Observation/2.0 "
    "(personal desktop astronomy viewer)"
)


@dataclass(frozen=True)
class ObservationItem:
    """Normalised metadata returned by every provider."""

    provider_id: str
    source_name: str
    item_id: str
    title: str
    date: str
    description: str
    preview_url: str
    full_url: str
    page_url: str


def fetch_text(url: str, timeout: int = 30) -> str:
    """Download a webpage and decode it as text."""

    request = Request(
        url,
        headers={"User-Agent": USER_AGENT},
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset()
            encoding = charset or "utf-8"

            return response.read().decode(
                encoding,
                errors="replace",
            )

    except HTTPError as error:
        raise RuntimeError(
            f"Request failed with HTTP status {error.code}: {url}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"Could not connect to {url}: {error.reason}"
        ) from error

    except TimeoutError as error:
        raise RuntimeError(
            f"Request timed out: {url}"
        ) from error


class LatestEntryParser(HTMLParser):
    """Find the first real image entry matching an ID pattern."""

    def __init__(
        self,
        base_url: str,
        entry_pattern: str,
    ) -> None:
        super().__init__()

        self.base_url = base_url
        self.entry_pattern = re.compile(
            entry_pattern,
            flags=re.IGNORECASE,
        )
        self.entry_url: str | None = None

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if self.entry_url is not None or tag != "a":
            return

        attributes = dict(attrs)
        href = attributes.get("href")

        if not href:
            return

        absolute_url = urljoin(self.base_url, href)
        clean_url, _fragment = urldefrag(absolute_url)

        if self.entry_pattern.search(clean_url):
            self.entry_url = clean_url


class MetadataParser(HTMLParser):
    """Extract metadata, image links and visible page text."""

    def __init__(self, base_url: str) -> None:
        super().__init__()

        self.base_url = base_url
        self.meta: dict[str, str] = {}
        self.image_links: list[str] = []
        self.time_value = ""
        self.text_chunks: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attributes = dict(attrs)

        if tag == "meta":
            key = (
                attributes.get("property")
                or attributes.get("name")
            )
            content = attributes.get("content")

            if key and content:
                self.meta[key.lower()] = content.strip()

        elif tag == "a":
            href = attributes.get("href")

            if not href:
                return

            absolute_url = urljoin(self.base_url, href)
            lowered = absolute_url.lower()

            if lowered.endswith(
                (
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".webp",
                    ".tif",
                    ".tiff",
                )
            ):
                self.image_links.append(absolute_url)

        elif tag == "time" and not self.time_value:
            self.time_value = (
                attributes.get("datetime") or ""
            ).strip()

    def handle_data(self, data: str) -> None:
        cleaned = " ".join(data.split())

        if cleaned:
            self.text_chunks.append(cleaned)

    @property
    def visible_text(self) -> str:
        return " ".join(self.text_chunks)


def find_latest_entry(
    index_url: str,
    entry_pattern: str,
) -> str:
    """Find the newest matching entry from an official index page."""

    html = fetch_text(index_url)

    parser = LatestEntryParser(
        base_url=index_url,
        entry_pattern=entry_pattern,
    )
    parser.feed(html)

    if not parser.entry_url:
        raise RuntimeError(
            f"Could not find a current entry at {index_url}"
        )

    return parser.entry_url


def extract_page_metadata(
    page_url: str,
) -> MetadataParser:
    """Read metadata and visible text from an image page."""

    html = fetch_text(page_url)

    parser = MetadataParser(page_url)
    parser.feed(html)

    return parser


def extract_release_date(parser: MetadataParser) -> str:
    """Extract and normalise an ESA/Hubble/Webb release date."""

    metadata_date = (
        parser.meta.get("article:published_time")
        or parser.meta.get("date")
        or parser.time_value
    )

    if metadata_date:
        return metadata_date[:10]

    text = parser.visible_text.replace("\xa0", " ")

    release_position = text.lower().find("release date")

    if release_position == -1:
        return ""

    nearby_text = text[
        release_position:release_position + 150
    ]

    match = re.search(
        r"(\d{1,2})\s+"
        r"([A-Za-z]+)\s+"
        r"(\d{4})",
        nearby_text,
    )

    if not match:
        return ""

    date_text = " ".join(match.groups())

    try:
        parsed = datetime.strptime(
            date_text,
            "%d %B %Y",
        )
        return parsed.strftime("%Y-%m-%d")
    except ValueError:
        return ""


def choose_largest_image(
    parser: MetadataParser,
) -> tuple[str, str]:
    """Choose suitable preview and full-resolution image URLs."""

    preview_url = (
        parser.meta.get("og:image")
        or parser.meta.get("twitter:image")
    )

    if not preview_url:
        raise RuntimeError(
            "The source page did not expose a preview image"
        )

    candidates = [
        urljoin(parser.base_url, preview_url),
        *parser.image_links,
    ]

    unique_candidates = list(dict.fromkeys(candidates))

    def image_priority(url: str) -> tuple[int, int]:
        lowered = url.lower()

        preferred_terms = (
            "publicationjpg",
            "large",
            "full",
            "original",
            "wallpaper",
        )

        preferred = int(
            any(term in lowered for term in preferred_terms)
        )

        return preferred, len(url)

    full_url = max(
        unique_candidates,
        key=image_priority,
    )

    return (
        urljoin(parser.base_url, preview_url),
        full_url,
    )
