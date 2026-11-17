import argparse
import csv
import re
from datetime import datetime, timedelta
from pathlib import Path

from market_analyzer.ingestion.price_ocr import read_price


FRAME_TIMESTAMP = re.compile(r"frame_(\d+(?:\.\d+)?)s\.png$")


def frame_seconds(path: Path) -> float:
    match = FRAME_TIMESTAMP.match(path.name)
    if match is None:
        raise ValueError("Invalid sampled frame name: {}".format(path.name))
    return float(match.group(1))


def process_frames(
    frames_dir: Path,
    output_path: Path,
    item: str,
    source: str,
    recorded_at: datetime,
    region: tuple[int, int, int, int],
) -> int:
    frames = sorted(frames_dir.glob("frame_*.png"), key=frame_seconds)
    if not frames:
        raise FileNotFoundError("No sampled frames found in {}".format(frames_dir))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["timestamp", "item", "preco_medio", "origem_video", "observacao"],
        )
        writer.writeheader()
        for frame in frames:
            seconds = frame_seconds(frame)
            timestamp = recorded_at + timedelta(seconds=seconds)
            try:
                price = read_price(frame, region)
            except (RuntimeError, ValueError) as error:
                raise RuntimeError(
                    "OCR failed for {}: {}".format(frame.name, error)
                ) from error
            writer.writerow(
                {
                    "timestamp": timestamp.isoformat(timespec="seconds"),
                    "item": item,
                    "preco_medio": price,
                    "origem_video": source,
                    "observacao": "OCR sample at {:.1f}s".format(seconds),
                }
            )
    return len(frames)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert sampled market frames into a CSV."
    )
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--item", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument(
        "--recorded-at",
        type=datetime.fromisoformat,
        required=True,
        help="Recording start time in ISO format.",
    )
    parser.add_argument(
        "--region",
        nargs=4,
        type=int,
        metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"),
        default=(1410, 755, 1545, 805),
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    count = process_frames(
        args.input_dir,
        args.output,
        args.item,
        args.source,
        args.recorded_at,
        tuple(args.region),
    )
    print("Wrote {} OCR samples to {}".format(count, args.output))


if __name__ == "__main__":
    main()

