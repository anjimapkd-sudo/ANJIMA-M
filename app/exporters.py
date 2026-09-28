from datetime import datetime
from pathlib import Path

from fpdf import FPDF

from .config import EXPORTS_DIR, STATIC_DIR


def _local_image(url_path: str) -> str:
    relative = url_path.replace("/static/", "")
    return str(STATIC_DIR / relative)


def _clean(text: str) -> str:
    if text is None:
        return ""
    return str(text).encode("latin-1", "replace").decode("latin-1")


def _add_text_block(pdf, heading, text):
    """
    Adds a neatly aligned heading and paragraph.
    """
    pdf.set_x(15)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, _clean(heading), ln=True)

    pdf.set_x(15)

    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(
        180,
        6,
        _clean(text),
        border=0,
        align="L"
    )

    pdf.ln(3)


def save_pdf(layout, comic_id: str) -> str:
    filename = (
        f"comic_{comic_id}_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    output = EXPORTS_DIR / filename

    pdf = FPDF(format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=18)

    text_width = 180

    for panel in layout:
        pdf.add_page()

        # -------------------------
        # PANEL TITLE
        # -------------------------
        pdf.set_x(15)
        pdf.set_font("Helvetica", "B", 18)

        title = _clean(
            f"Panel {panel['panel_number']}: {panel['title']}"
        )

        pdf.multi_cell(
            text_width,
            10,
            title,
            border=0,
            align="L"
        )

        pdf.ln(5)

        # -------------------------
        # PANEL IMAGE
        # -------------------------
        image = _local_image(panel["image_path"])

        if Path(image).exists():
            pdf.image(
                image,
                x=15,
                y=pdf.get_y(),
                w=180
            )

        pdf.ln(128)

        # -------------------------
        # DESCRIPTION
        # -------------------------
        _add_text_block(
            pdf,
            "Description",
            panel["scene_description"]
        )

        # -------------------------
        # CAPTION
        # -------------------------
        _add_text_block(
            pdf,
            "Caption",
            panel["caption"]
        )

        # -------------------------
        # NARRATION
        # -------------------------
        _add_text_block(
            pdf,
            "Narration",
            panel["narration"]
        )

    pdf.output(str(output))

    return f"/static/exports/{filename}"