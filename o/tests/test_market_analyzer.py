import csv
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from market_analyzer.analysis.statistics import summary
from market_analyzer.backtesting.simulator import run
from market_analyzer.domain.models import MarketSample
from market_analyzer.ingestion.csv_loader import load_samples


class MarketAnalyzerTests(unittest.TestCase):
    def setUp(self) -> None:
        start = datetime(2026, 1, 1)
        self.samples = [
            MarketSample(start, "item", 100),
            MarketSample(start + timedelta(seconds=10), "item", 200),
        ]

    def test_summary(self) -> None:
        result = summary(self.samples)
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["minimum"], 100)
        self.assertEqual(result["maximum"], 200)
        self.assertEqual(result["median"], 150)

    def test_backtest_closes_position(self) -> None:
        trades, position = run(self.samples, buy_below=120, sell_at=180)
        self.assertEqual(len(trades), 1)
        self.assertIsNone(position)
        self.assertEqual(trades[0].profit, 100)

    def test_backtest_applies_fees(self) -> None:
        trades, _ = run(self.samples, buy_below=120, sell_at=180, fee_rate=0.05)
        self.assertEqual(trades[0].profit, 85)

    def test_csv_loader_maps_current_schema(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "samples.csv"
            with path.open("w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["timestamp", "item", "preco_medio", "origem_video"],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "timestamp": "2026-01-01T00:00:00",
                        "item": "item",
                        "preco_medio": "100",
                        "origem_video": "sample.mp4",
                    }
                )

            samples = load_samples(path)

        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].item_id, "item")
        self.assertEqual(samples[0].average_price, 100)
        self.assertEqual(samples[0].source, "sample.mp4")


if __name__ == "__main__":
    unittest.main()
