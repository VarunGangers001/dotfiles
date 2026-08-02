from pathlib import Path

from cache import CACHE_DIR, PREVIEW_IMAGE_PATH
from renderers.contour import render_contour


RENDER_PATH = CACHE_DIR / "render.txt"
WORKING_IMAGE_PATH = CACHE_DIR / "render-source.png"


def render_observation(mode: str = "contour") -> Path:
    """Render the cached observation using the requested renderer."""

    if not PREVIEW_IMAGE_PATH.exists():
        raise RuntimeError(
            f"Preview image does not exist: {PREVIEW_IMAGE_PATH}"
        )

    if mode == "contour":
        render_contour(
            input_image=PREVIEW_IMAGE_PATH,
            output_text=RENDER_PATH,
            working_image=WORKING_IMAGE_PATH,
        )
    else:
        raise ValueError(f"Unknown render mode: {mode}")

    return RENDER_PATH


if __name__ == "__main__":
    try:
        path = render_observation()
        print(path.read_text(encoding="utf-8"))
        print(f"\nSaved render to: {path}")

    except (RuntimeError, ValueError) as error:
        print(f"Render error: {error}")
