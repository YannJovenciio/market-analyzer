import unittest

from market_analyzer.ingestion.price_ocr import parse_price


class PriceOcrTests(unittest.TestCase):
    def test_parses_dot_separator(self) -> None:
        self.assertEqual(parse_price("Preço 171.453"), 171453)

    def test_parses_comma_separator(self) -> None:
        self.assertEqual(parse_price("171,453"), 171453)

    def test_parses_price_without_separator(self) -> None:
        self.assertEqual(parse_price("171453"), 171453)

    def test_rejects_text_without_price(self) -> None:
        with self.assertRaises(ValueError):
            parse_price("sem valor")


if __name__ == "__main__":
    unittest.main()
