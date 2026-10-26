"""
Image helpers (Pillow only, no Streamlit): load a picture cropped to its slot,
or fitted whole inside it (screenshots), and build the hero "print": the
portrait (or a labelled stand-in) with a solid sage block offset behind it.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

# Size each slot is rendered at.
RENDER_WIDTH = {(3, 2): 1200, (4, 5): 960, (1, 1): 800}

# Keep in sync with .streamlit/config.toml and assets/style.css.
SAGE = "#8fa37a"
SURFACE = "#eae8e1"
INK = "#1f1f1f"
MUTED_INK = "#55534e"

PRINT_OFFSET = 0.08  # how far the sage block sits down and right, as a share of the photo width
STAND_IN_FONTS = ["georgiai.ttf", "DejaVuSerif-Italic.ttf", "LiberationSerif-Italic.ttf"]


def find_image(path: str) -> Path | None:
    """The file at `path`, or one with the same name and another image extension."""
    wanted = Path(path)
    if not wanted.is_absolute():
        wanted = ROOT / wanted
    for candidate in [wanted, *(wanted.with_suffix(ext) for ext in EXTENSIONS)]:
        if candidate.is_file():
            return candidate
    return None


def slot_size(ratio: tuple[int, int]) -> tuple[int, int]:
    width = RENDER_WIDTH.get(ratio, 1200)
    return width, round(width * ratio[1] / ratio[0])


def load_image(path: str, ratio: tuple[int, int], crop: bool = True) -> Image.Image | None:
    """The picture sized to a `ratio` slot, or None if it's missing or unreadable.

    crop=True fills the slot (center-cropped); crop=False fits the whole picture
    inside it on a surface-coloured mat, so nothing is cut off or stretched.
    """
    found = find_image(path)
    if found is None:
        return None
    try:
        with Image.open(found) as img:
            img = ImageOps.exif_transpose(img).convert("RGB")
            if crop:
                return ImageOps.fit(img, slot_size(ratio), Image.Resampling.LANCZOS)
            return ImageOps.pad(img, slot_size(ratio), Image.Resampling.LANCZOS, color=SURFACE)
    except (OSError, ValueError):
        return None


def _stand_in_font(size: int) -> tuple[ImageFont.ImageFont, str]:
    """A serif italic if the system has one, plus the dash it can draw."""
    for name in STAND_IN_FONTS:
        try:
            return ImageFont.truetype(name, size), "—"
        except OSError:
            continue
    return ImageFont.load_default(size=size), "-"  # Pillow's default font has no em dash


def stand_in(ratio: tuple[int, int], name: str) -> Image.Image:
    """A flat surface block, labelled so nobody mistakes it for a missing image."""
    width, height = slot_size(ratio)
    img = Image.new("RGB", (width, height), SURFACE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width - 1, height - 1], outline=SAGE, width=3)
    font, dash = _stand_in_font(max(28, width // 16))
    draw.multiline_text(
        (width / 2, height / 2), f"Photo coming soon {dash}\n{name}",
        fill=MUTED_INK, font=font, anchor="mm", align="center", spacing=18,
    )
    return img


def stand_in_label(name: str) -> str:
    return f"Photo coming soon — {name}"


def print_frame(photo: Image.Image) -> Image.Image:
    """`photo` on a transparent canvas with a sage block offset behind it."""
    offset = round(photo.width * PRINT_OFFSET)
    canvas = Image.new("RGBA", (photo.width + offset, photo.height + offset), (0, 0, 0, 0))
    canvas.paste(Image.new("RGBA", photo.size, SAGE), (offset, offset))
    canvas.paste(photo.convert("RGBA"), (0, 0))
    return canvas


def profile_print(path: str, ratio: tuple[int, int], name: str) -> tuple[Image.Image, bool]:
    """(the framed portrait, True) or (the framed stand-in, False)."""
    photo = load_image(path, ratio)
    if photo is None:
        return print_frame(stand_in(ratio, name)), False
    return print_frame(photo), True
