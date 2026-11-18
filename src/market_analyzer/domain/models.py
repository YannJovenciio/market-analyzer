from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MarketSample:
    """A single observed market state."""

    timestamp: datetime
    item_id: str
    average_price: int
    source: str = ""
    quantity: int | None = None


@dataclass(frozen=True)
class BacktestTrade:
    """A simulated buy and sell pair."""

    purchase: MarketSample
    sale: MarketSample
    profit: float

