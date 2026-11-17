from market_analyzer.domain.models import BacktestTrade, MarketSample


def run(
    samples: list[MarketSample],
    buy_below: int,
    sell_at: int,
    fee_rate: float = 0.0,
) -> tuple[list[BacktestTrade], MarketSample | None]:
    if buy_below >= sell_at:
        raise ValueError("buy_below must be lower than sell_at.")
    if not 0 <= fee_rate < 1:
        raise ValueError("fee_rate must be between 0 and 1.")

    position: MarketSample | None = None
    trades: list[BacktestTrade] = []
    for sample in sorted(samples, key=lambda value: value.timestamp):
        if position is None and sample.average_price <= buy_below:
            position = sample
        elif position is not None and sample.average_price >= sell_at:
            gross = sample.average_price - position.average_price
            fees = (position.average_price + sample.average_price) * fee_rate
            trades.append(BacktestTrade(position, sample, gross - fees))
            position = None
    return trades, position

