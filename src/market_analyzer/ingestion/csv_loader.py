import csv
from datetime import datetime
from pathlib import Path

from market_analyzer.domain.models import MarketSample


def load_samples(path: Path) -> list[MarketSample]:
    if not path.exists():
        raise FileNotFoundError("CSV not found: {}".format(path))

    samples: list[MarketSample] = []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"timestamp", "item", "preco_medio"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(
                "Missing CSV columns: {}".format(", ".join(sorted(missing)))
            )

        for line_number, row in enumerate(reader, start=2):
            try:
                price = int(row["preco_medio"])
                if price < 0:
                    raise ValueError("price cannot be negative")
                samples.append(
                    MarketSample(
                        timestamp=datetime.fromisoformat(row["timestamp"]),
                        item_id=row["item"],
                        average_price=price,
                        source=row.get("origem_video", ""),
                    )
                )
            except (TypeError, ValueError) as error:
                raise ValueError(
                    "Invalid CSV row {}: {}".format(line_number, error)
                ) from error

    if not samples:
        raise ValueError("CSV contains no samples.")
    return sorted(samples, key=lambda sample: sample.timestamp)

