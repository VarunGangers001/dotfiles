from pathlib import Path
import subprocess


def hex_to_rgb(hex_colour: str) -> tuple[int, int, int]:
    """Convert a six-digit hexadecimal colour into RGB values."""

    cleaned = hex_colour.lstrip("#")

    if len(cleaned) != 6:
        raise ValueError(
            f"Expected a six-digit hex colour, got: {hex_colour}"
        )

    return tuple(
        int(cleaned[index:index + 2], 16)
        for index in (0, 2, 4)
    )


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
    symbols: str = "braille",
    foreground: str = "#faa968",
    background: str = "#05182e",
    plain_output: Path | None = None,
) -> None:
    """Create terminal-coloured and plain Unicode contour renders."""

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
        symbols,
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

    plain_render = result.stdout.rstrip() + "\n"

    if plain_output is not None:
        plain_output.write_text(
            plain_render,
            encoding="utf-8",
        )

    foreground_rgb = hex_to_rgb(foreground)
    background_rgb = hex_to_rgb(background)

    foreground_code = (
        f"\033[38;2;"
        f"{foreground_rgb[0]};"
        f"{foreground_rgb[1]};"
        f"{foreground_rgb[2]}m"
    )

    background_code = (
        f"\033[48;2;"
        f"{background_rgb[0]};"
        f"{background_rgb[1]};"
        f"{background_rgb[2]}m"
    )

    reset = "\033[0m"

    coloured_render = "".join(
        f"{foreground_code}{background_code}{line}{reset}\n"
        for line in plain_render.splitlines()
    )

    output_text.write_text(
        coloured_render,
        encoding="utf-8",
    )
