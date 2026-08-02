from pathlib import Path
import subprocess


def render_contour(
    input_image: Path,
    output_text: Path,
    working_image: Path,
    width: int = 64,
    height: int = 26,
    resize_width: int = 700,
    blur: float = 3.0,
    contrast: int = 8,
    edge: float = 1.0,
    threshold: int = 45,
) -> None:
    """Create a gold-on-navy Unicode contour render."""

    image_command = [
        "magick",
        str(input_image),
        "-resize",
        f"{resize_width}x",
        "-colorspace",
        "Gray",
        "-blur",
        f"0x{blur}",
        "-contrast-stretch",
        f"{contrast}%x{contrast}%",
        "-edge",
        str(edge),
        "-normalize",
        "-threshold",
        f"{threshold}%",
        "-morphology",
        "Close",
        "Diamond",
        str(working_image),
    ]

    try:
        subprocess.run(
            image_command,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError(
            "ImageMagick is not installed or 'magick' is unavailable"
        ) from error
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"ImageMagick failed: {error.stderr.strip()}"
        ) from error

    chafa_command = [
        "chafa",
        "--format",
        "symbols",
        "--colors",
        "none",
        "--symbols",
        "braille",
        "--size",
        f"{width}x{height}",
        "--work",
        "9",
        str(working_image),
    ]

    try:
        result = subprocess.run(
            chafa_command,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError(
            "Chafa is not installed or unavailable"
        ) from error
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"Chafa failed: {error.stderr.strip()}"
        ) from error

    gold = "\033[38;2;250;169;104m"
    navy = "\033[48;2;5;24;46m"
    reset = "\033[0m"

    coloured_render = "".join(
        f"{gold}{navy}{line}{reset}\n"
        for line in result.stdout.splitlines()
    )

    output_text.write_text(
        coloured_render,
        encoding="utf-8",
    )
