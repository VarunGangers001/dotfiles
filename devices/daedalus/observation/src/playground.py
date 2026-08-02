import argparse

from cache import CACHE_DIR, PREVIEW_IMAGE_PATH
from renderers.contour import render_contour
from renderers.presets import PRESETS


PLAYGROUND_RENDER_PATH = CACHE_DIR / "playground-render.txt"
PLAYGROUND_IMAGE_PATH = CACHE_DIR / "playground-source.png"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Experiment with Daedalus render presets."
    )

    parser.add_argument(
        "--preset",
        choices=PRESETS.keys(),
        default="engraved",
        help="Renderer preset.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    if not PREVIEW_IMAGE_PATH.exists():
        raise RuntimeError(
            f"Preview image is missing: {PREVIEW_IMAGE_PATH}"
        )

    settings = PRESETS[args.preset]

    render_contour(
        input_image=PREVIEW_IMAGE_PATH,
        output_text=PLAYGROUND_RENDER_PATH,
        working_image=PLAYGROUND_IMAGE_PATH,
        width=settings["width"],
        height=settings["height"],
        resize_width=settings["resize_width"],
        blur=settings["blur"],
        contrast=settings["contrast"],
        edge=settings["edge"],
        threshold=settings["threshold"],
    )

    print(PLAYGROUND_RENDER_PATH.read_text(encoding="utf-8"))

    print("\n------------------------------------------")
    print(f"Preset:      {args.preset}")
    print(f"Size:        {settings['width']} x {settings['height']}")
    print(f"Resize:      {settings['resize_width']} px")
    print(f"Blur:        {settings['blur']}")
    print(f"Contrast:    {settings['contrast']}%")
    print(f"Edge:        {settings['edge']}")
    print(f"Threshold:   {settings['threshold']}%")
    print("------------------------------------------")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(f"Playground error: {error}")
