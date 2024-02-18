import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count

import uvicorn
from fastapi import FastAPI
from tqdm import tqdm

from utils.audio import generate_voiceover
from utils.llm import (
    get_description,
    get_most_engaging_titles,
    get_script,
    get_search_terms,
    get_titles,
    get_topic,
)
from utils.metadata import save_metadata
from utils.stock_videos import get_stock_videos
from utils.video import generate_subtitles, generate_video
from utils.yt import prep_for_manual_upload

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_video_data(title):
    logger.info("[Generated Title]")
    logger.info(title)

    script = get_script(title)
    logger.info("[Generated Script]")
    logger.info(script)

    description = get_description(title, script)
    logger.info("[Generated Description]")
    logger.info(description)

    search_terms = get_search_terms(title, script)
    logger.info("[Generated Search Terms]")
    logger.info(search_terms)

    stock_videos = get_stock_videos(search_terms)
    logger.info("[Generated Stock Videos]")

    voiceover = generate_voiceover(script)
    logger.info("[Generated Voiceover]")

    subtitles = generate_subtitles(voiceover)
    logger.info("[Generated Subtitles]")

    video = generate_video(stock_videos, voiceover, subtitles)
    logger.info("[Generated Video]")

    return title, description, script, search_terms, video


@app.post("/generate_videos/")
def generate_videos(n: int = 4) -> None:
    topic = get_topic()

    logger.info("[Generated Topic]")
    logger.info(topic)

    possible_titles = get_titles(topic)
    logger.info("[Generated Possible Titles]")
    logger.info(possible_titles)

    titles = get_most_engaging_titles(possible_titles, n)

    # Use ThreadPoolExecutor to execute the network-bound tasks in parallel
    with ThreadPoolExecutor(max_workers=min(cpu_count(), len(titles))) as executor:
        # Submit all tasks to the executor
        future_to_title = {
            executor.submit(generate_video_data, title): title for title in titles
        }

        for future in tqdm(as_completed(future_to_title), total=len(titles)):
            title, description, script, search_terms, video = future.result()

            save_metadata(title, description, None, script, search_terms, video)
            logger.info("[Saved Video]")

            # upload_tiktok(video, description)
            # upload_yt(video, title, description)

            prep_for_manual_upload(video, title, description)
            logger.info("[Uploaded Video]")


@app.get("/health/")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
