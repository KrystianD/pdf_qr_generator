import math
from io import BytesIO

import qrcode
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


def mm(x):
    import reportlab.lib.units
    return x * reportlab.lib.units.mm


def generate(page_width_mm: float, page_height_mm: float,
             base_size_mm: float = 10, margin_x_mm: float = 2, margin_y_mm: float = 2, stride_x_mm: float = 0, stride_y_mm: float = 0,
             prefix: str = "", suffix: str = "", digits: int = 5, start: int = 0, pages: int = 1,
             generate_label: bool = True, label_spacing_mm: float = 0.4, font_size: int = 5):
    f = BytesIO()

    page_width = mm(page_width_mm)
    page_height = mm(page_height_mm)
    canvas = Canvas(f, pagesize=(page_width, page_height))

    font = "Helvetica", font_size
    label_height = getAscent(*font) + mm(label_spacing_mm)

    tile_base_size = mm(base_size_mm)

    tile_margin_x = mm(margin_x_mm)
    tile_margin_y = mm(margin_y_mm)

    tile_width = tile_base_size + tile_margin_x
    tile_height = tile_base_size + tile_margin_y

    if generate_label:
        tile_height += label_height

    stride_x = max(mm(stride_x_mm), tile_width)
    stride_y = max(mm(stride_y_mm), tile_height)

    num = start
    page = 0
    pos_x = tile_margin_x
    pos_y = page_height - tile_margin_y
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

        pos_x += stride_x

        if pos_x + tile_width > page_width:
            pos_x = tile_margin_x
            pos_y -= stride_y

            if pos_y - tile_height < tile_margin_y:
                canvas.showPage()
                page += 1
                pos_y = page_height - tile_margin_y
                if page == pages:
                    break

    canvas.save()

    f.seek(0)
    return f


__all__ = [
    "generate",
]
