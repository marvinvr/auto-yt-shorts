import os
from datetime import datetime
from pathlib import Path


def upload_yt(
    file: str,
    metadata_path: str,
) -> str:

    #    res = YouTubeUploader(file, metadata_path).upload()
    ...


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
        os.system(f'cp {str(file)} "{new_video_file}"')

        # create a txt file with the description
        with open(new_video_file.with_suffix(".txt"), "w") as f:
            f.write(description)

        print("[Prepped for Manual Upload]")
        print(new_video_file)
        print(new_video_file.with_suffix(".txt"))
