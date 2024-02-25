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
  "Science Facts",
  "Historical Mysteries Solved",
  "Tech Milestones",
  "Cultural Oddities",
  "Animal Superpowers",
  "Psychological Phenomena",
  "Extreme Weather Events",
  "Unsung Heroes of History",
  "Futuristic Technologies in Development",
  "Mythical Places and Their Real Inspirations",
  "Space Exploration Milestones",
  "Microscopic Worlds",
  "Cryptocurrency and Blockchain",
  "The Science of Happiness",
  "Bizarre Laws from Around the World",
  "Hidden Gems of the Planet",
  "Secrets of Successful People",
  "Eco-Friendly Innovations",
  "Mysteries of the Deep Sea",
  "World Records and the Stories Behind Them"
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
