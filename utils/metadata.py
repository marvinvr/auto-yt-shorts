import json
import os
from datetime import datetime
from pathlib import Path
from typing import List

from config import OUTPUT_PATH


def save_metadata(
    title: str,
    description: str,
    topic: str,
    script: str,
    search_terms: List[str],
    video_path: Path,
) -> None:
    metadata = {
        "title": title,
        "description": description,
        "topic": topic,
        "script": script,
        "search_terms": search_terms,
    }

    today = (datetime.now()).strftime("%Y-%m-%d")

    os.system(f"mkdir -p {str(OUTPUT_PATH / today)}")

    new_video_file = OUTPUT_PATH / f"{today}" / f"{title}.mp4"

    os.system(f'mv {str(video_path)} "{new_video_file}"')

    with open(OUTPUT_PATH / f"{today}" / f"{title}.json", "w") as f:
        json.dump(metadata, f)
