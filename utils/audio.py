import os
import random
import uuid
from pathlib import Path

from openai import OpenAI

from config import BACKGROUND_SONGS_PATH, OPENAI_API_KEY, TEMP_PATH

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_voiceover(text: str) -> Path:
    audio_id = uuid.uuid4()
    audio_path = TEMP_PATH / f"{audio_id}.mp3"

    response = client.audio.speech.create(
        model="tts-1", voice="echo", input=text, speed=1
    )

    response.stream_to_file(audio_path)

    return audio_path


def get_random_background_song() -> Path:
    songs = list(BACKGROUND_SONGS_PATH.glob("*.mp3"))
    return random.choice(songs)
