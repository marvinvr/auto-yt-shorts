<p align="left">
  <img src="auto-yt-shorts.png" width="60%" alt="project-logo">
</p>
<p align="left">
    <h1 align="left">AUTO-YT-SHORTS</h1>
</p>
<p align="left">
	<img src="https://img.shields.io/github/license/marvinvr/auto-yt-shorts?style=flat-square&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/marvinvr/auto-yt-shorts?style=flat-square&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/marvinvr/auto-yt-shorts?style=flat-square&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/marvinvr/auto-yt-shorts?style=flat-square&color=0080ff" alt="repo-language-count">
<p>
<p align="left">
		<em>Developed with the software and tools below.</em>
</p>
<p align="left">
	<img src="https://img.shields.io/badge/tqdm-FFC107.svg?style=flat-square&logo=tqdm&logoColor=black" alt="tqdm">
	<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=flat-square&logo=YAML&logoColor=white" alt="YAML">
	<img src="https://img.shields.io/badge/SciPy-8CAAE6.svg?style=flat-square&logo=SciPy&logoColor=white" alt="SciPy">
	<img src="https://img.shields.io/badge/OpenAI-412991.svg?style=flat-square&logo=OpenAI&logoColor=white" alt="OpenAI">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat-square&logo=Docker&logoColor=white" alt="Docker">
	<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat-square&logo=GitHub-Actions&logoColor=white" alt="GitHub%20Actions">
	<img src="https://img.shields.io/badge/FastAPI-009688.svg?style=flat-square&logo=FastAPI&logoColor=white" alt="FastAPI">
</p>

<br><!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary><br>

