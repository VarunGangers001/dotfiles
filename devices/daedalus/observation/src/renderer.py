from pathlib import Path

from cache import CACHE_DIR, PREVIEW_IMAGE_PATH
from renderers.contour import render_contour
from renderers.presets import PRESETS


TERMINAL_RENDER_PATH = CACHE_DIR / "render.txt"
PLAIN_RENDER_PATH = CACHE_DIR / "render-plain.txt"
WORKING_IMAGE_PATH = CACHE_DIR / "render-source.png"


def render_observation(mode: str = "engraved") -> Path:
    """Render the cached observation using a named preset."""

    if not PREVIEW_IMAGE_PATH.exists():
        raise RuntimeError(
            f"Preview image does not exist: {PREVIEW_IMAGE_PATH}"
        )

    if mode not in PRESETS:
        raise ValueError(f"Unknown render mode: {mode}")

    settings = PRESETS[mode]

    render_contour(
        input_image=PREVIEW_IMAGE_PATH,
        output_text=TERMINAL_RENDER_PATH,
        plain_output=PLAIN_RENDER_PATH,
        working_image=WORKING_IMAGE_PATH,
        **settings,
    )

    return PLAIN_RENDER_PATH


if __name__ == "__main__":
    try:
        render_observation()

        print(
            TERMINAL_RENDER_PATH.read_text(
                encoding="utf-8"
            )
        )

        print(f"\nTerminal render: {TERMINAL_RENDER_PATH}")
        print(f"GTK render:      {PLAIN_RENDER_PATH}")

    except (RuntimeError, ValueError) as error:
        print(f"Render error: {error}")
