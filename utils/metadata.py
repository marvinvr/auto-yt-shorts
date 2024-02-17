import json
from pathlib import Path
from typing import List

from config import OUTPUT_PATH


def save_metadata(title: str, description: str, topic: str, script: str, search_terms: List[str], video_path: Path) -> None:
    metadata = {
        "title": title,
        "description": description,
        "topic": topic,
        "script": script,
        "search_terms": search_terms
    }
    
    video_id = video_path.stem
    
    with open(OUTPUT_PATH / f"{video_id}.json", "w") as f:
        json.dump(metadata, f)