- [ Overview](#-overview)
- [ Demo](#-demo)
- [ Features](#-features)
- [ Repository Structure](#-repository-structure)
- [ Modules](#-modules)
- [ Getting Started](#-getting-started)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Tests](#-tests)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)
</details>
<hr>

## Overview

Auto-yt-shorts is an open-source project designed to automate the process of generating engaging short videos for platforms like YouTube and TikTok. Leveraging AI models and APIs, it enables the effortless creation of video content by suggesting topics, generating voiceovers, adding subtitles, and incorporating stock footage. With features like automatic uploads, background song selection, and parallel execution, auto-yt-shorts offers a valuable solution for content creators seeking a seamless video production workflow.

**Note:**
This project has been created out of curiosity and for educational purposes. It is not intended for commercial use or to infringe on any copyrights, and it is not actively being used to generate AI-generated videos.

---

## Demo

The YouTube channel below showcases the auto-yt-shorts project in action, a few examples of the videos generated using the AI model, and the process of uploading them to the platform.

==> [QuickQuirks YouTube Channel](https://www.youtube.com/channel/UC4igt1OgsZGBs7PRqpxI9eQ)

---

## Features

|     | Feature          | Description                                                                                                                                                                                                                    |
| --- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ⚙️  | **Architecture** | _The project utilizes a modular architecture with components for video generation, processing, and uploading. It leverages Python environment setup with Docker, FastAPI for web services, and OpenAI for content generation._ |
| 🔌  | **Integrations** | _Key integrations include OAuth 2.0 for YouTube uploads, Pexels for stock videos, OpenAI for content generation, and AssemblyAI for audio processing. External dependencies like scipy and httplib2 enhance functionality._    |
| 🧩  | **Modularity**   | _The codebase is modular with distinct modules for metadata, video processing, AI content generation, and upload functionalities._                                                                                             |
| ⚡️ | **Performance**  | _Efficiency is maintained through parallel execution for video processing, allowing for faster content generation. The use of Docker containers aids in resource management and scalability of the application._               |
| 📦  | **Dependencies** | _Key dependencies include oauth2client, FastAPI, OpenAI, and Docker for environment setup and execution. External libraries like pillow and opencv-python enhance image and video processing capabilities._                    |

---

## Repository Structure

```sh
└── auto-yt-shorts/
    ├── .github
    │   └── workflows
    ├── Dockerfile
    ├── config.py
    ├── docker-compose.yml
    ├── environment.yml
    ├── example.env
    ├── fonts
    │   └── bold_font.ttf
    ├── main.py
    ├── requirements.txt
    ├── test.http
    ├── upload_video.py
    └── utils
        ├── audio.py
        ├── llm.py
        ├── metadata.py
        ├── stock_videos.py
        ├── tiktok.py
        ├── video.py
        └── yt.py
```

---

## Modules

<details closed><summary>.</summary>

| File                                                                                            | Summary                                                                                                                                                                                                                                                                              |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [config.py](https://github.com/marvinvr/auto-yt-shorts/blob/master/config.py)                   | Defines settings and API keys for controversial topic generation, OpenAI model selection, minimum/maximum search terms, and API keys for Pexels, AssemblyAI, and News API. Creates directories for temporary and output files, background songs, and secondary video content.        |
| [requirements.txt](https://github.com/marvinvr/auto-yt-shorts/blob/master/requirements.txt)     | Manages project dependencies such as OpenAI and FastAPI to facilitate AI video generation, processing, and uploading functionalities within the auto-yt-shorts repository's ecosystem. The file ensures seamless integration of critical libraries for efficient execution of tasks. |
| [environment.yml](https://github.com/marvinvr/auto-yt-shorts/blob/master/environment.yml)       | Defines dependencies and environment setup for Python project auto-yt-shorts. Specifies required packages and their versions, ensuring compatibility and consistent development environment for the repository.                                                                      |
| [Dockerfile](https://github.com/marvinvr/auto-yt-shorts/blob/master/Dockerfile)                 | Builds a Docker container for auto-yt-shorts project, setting up Python environment and executing necessary commands. Copies project files, installs dependencies, and initiates the main script within a Python virtual environment.                                                |
| [test.http](https://github.com/marvinvr/auto-yt-shorts/blob/master/test.http)                   | Generate_videos/.                                                                                                                                                                                                                                                                    |
| [upload_video.py](https://github.com/marvinvr/auto-yt-shorts/blob/master/upload_video.py)       | Enables uploading videos to YouTube with OAuth 2.0 authentication and customizable metadata. Implements retry logic and resumable uploads for reliability. Facilitates seamless integration with the parent repositorys video processing workflow.                                   |
| [docker-compose.yml](https://github.com/marvinvr/auto-yt-shorts/blob/master/docker-compose.yml) | Orchestrates Docker containers for the auto-yt-shorts service, configuring volumes and environment variables. Exposes port 8000 for external access.                                                                                                                                 |
| [main.py](https://github.com/marvinvr/auto-yt-shorts/blob/master/main.py)                       | Generates and processes video content based on user input, leveraging parallel execution for efficiency. Handles video metadata, stock footage selection, voiceover generation, and automatic upload to the platform.                                                                |

</details>

<details closed><summary>utils</summary>

| File                                                                                            | Summary                                                                                                                                                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [metadata.py](https://github.com/marvinvr/auto-yt-shorts/blob/master/utils/metadata.py)         | Creates and stores metadata for a video, moving the video file to designated output location and saving metadata in JSON format.                                                                                                                                                               |
| [llm.py](https://github.com/marvinvr/auto-yt-shorts/blob/master/utils/llm.py)                   | Generates engaging TikTok video ideas, titles, and descriptions based on user input topics. Utilizes OpenAIs language model to suggest captivating content elements in a conversational manner. Enhances creativity in content creation for short-form videos.                                 |
| [yt.py](https://github.com/marvinvr/auto-yt-shorts/blob/master/utils/yt.py)                     | Enables automatic and manual video uploads to YouTube. Automatically uploads video with specified details. Prepares videos for manual upload by organizing into folders with relevant metadata. Organized and streamlined YouTube video upload functionalities in the repository architecture. |
| [tiktok.py](https://github.com/marvinvr/auto-yt-shorts/blob/master/utils/tiktok.py)             | Enables TikTok video uploads using AuthBackend for authentication and upload_video function. Facilitates captioning and customizing upload settings.                                                                                                                                           |
| [audio.py](https://github.com/marvinvr/auto-yt-shorts/blob/master/utils/audio.py)               | Generates voiceovers and selects random background songs for videos using OpenAI API and local files. Provides functionalities for creating audio files and selecting music assets in the auto-yt-shorts repository structure.                                                                 |
| [stock_videos.py](https://github.com/marvinvr/auto-yt-shorts/blob/master/utils/stock_videos.py) | Retrieves stock videos based on search terms using Pexels API. Integrates with the parent repositorys architecture via config and video utils. Implements video search and retrieval functionalities for further processing.                                                                   |
| [video.py](https://github.com/marvinvr/auto-yt-shorts/blob/master/utils/video.py)               | Generates subtitles and combines videos into a single clip with burnt-in subtitles and background music. Includes functionality to save videos from URLs and add secondary content.                                                                                                            |

</details>

---

## Getting Started

### Locally

**System Requirements:**

- **Python**: `version 3.12`

#### Installation

<h4>From <code>source</code></h4>

> 1. Clone the auto-yt-shorts repository:
>
> ```console
> $ git clone https://github.com/marvinvr/auto-yt-shorts
> ```
>
> 2. Change to the project directory:
>
> ```console
> $ cd auto-yt-shorts
> ```
>
> 3. Update the environment file:
>
> ```console
> $ cp example.env .env
> ```
>
> 4. Update the `.env` file with your API keys and other credentials.
>
> 5. Prefill the `music` and `secondary_video` directories with background music and secondary video content. The tool will automatically select and use these files.
>
> 6. Setup and Authenticate with YouTube using the OAuth 2.0 flow:
>
> Follow the instructions in the [YouTube Data API documentation](https://developers.google.com/youtube/v3/quickstart/python) to create a project and obtain OAuth 2.0 credentials.
>
> ```console
> $ python upload_video.py
> ```
>
> 7. Install the dependencies:
>
> ```console
> $ pip install -r requirements.txt
> ```

#### Usage

<h4>From <code>source</code></h4>

> Run auto-yt-shorts using the command below:
>
> ```console
> $ python main.py
> ```

### With Docker

> Start the Docker container using the command below:
>
> ```console
> $ docker compose up
> ```
>
> The application will be accessible at `http://localhost:8000`. You can send a POST request to the `/generate_videos` endpoint with the required parameters to generate a video.

---

## Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/marvinvr/auto-yt-shorts/issues)**: Submit bugs found or log feature requests for the `auto-yt-shorts` project.
- **[Join the Discussions](https://github.com/marvinvr/auto-yt-shorts/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/marvinvr/auto-yt-shorts
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="center">
   <a href="https://github.com{/marvinvr/auto-yt-shorts/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=marvinvr/auto-yt-shorts">
   </a>
</p>
</details>

---

## License

This project is protected under the [MIT](https://choosealicense.com/licenses/mit) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/mit) file.

---

## Acknowledgments

- This project was inspired by the [MoneyPrinter](https://github.com/FujiwaraChoki/MoneyPrinter) repository. Some of the code and ideas were adapted from this project.

---
