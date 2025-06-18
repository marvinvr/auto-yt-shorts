import base64
import json
import mimetypes
import random
import requests
import struct
import uuid
from pathlib import Path

from config import BACKGROUND_SONGS_PATH, GEMINI_API_KEY, GEMINI_TTS_MODEL, TEMP_PATH


def save_binary_file(file_path: Path, data: bytes):
    """Save binary data to a file."""
    with open(file_path, "wb") as f:
        f.write(data)


def convert_to_wav(audio_data: bytes, mime_type: str, speed: float = 1.1) -> bytes:
    """Converts audio data to WAV format with proper header and adjusts playback speed.

    Args:
        audio_data: The raw audio data as a bytes object.
        mime_type: Mime type of the audio data.
        speed: Speed multiplier for playback (e.g., 1.1 for 1.1x speed).

    Returns:
        A bytes object representing the WAV file.
    """
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    original_sample_rate = parameters["rate"]
    # Adjust sample rate to change playback speed
    sample_rate = int(original_sample_rate * speed)
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",  # ChunkID
        chunk_size,  # ChunkSize
        b"WAVE",  # Format
        b"fmt ",  # Subchunk1ID
        16,  # Subchunk1Size
        1,  # AudioFormat (PCM)
        num_channels,  # NumChannels
        sample_rate,  # SampleRate
        byte_rate,  # ByteRate
        block_align,  # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",  # Subchunk2ID
        data_size,  # Subchunk2Size
    )
    return header + audio_data


def parse_audio_mime_type(mime_type: str) -> dict[str, int]:
    """Parse bits per sample and rate from an audio MIME type string.

    Args:
        mime_type: The audio MIME type string (e.g., "audio/L16;rate=24000").

    Returns:
        A dictionary with "bits_per_sample" and "rate" keys.
    """
    bits_per_sample = 16
    rate = 24000

    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass

    return {"bits_per_sample": bits_per_sample, "rate": rate}


def generate_voiceover(text: str) -> Path:
    """Generate voiceover audio using Google Gemini TTS REST API.

    Args:
        text: The text to convert to speech.

    Returns:
        Path to the generated audio file.
    """
    audio_id = uuid.uuid4()
    audio_path = TEMP_PATH / f"{audio_id}.wav"

    # Prepare the REST API request
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_TTS_MODEL}:generateContent"

    headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}

    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "temperature": 0.8,
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Fenrir"}}
            },
        },
    }

    try:
        # Make the API request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        response_data = response.json()

        # Extract the audio data from the response
        if (
            "candidates" in response_data
            and response_data["candidates"]
            and "content" in response_data["candidates"][0]
            and "parts" in response_data["candidates"][0]["content"]
            and response_data["candidates"][0]["content"]["parts"]
        ):
            part = response_data["candidates"][0]["content"]["parts"][0]

            if "inlineData" in part and "data" in part["inlineData"]:
                # Decode the base64 audio data
                audio_data = base64.b64decode(part["inlineData"]["data"])
                mime_type = part["inlineData"].get("mimeType", "audio/wav")

                # Convert to WAV if needed
                file_extension = mimetypes.guess_extension(mime_type)
                if file_extension is None or file_extension != ".wav":
                    audio_data = convert_to_wav(audio_data, mime_type)

                save_binary_file(audio_path, audio_data)
            else:
                raise Exception("No audio data found in API response")
        else:
            raise Exception("Invalid response structure from Gemini TTS API")

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse API response: {e}")
    except Exception as e:
        raise Exception(f"TTS generation failed: {e}")

    return audio_path


def get_random_background_song() -> Path:
    songs = list(BACKGROUND_SONGS_PATH.glob("*.mp3"))
    return random.choice(songs)
