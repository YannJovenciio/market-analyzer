import argparse
import re
from pathlib import Path

from PIL import Image, ImageOps


PRICE_PATTERN = re.compile(r"\b\d{1,3}(?:[.,]\d{3})+\b|\b\d{6,9}\b")


def parse_price(text: str) -> int:
    """Parse a localized integer price such as 171.453 or 171,453."""
    normalized = text.replace(",", ".")
    normalized = re.sub(r"(?<=\d)\s+(?=\d)", "", normalized)
    match = PRICE_PATTERN.search(normalized)
    if match is None:
        raise ValueError("No price found in OCR text: {!r}".format(text))
    return int(match.group(0).replace(".", ""))


def prepare_price_region(
    image: Image.Image,
    left: int,
    top: int,
    right: int,
    bottom: int,
) -> Image.Image:
    if not 0 <= left < right <= image.width:
        raise ValueError("Invalid horizontal crop coordinates.")
    if not 0 <= top < bottom <= image.height:
        raise ValueError("Invalid vertical crop coordinates.")

    region = image.crop((left, top, right, bottom)).convert("L")
    region = region.resize((region.width * 3, region.height * 3))
    region = ImageOps.autocontrast(region)
    return region.point(lambda pixel: 255 if pixel > 110 else 0)


def read_price(
    image_path: Path,
    region: tuple[int, int, int, int],
) -> int:
    try:
        import pytesseract
    except ImportError as error:
        raise RuntimeError(
            "pytesseract is not installed. Run: python -m pip install -e ."
        ) from error

    try:
        image = Image.open(image_path)
        prepared = prepare_price_region(image, *region)
        text = pytesseract.image_to_string(
            prepared,
            config="--psm 7 -c tessedit_char_whitelist=0123456789.,",
        )
    except pytesseract.TesseractNotFoundError as error:
        raise RuntimeError(
            "Tesseract OCR executable was not found. Install Tesseract and "
            "configure its executable in PATH."
        ) from error
    return parse_price(text)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read a price from a sampled frame.")
    parser.add_argument("--input", type=Path, required=True, help="PNG frame path.")
    parser.add_argument(
        "--region",
        nargs=4,
        type=int,
        metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"),
        default=(1410, 755, 1545, 805),
        help="Price crop coordinates in pixels.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    print(read_price(args.input, tuple(args.region)))


if __name__ == "__main__":
    main()
