import os
from pathlib import Path

import dotenv

dotenv.load_dotenv()

POSSIBLE_TOPICS = [
    # "NASA Facts",
    "Controversial Events",
    # "Bold Predictions",
    "Controversial Actions by Celebrities",
    "Controversial Actions by Well Known Companies",
]


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY_AUTO_YT_SHORTS")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY_AUTO_YT_SHORTS not set")


OPENAI_MODEL = "gpt-4-turbo-preview"  # "gpt-3.5-turbo-0125"

MIN_SEARCH_TERMS = 3
MAX_SEARCH_TERMS = 5

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

ASSEMBLY_AI_API_KEY = os.environ.get("ASSEMBLY_AI_API_KEY")

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

TEMP_PATH = Path("temp")

os.makedirs(TEMP_PATH, exist_ok=True)

OUTPUT_PATH = Path("output")

os.makedirs(OUTPUT_PATH, exist_ok=True)

BACKGROUND_SONGS_PATH = Path("music")

SECONDARY_CONTENT_PATH = Path("secondary_video")
