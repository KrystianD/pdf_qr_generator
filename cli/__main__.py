import argparse
import sys

from lib.generator import generate


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--size', type=float, default=10, metavar="MM", help="Base QR code size (in millimeters), default: 10")
    argparser.add_argument('--margin', type=float, default=2, metavar="MM", help="Margin between QR codes (in millimeters), default: 2")
    argparser.add_argument('--prefix', type=str, default="", metavar="STR", help="Number prefix, default: empty")
    argparser.add_argument('--suffix', type=str, default="", metavar="STR", help="Number suffix, default: empty")
    argparser.add_argument('--digits', type=int, default=5, metavar="NUM", help="Number of digits, default: 5")
    argparser.add_argument('--start', type=int, default=0, metavar="NUM", help="Number to start with, default: 0")
    argparser.add_argument('--no-label', action="store_true", help="Skip label generation, default: to generate")
    argparser.add_argument('--font-size', type=float, default=5, metavar="NUM", help="Font size for label text, default: 5")
    argparser.add_argument('--label-spacing', type=float, default=0.4, metavar="MM", help="Vertical spacing between QR code and its label, default: 0.4")

    argparser.add_argument('-o', '--output', type=str, default="codes.pdf", metavar="PATH", help="Output path for generated PDF file, default: codes.pdf")

    args = argparser.parse_args()

    f = generate(
            base_size_mm=args.size,
            margin_mm=args.margin,
            prefix=args.prefix,
            suffix=args.suffix,
            digits=args.digits,
            start=args.start,
            generate_label=not args.no_label,
            label_spacing_mm=args.label_spacing,
            font_size=args.font_size,
    )

    with open(args.output, "wb") as fo:
        fo.write(f.read())

    print(f"PDF file saved to: {args.output}", file=sys.stderr)


main()
