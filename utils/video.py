import os
import random
import uuid
from pathlib import Path
from typing import List

import assemblyai as aai
import requests
import srt_equalizer
from moviepy.audio.fx.all import volumex
from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    TextClip,
    VideoFileClip,
    concatenate_videoclips,
)
from moviepy.video.fx.all import crop
from moviepy.video.tools.subtitles import SubtitlesClip

from config import ASSEMBLY_AI_API_KEY, OUTPUT_PATH, SECONDARY_CONTENT_PATH, TEMP_PATH
from utils.audio import get_random_background_song


def generate_word_timestamps(audio_path: Path) -> List[dict]:
    """Generate word-level timestamps using AssemblyAI"""
    aai.settings.api_key = ASSEMBLY_AI_API_KEY

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(str(audio_path))

    # Extract word-level timestamps
    words = []
    if transcript.words:
        for word in transcript.words:
            words.append({
                'text': word.text,
                'start': word.start / 1000.0,  # Convert from ms to seconds
                'end': word.end / 1000.0,      # Convert from ms to seconds
                'confidence': getattr(word, 'confidence', 1.0)
            })
    
    return words


def generate_subtitles(audio_path: Path) -> Path:
    """Legacy function for backward compatibility"""
    def equalize_subtitles(srt_path: str, max_chars: int = 10) -> None:
        srt_equalizer.equalize_srt_file(srt_path, srt_path, max_chars)

    aai.settings.api_key = ASSEMBLY_AI_API_KEY

    subtitles_id = uuid.uuid4()

    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(str(audio_path))

    # Save subtitles
    subtitles_path = TEMP_PATH / f"{subtitles_id}.srt"

    subtitles = transcript.export_subtitles_srt()

    with open(subtitles_path, "w") as f:
        f.write(subtitles)

    # Equalize subtitles
    equalize_subtitles(subtitles_path)

    return subtitles_path


def combine_videos(video_paths: List[Path], max_duration: int) -> Path:
    video_id = uuid.uuid4()
    combined_video_path = TEMP_PATH / f"{video_id}.mp4"

    clips = []
    for video_path in video_paths:
        clip = VideoFileClip(str(video_path))
        clip = clip.without_audio()
        # chain the clip to itself as many times as needed to be over max_duration / len(video_paths)
        clip = concatenate_videoclips([clip] * int(max_duration / len(video_paths)))

        clip = clip.subclip(0, max_duration / len(video_paths))
        clip = clip.set_fps(30)

        # Not all videos are same size,
        # so we need to resize them
        clip = crop(
            clip,
            width=int(clip.h / 1920 * 1080),
            height=clip.h,
            x_center=clip.w / 2,
            y_center=clip.h / 2,
        )
        clip = clip.resize((1080, 1920))

        clips.append(clip)

    final_clip = concatenate_videoclips(clips)
    final_clip = final_clip.set_fps(30)
    final_clip.write_videofile(
        str(combined_video_path),
        threads=os.cpu_count(),
        temp_audiofile=str(TEMP_PATH / f"{video_id}.mp3"),
    )

    return combined_video_path


def create_karaoke_subtitles(words: List[dict], video_duration: float) -> List[TextClip]:
    """Create karaoke-style word-by-word subtitle clips with highlighting"""
    subtitle_clips = []
    
    for word_idx, word in enumerate(words):
        # Find when the next word starts (or video ends)
        next_word_start = words[word_idx + 1]['start'] if word_idx + 1 < len(words) else video_duration
        
        # Create highlighted word clip that disappears when next word starts
        highlighted_clip = TextClip(
            word['text'],
            font="fonts/bold_font.ttf",
            fontsize=118,
            color="#FFFF00",  # Bright yellow
            stroke_color="black",
            stroke_width=6,
        ).set_start(word['start']).set_end(min(next_word_start, word['end'] + 0.3)).set_pos(("center", "center"))
        
        subtitle_clips.append(highlighted_clip)
    
    return subtitle_clips


