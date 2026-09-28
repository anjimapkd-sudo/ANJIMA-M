import re
import uuid
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .config import PANELS_DIR


def _safe_name(text: str) -> str:
    return (
        re.sub(r"[^a-zA-Z0-9_-]+", "_", text)[:50].strip("_")
        or "panel"
    )


def _get_font(size: int, bold: bool = False):
    font_names = []

    if bold:
        font_names = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
        ]
    else:
        font_names = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
        ]

    for font_path in font_names:
        try:
            return ImageFont.truetype(font_path, size)
        except OSError:
            pass

    return ImageFont.load_default()


def _draw_wrapped_text(draw, text, xy, font, fill, max_width):
    words = str(text).split()
    lines = []
    current = ""

    for word in words:
        test = current + " " + word if current else word

        if draw.textbbox((0, 0), test, font=font)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    x, y = xy

    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + 8

    return y


def _draw_fox(draw, panel_number):
    """
    Draws a simple colourful cartoon fox.
    """

    # Ground / grass
    draw.rectangle((0, 580, 1024, 768), fill="#75b85c")

    # Trees
    for x in [80, 230, 800, 930]:
        draw.rectangle((x - 15, 300, x + 15, 600), fill="#70452a")
        draw.ellipse(
            (x - 90, 190, x + 90, 380),
            fill="#2f8f46",
            outline="#174d29",
            width=5,
        )
        draw.ellipse(
            (x - 60, 150, x + 100, 330),
            fill="#3da653",
            outline="#174d29",
            width=5,
        )

    # Fox body
    draw.ellipse(
        (380, 390, 650, 620),
        fill="#e87932",
        outline="#8c3d19",
        width=7,
    )

    # Tail
    draw.ellipse(
        (560, 430, 790, 590),
        fill="#e87932",
        outline="#8c3d19",
        width=7,
    )

    draw.ellipse(
        (700, 465, 790, 590),
        fill="#fff4df",
        outline="#8c3d19",
        width=5,
    )

    # Head
    draw.ellipse(
        (390, 220, 640, 450),
        fill="#e87932",
        outline="#8c3d19",
        width=7,
    )

    # Ears
    draw.polygon(
        [(405, 280), (420, 150), (490, 245)],
        fill="#e87932",
        outline="#8c3d19",
    )

    draw.polygon(
        [(540, 245), (610, 150), (625, 285)],
        fill="#e87932",
        outline="#8c3d19",
    )

    # Inner ears
    draw.polygon(
        [(425, 245), (430, 185), (465, 240)],
        fill="#f4a3a3",
    )

    draw.polygon(
        [(565, 240), (600, 185), (605, 250)],
        fill="#f4a3a3",
    )

    # Face
    draw.ellipse(
        (445, 300, 585, 425),
        fill="#fff1d6",
    )

    # Eyes
    draw.ellipse((455, 315, 475, 340), fill="black")
    draw.ellipse((550, 315, 570, 340), fill="black")

    # Nose
    draw.ellipse((505, 350, 525, 370), fill="black")

    # Smile
    draw.arc((475, 350, 555, 410), 10, 170, fill="black", width=4)

    # Legs
    draw.rounded_rectangle(
        (420, 535, 470, 660),
        radius=20,
        fill="#e87932",
        outline="#8c3d19",
        width=5,
    )

    draw.rounded_rectangle(
        (560, 535, 610, 660),
        radius=20,
        fill="#e87932",
        outline="#8c3d19",
        width=5,
    )

    # Different action for different panels
    if panel_number == 2:
        # Magic glow
        for r in range(80, 20, -15):
            draw.ellipse(
                (500 - r, 390 - r, 500 + r, 390 + r),
                outline="#f7d64a",
                width=8,
            )

    elif panel_number == 3:
        # Shield
        draw.polygon(
            [(650, 300), (750, 340), (725, 500), (650, 550), (575, 500), (550, 340)],
            fill="#5aa9e6",
            outline="#173f67",
        )

    elif panel_number == 4:
        # Lightning / danger
        draw.line(
            [(760, 170), (710, 300), (770, 300), (700, 450)],
            fill="#f4d03f",
            width=18,
        )

    elif panel_number == 5:
        # Flowers
        for x, y in [(170, 620), (250, 650), (820, 620), (900, 650)]:
            draw.ellipse((x - 12, y - 12, x + 12, y + 12), fill="#f06b8d")
            draw.ellipse((x - 12, y - 35, x + 12, y - 10), fill="#f06b8d")
            draw.ellipse((x - 35, y - 12, x - 10, y + 12), fill="#f06b8d")
            draw.ellipse((x + 10, y - 12, x + 35, y + 12), fill="#f06b8d")
            draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill="#ffd447")


def _create_comic_panel(prompt: str, panel_number: int, output: Path):
    width = 1024
    height = 768

    # Colourful sky
    image = Image.new("RGB", (width, height), "#9ddcff")
    draw = ImageDraw.Draw(image)

    # Sun
    draw.ellipse(
        (800, 50, 930, 180),
        fill="#ffd34e",
        outline="#e0a800",
        width=5,
    )

    # Decorative clouds
    for x, y in [(80, 80), (280, 120), (650, 100)]:
        draw.ellipse((x, y, x + 90, y + 55), fill="white")
        draw.ellipse((x + 35, y - 20, x + 125, y + 55), fill="white")
        draw.ellipse((x + 70, y, x + 160, y + 55), fill="white")

    # Comic border
    draw.rounded_rectangle(
        (20, 20, 1004, 748),
        radius=20,
        outline="#222222",
        width=10,
    )

    # Title
    title_font = _get_font(34, bold=True)

    title = f"COMICCRAFT - PANEL {panel_number}"

    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]

    draw.rounded_rectangle(
        (45, 40, 45 + title_width + 35, 95),
        radius=12,
        fill="#ffffff",
        outline="#222222",
        width=3,
    )

    draw.text(
        (62, 50),
        title,
        font=title_font,
        fill="#222222",
    )

    # Draw fox and forest
    _draw_fox(draw, panel_number)

    # Story text box
    box_top = 610

    draw.rounded_rectangle(
        (55, box_top, 969, 725),
        radius=15,
        fill="#fffdf5",
        outline="#222222",
        width=4,
    )

    text_font = _get_font(21)

    clean_prompt = str(prompt).strip()

    if len(clean_prompt) > 250:
        clean_prompt = clean_prompt[:247] + "..."

    _draw_wrapped_text(
        draw,
        clean_prompt,
        (75, box_top + 15),
        text_font,
        "#222222",
        875,
    )

    image.save(output, "PNG")


def generate_image(prompt: str, panel_number: int) -> str:
    filename = (
        f"panel_{panel_number}_"
        f"{uuid.uuid4().hex[:8]}_"
        f"{_safe_name(prompt)}.png"
    )

    output = PANELS_DIR / filename

    PANELS_DIR.mkdir(parents=True, exist_ok=True)

    _create_comic_panel(
        prompt=prompt,
        panel_number=panel_number,
        output=output,
    )

    return f"/static/panels/{filename}"