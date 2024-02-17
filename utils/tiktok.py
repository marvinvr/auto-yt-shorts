from tiktok_uploader.auth import AuthBackend
from tiktok_uploader.upload import upload_video, upload_videos


def upload_tiktok(video_path: str, caption: str) -> str:

    upload_video(
        str(video_path), caption, "cookies.txt", browser="firefox", headless=False
    )
