from collections.abc import Callable

from providers.common import ObservationItem
from providers.hubble_monthly import fetch_latest as fetch_hubble
from providers.nasa_apod import fetch_latest as fetch_nasa
from providers.webb_monthly import fetch_latest as fetch_webb


ProviderFetcher = Callable[[], ObservationItem]


PROVIDERS: dict[str, ProviderFetcher] = {
    "nasa": fetch_nasa,
    "hubble": fetch_hubble,
    "webb": fetch_webb,
}


DISPLAY_NAMES = {
    "nasa": "NASA APOD",
    "hubble": "Hubble Weekly",
    "webb": "Webb Monthly",
}
