from source_manager import refresh_all


def main() -> None:
    """Refresh every configured Observation source."""

    print("Starting Observation refresh...")
    refresh_all()
    print("Observation refresh complete.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, OSError) as error:
        print(f"Observation refresh failed: {error}")
        raise SystemExit(1)
