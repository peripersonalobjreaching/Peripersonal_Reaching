#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Union

VIDEO_DIR = re.compile(r"^image_(\d+)$")
FRAME_FILE = re.compile(r"^(\d+)\.json$")


ALIASES = {
    "question": "Question",
    "scene_description": "Scene Description",
    "chain_of_landmark": "Chain-of-landmark",
    "is_target_in_frame": "Is target in frame",
    "head_movement": "Head movement",
    "is_hand_in_frame": "Is hand in frame",
    "hand_movement": "Hand movement",
    "risk_items": "Risk Items",
    "risk_direction": "Risk direction",
    "reaching_target": "Reaching Target",
    "phase": "Phase",
}


@dataclass(frozen=True)
class Frame:
    """One annotated frame: the parsed JSON, plus where it came from."""

    video_id: str
    frame_index: int
    path: Path
    raw: Dict[str, Any]

    def __getattr__(self, name: str) -> Any:
        if name in ALIASES:
            return self.raw.get(ALIASES[name])
        raise AttributeError(
            f"{name!r} is not an annotation field. Expected one of: "
            f"{', '.join(sorted(ALIASES))} — or use frame.raw[...] directly."
        )


@dataclass
class Video:
    """One source video's frames, in numeric frame-index order."""

    video_id: str
    frames: List[Frame] = field(default_factory=list)

    def __iter__(self) -> Iterator[Frame]:
        return iter(self.frames)

    def __len__(self) -> int:
        return len(self.frames)


@dataclass
class Dataset:
    root: Path
    videos: List[Video] = field(default_factory=list)
    skipped: List[str] = field(default_factory=list)

    @property
    def frames(self) -> List[Frame]:
        return [frame for video in self.videos for frame in video.frames]


def load_dataset(root: Union[str, Path]) -> Dataset:
    """Read every annotation under *root*, the directory holding `image_*/`."""
    root = Path(root)
    if not root.is_dir():
        raise NotADirectoryError(f"no such annotation root: {root}")

    videos: List[Video] = []
    skipped: List[str] = []
    directories = [path for path in root.iterdir() if path.is_dir()]


    def video_number(path: Path) -> int:
        match = VIDEO_DIR.match(path.name)
        return int(match.group(1)) if match else -1

    for directory in sorted(directories, key=lambda p: (video_number(p), p.name)):
        if not VIDEO_DIR.match(directory.name):
            skipped.append(directory.name)
            continue

        frames: List[Frame] = []
        for path in directory.iterdir():
            match = FRAME_FILE.match(path.name)
            if not match:
                continue  # the .mp4 and the preview .jpg
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}: {exc}") from None
            frames.append(Frame(directory.name, int(match.group(1)), path, raw))

        frames.sort(key=lambda frame: frame.frame_index)
        videos.append(Video(directory.name, frames))

    return Dataset(root, videos, skipped)


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "data/annotations"
    dataset = load_dataset(target)
    print(f"{len(dataset.videos)} videos, {len(dataset.frames)} frames")
    