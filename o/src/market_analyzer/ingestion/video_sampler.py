import argparse
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image


def sample_video(
    input_path: Path,
    output_dir: Path,
    interval_seconds: float = 10.0,
) -> list[Path]:
    """Save one PNG frame at each configured interval."""
    if interval_seconds <= 0:
        raise ValueError("interval_seconds must be greater than zero.")
    if not input_path.exists():
        raise FileNotFoundError("Video not found: {}".format(input_path))

    output_dir.mkdir(parents=True, exist_ok=True)
    frames: list[Path] = []
    reader = imageio_ffmpeg.read_frames(str(input_path), pix_fmt="rgb24")

    try:
        metadata = next(reader)
        fps = float(metadata["fps"])
        width, height = metadata["size"]
        if fps <= 0:
            raise ValueError("Video metadata contains an invalid frame rate.")

        interval_frames = max(1, round(fps * interval_seconds))
        next_frame = 0
        frame_number = 0

        for raw_frame in reader:
            if frame_number >= next_frame:
                frame = np.frombuffer(raw_frame, dtype=np.uint8)
                frame = frame.reshape((height, width, 3))
                timestamp = frame_number / fps
                output_path = output_dir / "frame_{:06.1f}s.png".format(timestamp)
                Image.fromarray(frame).save(output_path)
                frames.append(output_path)
                next_frame += interval_frames
            frame_number += 1
    finally:
        reader.close()

    return frames


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract frames from a market video at fixed intervals."
    )
    parser.add_argument("--input", type=Path, required=True, help="Input video path.")
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Directory where sampled PNGs will be saved.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=10.0,
        help="Sampling interval in seconds (default: 10).",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    frames = sample_video(args.input, args.output, args.interval)
    print("Saved {} frames to {}".format(len(frames), args.output))


if __name__ == "__main__":
    main()

