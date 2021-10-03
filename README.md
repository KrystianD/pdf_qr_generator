PDF QR codes generator
=====

A utility for generating PDFs filled with QR codes. Highly customizable.

QR code content includes version number and CRC8/CCITT checksum. For example `V1.00051.31`, `00051` is a QR code content and `31` is CRC8 checksum of the QR code content in hex format.

Each tile consists of QR code and an (optional) label.

# Requirements

```sh
pip install -r requirements.txt
```

# Usage

## Basic

Generate `codes.pdf` file with the default settings.

```sh
python -m cli
```

## Advanced

```
usage: python -m cli [-h] [--page-size SIZE] [--landscape] [--size MM] [--margin MM] [--stride-x MM] [--stride-y MM] [--prefix STR] [--suffix STR] [--digits NUM] [--start NUM] [--no-label] [--font-size NUM]
                     [--label-spacing MM] [-o PATH]

optional arguments:
  -h, --help            show this help message and exit
  --page-size SIZE      Page size. Possible values are predefined page format (A4, A5, etc) or dimensions millimeters (20x30), default: A4
  --landscape           Landscape orientation. For predefined formats only, default: portrait
  --size MM             Base QR code size (in millimeters), default: 10
  --margin MM           Margin between QR codes (in millimeters), default: 2
  --stride-x MM         Horizontal distance between QR code tiles (in millimeters), default: 0
  --stride-y MM         Vertical distance between QR code tiles (in millimeters), default: 0
  --prefix STR          Number prefix, default: empty
  --suffix STR          Number suffix, default: empty
  --digits NUM          Number of digits, default: 5
  --start NUM           Number to start with, default: 0
  --no-label            Skip label generation, default: to generate
  --font-size NUM       Font size for label text, default: 5
  --label-spacing MM    Vertical spacing between QR code and its label, default: 0.4
  -o PATH, --output PATH
                        Output path for generated PDF file, default: codes.pdf
```
