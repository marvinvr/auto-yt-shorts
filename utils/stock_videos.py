from typing import List

from config import PEXELS_API_KEY
import requests

from utils.video import save_video


def get_stock_videos(search_terms: List[str]) -> List[str]:
    urls = [search_pexels(term) for term in search_terms]
    
    return [save_video(url) for url in urls if url]
    
def search_pexels(query: str) -> str:
    headers = {
        "Authorization": PEXELS_API_KEY
    }

    url = f"https://api.pexels.com/videos/search?query={query}&per_page=1"

    r = requests.get(url, headers=headers)

    response = r.json()

    try:
        video_urls = response["videos"][0]["video_files"]
    except:
        return ""
    video_url = ""

    for video in video_urls:
        if ".com/external" in video["link"]:
            video_url = video["link"]

    return video_url
    