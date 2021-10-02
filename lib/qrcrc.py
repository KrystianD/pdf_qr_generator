from crc import CrcCalculator, Crc8


def calc_crc(code):
    crc_calculator = CrcCalculator(Crc8.CCITT)

    txt = code
    crc = crc_calculator.calculate_checksum(txt.encode("ascii"))

    return f"{crc:02X}"


__all__ = [
    "calc_crc",
]