def generate_video_with_karaoke(
    video_paths: List[Path], tts_path: Path
) -> Path:
    """Generate video with karaoke-style word-by-word subtitles"""
    audio = AudioFileClip(str(tts_path))

    combined_video_path = combine_videos(video_paths, audio.duration)

    # Generate word-level timestamps
    words = generate_word_timestamps(tts_path)
    
    # Create karaoke subtitle clips
    subtitle_clips = create_karaoke_subtitles(words, audio.duration)

    # Combine video with karaoke subtitles
    video_clips = [VideoFileClip(str(combined_video_path))]
    video_clips.extend(subtitle_clips)
    
    result = CompositeVideoClip(video_clips)

    # Add the audio
    audio = AudioFileClip(str(tts_path))
    music = AudioFileClip(str(get_random_background_song()))

    music = music.set_duration(audio.duration)

    audio = CompositeAudioClip([audio, volumex(music, 0.07)])

    result = result.set_audio(audio)

    secondary_video = get_secondary_video_clip(result.duration)

    secondary_video = secondary_video.resize(
        (result.w, int(secondary_video.h / secondary_video.w * result.w))
    )

    secondary_video_position = ("center", result.h - secondary_video.h - 160)

    result = CompositeVideoClip(
        [result, secondary_video.set_pos(secondary_video_position)]
    )

    video_id = uuid.uuid4()

    output_video_path = OUTPUT_PATH / f"{video_id}.mp4"

    result.write_videofile(
        str(output_video_path),
        threads=os.cpu_count(),
        temp_audiofile=str(TEMP_PATH / f"{video_id}.mp3"),
    )

    return output_video_path


def generate_video(
    video_paths: List[Path], tts_path: Path, subtitles_path: Path = None
) -> Path:
    """Legacy function - now uses karaoke subtitles by default"""
    # Use new karaoke approach
    return generate_video_with_karaoke(video_paths, tts_path)


def generate_video_legacy(
    video_paths: List[Path], tts_path: Path, subtitles_path: Path
) -> Path:
    """Original implementation kept for fallback"""
    audio = AudioFileClip(str(tts_path))

    combined_video_path = combine_videos(video_paths, audio.duration)

    generator = lambda txt: TextClip(
        txt,
        font=f"fonts/bold_font.ttf",
        fontsize=112,
        color="#FFFFFF",
        stroke_color="black",
        stroke_width=5,
    )

    # Burn the subtitles into the video
    subtitles = SubtitlesClip(str(subtitles_path), generator)
    result = CompositeVideoClip(
        [
            VideoFileClip(str(combined_video_path)),
            subtitles.set_pos(("center", "center")),
        ]
    )

    # Add the audio
    audio = AudioFileClip(str(tts_path))
    music = AudioFileClip(str(get_random_background_song()))

    music = music.set_duration(audio.duration)

    audio = CompositeAudioClip([audio, volumex(music, 0.07)])

    result = result.set_audio(audio)

    secondary_video = get_secondary_video_clip(result.duration)

    secondary_video = secondary_video.resize(
        (result.w, int(secondary_video.h / secondary_video.w * result.w))
    )

    secondary_video_position = ("center", result.h - secondary_video.h - 160)

    result = CompositeVideoClip(
        [result, secondary_video.set_pos(secondary_video_position)]
    )

    video_id = uuid.uuid4()

    output_video_path = OUTPUT_PATH / f"{video_id}.mp4"

    result.write_videofile(
        str(output_video_path),
        threads=os.cpu_count(),
        temp_audiofile=str(TEMP_PATH / f"{video_id}.mp3"),
    )

    return output_video_path


def save_video(video_url: str) -> str:
    video_id = uuid.uuid4()
    video_path = TEMP_PATH / f"{video_id}.mp4"

    with open(video_path, "wb") as f:
        f.write(requests.get(video_url).content)

    return video_path


def get_secondary_video_clip(duration) -> VideoFileClip:
    secondary_videos = list(SECONDARY_CONTENT_PATH.glob("*.mp4"))

    video_path = random.choice(secondary_videos)

    video = VideoFileClip(str(video_path)).without_audio()

    start_time = random.uniform(0, video.duration - duration)

    clip = video.subclip(start_time, start_time + duration)

    clip = clip.set_fps(30)

    return clip
