import argparse

from cache import CACHE_ROOT, provider_paths
from renderers.contour import render_contour
from renderers.presets import PRESETS


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Experiment with Daedalus Observation renders."
    )

    parser.add_argument(
        "--source",
        choices=("nasa", "hubble", "webb"),
        default="nasa",
        help="Cached image source to render.",
    )

    parser.add_argument(
        "--preset",
        choices=PRESETS.keys(),
        default="engraved",
        help="Renderer preset.",
    )

    parser.add_argument(
        "--blur",
        type=float,
        default=None,
        help="Override the preset blur strength.",
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=None,
        help="Override the preset threshold percentage.",
    )

    parser.add_argument(
        "--edge",
        type=float,
        default=None,
        help="Override the preset edge strength.",
    )

    parser.add_argument(
        "--contrast",
        type=int,
        default=None,
        help="Override the preset contrast percentage.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    source_paths = provider_paths(args.source)
    preview_path = source_paths["preview"]

    if not preview_path.exists():
        raise RuntimeError(
            f"Preview image is missing: {preview_path}"
        )

    settings = PRESETS[args.preset].copy()

    if args.blur is not None:
        settings["blur"] = args.blur

    if args.threshold is not None:
        settings["threshold"] = args.threshold

    if args.edge is not None:
        settings["edge"] = args.edge

    if args.contrast is not None:
        settings["contrast"] = args.contrast

    playground_dir = CACHE_ROOT / "playground" / args.source
    playground_dir.mkdir(parents=True, exist_ok=True)

    render_path = playground_dir / "render.txt"
    plain_path = playground_dir / "render-plain.txt"
    working_path = playground_dir / "render-source.png"

    render_contour(
        input_image=preview_path,
        output_text=render_path,
        plain_output=plain_path,
        working_image=working_path,
        **settings,
    )

    print(render_path.read_text(encoding="utf-8"))

    print("\n------------------------------------------")
    print(f"Source:      {args.source}")
    print(f"Preset:      {args.preset}")
    print(f"Size:        {settings['width']} x {settings['height']}")
    print(f"Resize:      {settings['resize_width']} px")
    print(f"Blur:        {settings['blur']}")
    print(f"Contrast:    {settings['contrast']}%")
    print(f"Edge:        {settings['edge']}")
    print(f"Threshold:   {settings['threshold']}%")
    print(f"Symbols:     {settings['symbols']}")
    print(f"Foreground:  {settings['foreground']}")
    print(f"Background:  {settings['background']}")
    print("------------------------------------------")
    print(f"Processed image: {working_path}")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, OSError) as error:
        print(f"Playground error: {error}")
