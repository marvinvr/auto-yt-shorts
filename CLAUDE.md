# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Installation and Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp example.env .env
# Edit .env with your API keys and credentials

# Initial YouTube OAuth setup (run once)
python upload_video.py

# Update/refresh OAuth credentials
python update_tokens.py
```

### Running the Application
```bash
# One-time execution
RUN_ONCE=true python main.py

# Scheduled execution with cron
CRON_SCHEDULE="0 */6 * * *" python main.py

# Run with Docker
docker compose up

# Testing stock video functionality
python test.py
```

### Project Structure & Configuration
- `config.py` - Central configuration with environment variables and API keys
- `main.py` - Entry point with scheduler and video generation orchestration
- `requirements.txt` - Python dependencies
- `utils/` - Core functionality modules
- `credentials/` - YouTube OAuth credentials (client_secrets.json, tokens.json)
- `music/` - Background music files (.mp3)
- `secondary_video/` - Secondary video content (.mp4)
- `temp/` - Temporary files during processing
- `output/` - Final generated videos organized by date

## Architecture Overview

This is an automated YouTube Shorts/TikTok video generation system that creates engaging short-form content using AI. The application follows a pipeline architecture:

### Core Pipeline (main.py:55-121)
1. **Topic Generation** - Selects from predefined controversial topics
2. **Content Creation** - Generates titles, scripts, and descriptions using OpenAI
3. **Media Assembly** - Combines stock footage, voiceover, and subtitles
4. **Upload & Storage** - Automatically uploads to platforms and saves metadata

### Key Modules

**utils/llm.py** - OpenAI integration for content generation
- `get_topic()` - Random topic selection from `POSSIBLE_TOPICS`
- `get_titles()`, `get_script()` - AI-generated content
- `get_most_engaging_titles()` - Content ranking and selection

**utils/video.py** - Video processing and assembly
- `generate_subtitles()` - AssemblyAI transcription with SRT equalization
- `combine_videos()` - Concatenates stock footage to match audio duration
- `generate_video()` - Final composition with subtitles, audio, and secondary content

**utils/audio.py** - Voice generation and audio processing
- `generate_voiceover()` - Google Gemini TTS with custom voice (Fenrir)
- `get_random_background_song()` - Random background music selection

**utils/stock_videos.py** - External media sourcing
- `get_stock_videos()` - Pexels API integration for relevant footage

**utils/yt.py** - Platform upload functionality
- `auto_upload()` - YouTube upload with OAuth 2.0 authentication
- Uses `upload_video.py` script for actual upload process

### Environment Variables
Key configurations in `.env`:
- `OPENAI_API_KEY_AUTO_YT_SHORTS` - OpenAI API access
- `GEMINI_API_KEY` - Google Gemini TTS
- `PEXELS_API_KEY` - Stock video sourcing
- `ASSEMBLY_AI_API_KEY` - Subtitle generation
- `CRON_SCHEDULE` - Automated execution timing
- `RUN_ONCE` - Single execution mode
- `VIDEO_COUNT` - Number of videos per run
- `NO_UPLOAD` - Disable platform uploads
- `NOTIFY_ON_SUCCESS` - Success notifications via Apprise

### Execution Modes
- **Scheduled Mode**: Uses APScheduler with cron expressions for automated generation
- **One-time Mode**: Single execution when `RUN_ONCE=true`
- **Docker Mode**: Containerized execution with volume mounts for credentials and content

The system is designed for unattended operation, generating content based on controversial topics to maximize engagement, with comprehensive error handling and notification systems.