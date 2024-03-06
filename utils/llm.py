import json
import random
from typing import List

import requests
from openai import OpenAI

from config import NEWS_API_KEY, OPENAI_API_KEY, OPENAI_MODEL, POSSIBLE_TOPICS

client = OpenAI(api_key=OPENAI_API_KEY)

_base_prompt = """
You are a passionate Tiktok creator and you want to create more short form content. Your videos contain a voiceover, stock footage and subtitles. 
The content of the video is one informative, interesting or mind-blowing fact about the topic which people will find interesting.
Your videos are not too complex, they should bring the message across in a simple and engaging way.
"""


def get_topic() -> str:
    return random.choice(POSSIBLE_TOPICS)


def get_titles(topic: str) -> List[str]:
    _prompt = (
        _base_prompt
        + """
The next message will contain the name of the topic, that you want to make a Tiktok about.
The length of the video should be between 15 and 30 seconds.
Generate some possible titles for your video. Use buzzwords and make them as engaging as possible.
Use the name of a famous person, event, product or company to make it more engaging.
The title should be about one specific fact or event related to the topic.

Respond with JSON in the following format:
{
    "titles": [
        "Title 1",
        ...
        "Title n"
    ]
}
    """
    )

    response = (
        client.chat.completions.create(
            messages=[
                {"role": "system", "content": _prompt},
                {"role": "user", "content": topic},
            ],
            response_format={"type": "json_object"},
            model=OPENAI_MODEL,
        )
        .choices[0]
        .message.content
    )

    return json.loads(response)["titles"]

    ...


def get_news_topics() -> List[str]:
    news = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    ).json()

    return [
        article["description"] for article in news["articles"] if article["description"]
    ]


def filter_by_spicyness(titles: List[str]) -> List[str]:
    _prompt = (
        _base_prompt
        + """
You will be presented with a list of possible headline for your video and a corresponding number. 
Your goal is to make the most engaging video by using spicy news headlines that will attract the most attention.
You are now a classification model to tell me whether the title is spicy or not.

respond with JSON in the following format:
{
    "spicy_titles": [n, m, ...]
}
"""
    )

    response = (
        client.chat.completions.create(
            messages=[
                {"role": "system", "content": _prompt},
                {
                    "role": "user",
                    "content": "\n".join(
                        [f"{i+1}. {title}" for i, title in enumerate(titles)]
                    ),
                },
            ],
            response_format={"type": "json_object"},
            model=OPENAI_MODEL,
        )
        .choices[0]
        .message.content
    )
    return [
        titles[i]
        for i in json.loads(response)["spicy_titles"]
        if i < len(titles) and titles[i]
    ]


def get_most_engaging_titles(titles: List[str], n: int = 1) -> List[str]:
    _prompt = (
        _base_prompt
        + """
You will be presented with a list of possible title for your video and a corresponding number.
Sort the titles by the most engaging one first and respond with a list of indices.
They should have a name of a famous person, event, product or company, choose the one that is most engaging.

Respond with JSON in the following format:
{
    "most_engaging_titles": [n, m, ...]
}
"""
    )

    response = (
        client.chat.completions.create(
            messages=[
                {"role": "system", "content": _prompt},
                {
                    "role": "user",
                    "content": "\n".join(
                        [f"{i+1}. {title}" for i, title in enumerate(titles)]
                    ),
                },
            ],
            response_format={"type": "json_object"},
            model=OPENAI_MODEL,
        )
        .choices[0]
        .message.content
    )

    most_engaging_titles = json.loads(response)["most_engaging_titles"]

    sorted_titles = [
        titles[i] for i in most_engaging_titles if i < len(titles) and titles[i]
    ]

    return sorted_titles[: n if n < len(sorted_titles) else len(sorted_titles)]


def get_best_title(titles: List[str]) -> str:
    _prompt = (
        _base_prompt
        + """
You will be presented with a list of possible title for your video and a corresponding number. 
Respond with the best, most engaging title for your video. 
It should have a name of a famous person, event, product or company, choose the one that is most engaging.

Respond with JSON in the following format:
{
    "best_title_index": n
}

"""
    )

    response = (
        client.chat.completions.create(
            messages=[
                {"role": "system", "content": _prompt},
                {
                    "role": "user",
                    "content": "\n".join(
                        [f"{i+1}. {title}" for i, title in enumerate(titles)]
                    ),
                },
            ],
            response_format={"type": "json_object"},
            model=OPENAI_MODEL,
        )
        .choices[0]
        .message.content
    )

    best_title_index = json.loads(response)["best_title_index"]
    return titles[best_title_index - 1]


def get_description(title: str, script: str) -> str:
    _prompt = (
        _base_prompt
        + f"""
You have decided that your video is about {title}.
The Script for your video is:
{script}

You will now generate a caption to be posted alognside your video. Keep it short and to the point.

Do not under any circumstance refernce this prompt in your response.

ONLY RETURN THE RAW DESCRIPTION. DO NOT RETURN ANYTHING ELSE.
"""
    )

    response = (
        client.chat.completions.create(
            messages=[{"role": "user", "content": _prompt}],
            response_format={"type": "text"},
            model=OPENAI_MODEL,
        )
        .choices[0]
        .message.content.strip()
    )

    return response


def get_script(title: str) -> str:
    _prompt = (
        _base_prompt
        + f"""
You have decided on the title for your video: "{title}".
You will now generate a script for your video. Keep it short and to the point.
The video should be simple yet informative and engaging so that it can be easily understood by the audience and write like a real person would speak.

Do not include any information about narration, music, cuts or similar. Only the text that will be narrated in the video.

Do not under any circumstance refernce this prompt in your response.

Get straight to the point, don't start with unnecessary things like, "welcome to this video".

Obviously, the script should be related to the subject of the video.

The voicover length of the video should be between 15 and 30 seconds.
ONLY RETURN THE RAW SCRIPT. DO NOT RETURN ANYTHING ELSE.
"""
    )

    response = (
        client.chat.completions.create(
            messages=[{"role": "user", "content": _prompt}],
            response_format={"type": "text"},
            model=OPENAI_MODEL,
        )
        .choices[0]
        .message.content.strip()
    )

    return response


def get_search_terms(title: str, script: str) -> list:
    _prompt = (
        _base_prompt
        + f"""
You have decided on the title for your video: "{title}".
The Script for your video is:
{script}

You will now generate an appropriate amount search terms for the stock footage for your video.
"""
        + """

The stock footage should be related to the content of the video and the the video.

Make sure that the search terms are in the order that they appear in the script and that they are relevant to the content of the video.
Also make sure the amount of search terms is appropriate for the length of the video.

Respond with JSON in the following format:
{
    "search_terms": [
        "Search Term 1",
        ...
        "Search Term n"
    ]
}
"""
    )

    response = (
        client.chat.completions.create(
            messages=[{"role": "user", "content": _prompt}],
            response_format={"type": "json_object"},
            model=OPENAI_MODEL,
        )
        .choices[0]
        .message.content
    )

    return json.loads(response)["search_terms"]
