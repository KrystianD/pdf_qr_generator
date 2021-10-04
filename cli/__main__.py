import argparse
import re
import sys

import reportlab.lib.pagesizes as pagesizes
from reportlab.lib.units import mm

from lib.generator import generate


def main():
    argparser = argparse.ArgumentParser(prog="python -m cli")
    argparser.add_argument('--page-size', type=str, default="A4", metavar="SIZE",
                           help="Page size. Possible values are predefined page format (A4, A5, etc) or dimensions millimeters (20x30), default: A4")
    argparser.add_argument('--landscape', action="store_true", help="Landscape orientation. For predefined formats only, default: portrait")
    argparser.add_argument('--size', type=float, default=10, metavar="MM", help="Base QR code size (in millimeters), default: 10")
    argparser.add_argument('--margin', type=float, default=2, metavar="MM", help="Margin between QR codes (in millimeters), default: 2")
    argparser.add_argument('--stride-x', type=float, default=0, metavar="MM", help="Horizontal distance between QR code tiles (in millimeters), default: 0")
    argparser.add_argument('--stride-y', type=float, default=0, metavar="MM", help="Vertical distance between QR code tiles (in millimeters), default: 0")
    argparser.add_argument('--prefix', type=str, default="", metavar="STR", help="Number prefix, default: empty")
    argparser.add_argument('--suffix', type=str, default="", metavar="STR", help="Number suffix, default: empty")
    argparser.add_argument('--digits', type=int, default=5, metavar="NUM", help="Number of digits, default: 5")
    argparser.add_argument('--start', type=int, default=0, metavar="NUM", help="Number to start with, default: 0")
    argparser.add_argument('--pages', type=int, default=1, metavar="NUM", help="Number of pages with QR codes to generate, default: 1")
    argparser.add_argument('--no-label', action="store_true", help="Skip label generation, default: to generate")
    argparser.add_argument('--font-size', type=float, default=5, metavar="NUM", help="Font size for label text, default: 5")
    argparser.add_argument('--label-spacing', type=float, default=0.4, metavar="MM", help="Vertical spacing between QR code and its label, default: 0.4")

    argparser.add_argument('-o', '--output', type=str, default="codes.pdf", metavar="PATH", help="Output path for generated PDF file, default: codes.pdf")

    args = argparser.parse_args()

    m = re.match(r"^([\d]+)x([\d]+)$", args.page_size)
    if m is not None:
        page_width_mm, page_height_mm = int(m.group(1)), int(m.group(2))
    else:
        predefined_size = getattr(pagesizes, args.page_size, None)
        if predefined_size is None:
            print(f"Unsupported page format: {args.page_size}")
            exit(1)
        page_width_mm, page_height_mm = predefined_size[0] / mm, predefined_size[1] / mm

        if args.landscape:
            page_width_mm, page_height_mm = page_height_mm, page_width_mm

    f = generate(
            page_width_mm=page_width_mm,
            page_height_mm=page_height_mm,
            base_size_mm=args.size,
            margin_mm=args.margin,
            stride_x_mm=args.stride_x,
            stride_y_mm=args.stride_y,
            prefix=args.prefix,
            suffix=args.suffix,
            digits=args.digits,
            start=args.start,
            pages=args.pages,
            generate_label=not args.no_label,
            label_spacing_mm=args.label_spacing,
            font_size=args.font_size,
    )

    with open(args.output, "wb") as fo:
        fo.write(f.read())

    print(f"PDF file saved to: {args.output}", file=sys.stderr)


main()
