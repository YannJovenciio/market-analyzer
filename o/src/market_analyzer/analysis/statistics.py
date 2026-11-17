from statistics import mean, median

from market_analyzer.domain.models import MarketSample


def prices(samples: list[MarketSample]) -> list[int]:
    if not samples:
        raise ValueError("At least one sample is required.")
    return [sample.average_price for sample in samples]


def summary(samples: list[MarketSample]) -> dict[str, float | int]:
    values = prices(samples)
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": mean(values),
        "median": median(values),
    }

