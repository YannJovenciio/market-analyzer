import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from market_analyzer.ingestion.video_sampler import sample_video


class VideoSamplerTests(unittest.TestCase):
    def test_rejects_non_positive_interval(self) -> None:
        with TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                sample_video(
                    Path(directory) / "missing.mp4",
                    Path(directory) / "frames",
                    interval_seconds=0,
                )

    def test_rejects_missing_video(self) -> None:
        with TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                sample_video(
                    Path(directory) / "missing.mp4",
                    Path(directory) / "frames",
                )


if __name__ == "__main__":
    unittest.main()
