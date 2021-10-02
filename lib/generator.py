import math
from io import BytesIO

import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import getAscent
from reportlab.pdfgen.canvas import Canvas

from lib.qrcrc import calc_crc


def gen_qr(data):
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=0,
    )

    qr.clear()
    qr.add_data(data)
    return qr.make_image(fill_color="black", back_color="white")


def cm(x):
    import reportlab.lib.units
    return x * reportlab.lib.units.cm


def mm(x):
    import reportlab.lib.units
    return x * reportlab.lib.units.mm


def generate(base_size_mm: float = 10, margin_mm: float = 2, prefix: str = "", suffix: str = "", digits: int = 5, start: int = 0,
             generate_label: bool = True, label_spacing_mm: float = 0.4, font_size: int = 5):
    f = BytesIO()

    page_width, page_height = A4
    canvas = Canvas(f, pagesize=A4)

    font = "Helvetica", font_size
    label_height = getAscent(*font) + mm(label_spacing_mm)

    tile_base_size = mm(base_size_mm)

    tile_margin = mm(margin_mm)

    tile_width = tile_base_size + tile_margin
    tile_height = tile_base_size + tile_margin

    if generate_label:
        tile_height += label_height

    num = start
    pos_x = tile_margin
    pos_y = page_height - tile_margin
    while True:
        txt = f"{prefix}{num:0{digits}}{suffix}"
        data_txt = f"V1.{txt}.{calc_crc(txt)}"
        num += 1

        img = gen_qr(data_txt)

        canvas.drawInlineImage(img, pos_x, pos_y - tile_base_size, width=tile_base_size, height=tile_base_size)

        if generate_label:
            label_size = canvas.stringWidth(txt, *font)

            text_obj = canvas.beginText(
                    pos_x + tile_base_size / 2 - label_size / 2,
                    pos_y - tile_base_size - label_height)
            text_obj.setFont(*font)
            text_obj.textLines(txt)

            canvas.drawText(text_obj)

        pos_x += tile_width

        if pos_x + tile_width > page_width:
            pos_x = tile_margin
            pos_y -= tile_height

            if pos_y - tile_height < tile_margin:
                break

    canvas.save()

    f.seek(0)
    return f


__all__ = [
    "generate",
]