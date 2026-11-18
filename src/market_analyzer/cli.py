import argparse
from pathlib import Path

from market_analyzer.analysis.statistics import summary
from market_analyzer.backtesting.simulator import run
from market_analyzer.ingestion.csv_loader import load_samples


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="market-analyzer",
        description="Market analysis and backtesting toolkit.",
    )
    parser.add_argument("--version", action="version", version="0.1.0")
    parser.add_argument("--input", type=Path, required=True, help="Input CSV path.")
    parser.add_argument(
        "--buy-below",
        type=int,
        default=130000,
        help="Simulate a purchase at or below this price.",
    )
    parser.add_argument(
        "--sell-at",
        type=int,
        default=190000,
        help="Simulate a sale at or above this price.",
    )
    parser.add_argument(
        "--fee-rate",
        type=float,
        default=0.0,
        help="Fee per operation as a fraction; e.g. 0.05 for 5%%.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    samples = load_samples(args.input)
    stats = summary(samples)
    trades, open_position = run(
        samples,
        buy_below=args.buy_below,
        sell_at=args.sell_at,
        fee_rate=args.fee_rate,
    )

    print("Item: {}".format(samples[0].item_id))
    print("Samples: {}".format(stats["count"]))
    print("Minimum: {}".format(stats["minimum"]))
    print("Maximum: {}".format(stats["maximum"]))
    print("Mean: {:.2f}".format(stats["mean"]))
    print("Median: {:.2f}".format(stats["median"]))
    print("Simulated trades: {}".format(len(trades)))
    print("Simulated profit: {:.2f}".format(sum(trade.profit for trade in trades)))
    if open_position is not None:
        print("Open position: {}".format(open_position.average_price))


if __name__ == "__main__":
    main()

