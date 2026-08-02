import json
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "daedalus"
CONFIG_PATH = CONFIG_DIR / "observation.json"

DEFAULT_PREFERENCES = {
    "provider": "nasa",
}


def load_preferences() -> dict:
    """Load Observation preferences from disk."""

    if not CONFIG_PATH.exists():
        return DEFAULT_PREFERENCES.copy()

    try:
        saved = json.loads(
            CONFIG_PATH.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError):
        return DEFAULT_PREFERENCES.copy()

    preferences = DEFAULT_PREFERENCES.copy()
    preferences.update(saved)

    return preferences


def save_preferences(preferences: dict) -> None:
    """Save Observation preferences to disk."""

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    CONFIG_PATH.write_text(
        json.dumps(
            preferences,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def get_selected_provider() -> str:
    """Return the last selected provider."""

    return load_preferences().get(
        "provider",
        DEFAULT_PREFERENCES["provider"],
    )


def set_selected_provider(provider_id: str) -> None:
    """Remember the selected provider."""

    preferences = load_preferences()
    preferences["provider"] = provider_id
    save_preferences(preferences)
