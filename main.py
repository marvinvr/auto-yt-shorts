import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from tqdm import tqdm

from config import CRON_SCHEDULE, RUN_ONCE, VIDEO_COUNT
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
from utils.notifications import send_error_notification, send_success_notification
from utils.stock_videos import get_stock_videos
from utils.video import generate_subtitles, generate_video
from utils.yt import auto_upload

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

    return title, description, script, search_terms, stock_videos, voiceover, subtitles


def generate_videos(n: int = 4) -> None:
    try:
        topic = get_topic()

        logger.info("[Generated Topic]")
        logger.info(topic)

        possible_titles = get_titles(topic)
        logger.info("[Generated Possible Titles]")
        logger.info(possible_titles)

        titles = get_most_engaging_titles(possible_titles, n)

        videos_generated = 0
        for title in tqdm(titles, desc="Generating videos"):
            try:
                (
                    title,
                    description,
                    script,
                    search_terms,
                    stock_videos,
                    voiceover,
                    subtitles,
                ) = generate_video_data(title)

                logging.debug(f"Title: {title}")
                logging.debug(f"Description: {description}")
                logging.debug(f"Script: {script}")
                logging.debug(f"Search terms: {search_terms}")
                logging.debug(f"Stock videos: {stock_videos}")
                logging.debug(f"Voiceover: {voiceover}")
                logging.debug(f"Subtitles: {subtitles}")

                video = generate_video(stock_videos, voiceover, subtitles)
                logger.info("[Generated Video]")

                new_video_file = save_metadata(
                    title, description, None, script, search_terms, video
                )
                logger.info("[Saved Video]")

                auto_upload(new_video_file, title, description)
                logger.info("[Uploaded Video]")
                videos_generated += 1

            except Exception as e:
                error_msg = f"Failed to generate/upload video '{title}'"
                logger.error(f"{error_msg}: {e}")
                send_error_notification(error_msg, e, "Video Generation")

        if videos_generated > 0:
            success_msg = (
                f"Successfully generated and uploaded {videos_generated} video(s)"
            )
            logger.info(success_msg)
            send_success_notification(success_msg, "Video Generation")
        else:
            error_msg = "No videos were successfully generated"
            logger.error(error_msg)
            send_error_notification(error_msg, context="Video Generation")

    except Exception as e:
        error_msg = "Failed to start video generation process"
        logger.error(f"{error_msg}: {e}")
        send_error_notification(error_msg, e, "Video Generation")


def main():
    cron_schedule = CRON_SCHEDULE
    run_once = RUN_ONCE
    video_count = VIDEO_COUNT

    if run_once:
        logger.info("RUN_ONCE is enabled, generating videos immediately...")
        generate_videos(video_count)
        logger.info("Video generation completed. Exiting.")
        return

    logger.info(f"Starting scheduler with cron schedule: {cron_schedule}")
    scheduler = BlockingScheduler()

    trigger = CronTrigger.from_crontab(cron_schedule)
    scheduler.add_job(
        func=generate_videos, trigger=trigger, args=[video_count], id="video_generation"
    )

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
        scheduler.shutdown()
    except Exception as e:
        error_msg = "Scheduler failed unexpectedly"
        logger.error(f"{error_msg}: {e}")
        send_error_notification(error_msg, e, "Scheduler")


if __name__ == "__main__":
    main()
