from providers.hubble_weekly import (
    fetch_latest as fetch_hubble,
)
from providers.nasa_apod import (
    fetch_latest as fetch_nasa,
)
from providers.webb_monthly import (
    fetch_latest as fetch_webb,
)


PROVIDERS = {
    "nasa": fetch_nasa,
    "hubble": fetch_hubble,
    "webb": fetch_webb,
}


def main() -> None:
    for provider_id, fetcher in PROVIDERS.items():
        print()
        print("=" * 64)
        print(provider_id.upper())
        print("=" * 64)

        try:
            item = fetcher()

            print(f"ID:      {item.item_id}")
            print(f"Title:   {item.title}")
            print(f"Date:    {item.date or 'Unavailable'}")
            print(f"Source:  {item.source_name}")
            print(f"Preview: {item.preview_url}")
            print(f"Full:    {item.full_url}")
            print(f"Page:    {item.page_url}")

        except RuntimeError as error:
            print(f"FAILED: {error}")


if __name__ == "__main__":
    main()
