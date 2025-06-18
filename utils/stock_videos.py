from typing import List

from config import PEXELS_API_KEY
import logging
import requests

from utils.video import save_video

logger = logging.getLogger(__name__)


def get_stock_videos(search_terms: list[str]) -> list[str]:
    urls = [search_pexels(term) for term in search_terms]

    if len(urls) == 0:
        logger.error("No stock videos found")
        raise Exception("No stock videos found")

    return [save_video(url) for url in urls if url]


def search_pexels(query: str) -> str:
    if not PEXELS_API_KEY:
        logger.error("PEXELS_API_KEY not set")
        raise Exception("PEXELS_API_KEY not set")

    headers = {"Authorization": PEXELS_API_KEY}

    url = f"https://api.pexels.com/videos/search?query={query}&per_page=1"

    r = requests.get(url, headers=headers)

    response = r.json()

    try:
        video_urls = response["videos"][0]["video_files"]
    except:
        logger.error(f"Error getting stock videos: {response}")
        return ""
    video_url = ""

    for video in video_urls:
        if "https://" in video["link"]:
            video_url = video["link"]

    return video_url
