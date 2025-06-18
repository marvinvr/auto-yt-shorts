import os
import shlex
from datetime import datetime
from pathlib import Path

from config import NO_UPLOAD


def auto_upload(
    video: Path,
    title: str,
    description: str,
    privacy: str = "public",
    category: str = "24",
) -> None:
    if NO_UPLOAD:
        return

    os.system(
        f"/venv/bin/python3 upload_video.py --file={shlex.quote(str(video))} --title={shlex.quote(title)} --description={shlex.quote(description)} --privacyStatus={shlex.quote(privacy)} --category={shlex.quote(category)}"
    )


def prep_for_manual_upload(
    file: Path,
    title: str,
    description: str,
) -> None:

    os.system("mkdir -p youtube")

    # create a folder with today's date
    today = (datetime.now()).strftime("%Y-%m-%d")

    os.system(f"mkdir -p youtube/{today}")

    # copy video file into youtube and name it title
    new_video_file = Path("youtube") / f"{today}" / f"{title}.mp4"
    if not new_video_file.exists():
        # copy it
        os.system(f"cp {shlex.quote(str(file))} {shlex.quote(str(new_video_file))}")

        # create a txt file with the description
        with open(new_video_file.with_suffix(".txt"), "w") as f:
            f.write(description)

        print("[Prepped for Manual Upload]")
        print({new_video_file})
        print({new_video_file.with_suffix(".txt")})
