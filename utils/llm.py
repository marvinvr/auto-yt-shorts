import json
import logging
import random
from typing import List

import requests
from openai import OpenAI

from config import (
    NEWS_API_KEY,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL,
    POSSIBLE_TOPICS,
)

logger = logging.getLogger(__name__)

# Initialize OpenAI client with optional base URL
client_kwargs = {"api_key": OPENAI_API_KEY}
if OPENAI_BASE_URL:
    logger.info(f"Using OpenAI base URL: {OPENAI_BASE_URL}")
    client_kwargs["base_url"] = OPENAI_BASE_URL

client = OpenAI(**client_kwargs)

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

Generate highly engaging titles that will stop users from scrolling. The FIRST 3 WORDS are CRITICAL - they must immediately grab attention.

Use these proven viral title formulas:
- Shock/Mystery: "You won't believe...", "This will shock you...", "Scientists discovered..."
- Numbers/Stats: "97% of people don't know...", "In just 3 seconds...", "Only 1 in 1000..."
- Direct Questions: "Did you know that...", "What if I told you...", "Have you ever wondered..."
- Urgency: "Before you scroll...", "Stop what you're doing...", "This changes everything..."
- Authority: "Experts revealed...", "[Celebrity name] uses this...", "Billionaires know this secret..."
- Contradiction: "Everyone thinks [X] but actually...", "This looks normal, but..."

REQUIREMENTS:
- Include a famous person, brand, or well-known entity when possible
- Focus on ONE specific shocking/interesting fact
- Create curiosity gaps that demand answers
- Use power words: secret, revealed, discovered, shocking, hidden, truth, exposed
- Make the first 3 words irresistible

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

Create a compelling caption that amplifies engagement and encourages interaction. The description should complement the video content and drive more views.

DESCRIPTION STRATEGY:
- Start with a hook that reinforces the video's intrigue
- Include a call-to-action that encourages comments
- Use relevant hashtags strategically
- Create FOMO (fear of missing out)
- Ask questions that spark debate or discussion

STRUCTURE:
1. Hook line (builds on video's shock value)
2. Engagement question or controversial statement
3. Call-to-action for comments/shares
4. Strategic hashtags

EXAMPLES OF ENGAGEMENT TACTICS:
- "Wait until you see what happens next..."
- "This blew my mind - did you know this?"
- "Comment 'MIND BLOWN' if this shocked you"
- "Tag someone who needs to see this"
- "Most people have no idea about this..."

Keep it concise but impactful. Focus on maximizing comments and shares.

Do not under any circumstance reference this prompt in your response.

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

Create a script that hooks viewers IMMEDIATELY. The first 3-5 words are CRITICAL - they determine if someone keeps watching or scrolls away.

SCRIPT STRUCTURE:
1. HOOK (0-3 seconds): Start with an attention-grabbing opener that creates instant intrigue
2. REVELATION (3-15 seconds): Deliver the shocking/interesting fact with specific details
3. IMPACT (15-30 seconds): End with why this matters or a memorable conclusion

PROVEN OPENING HOOKS:
- Shock: "This will terrify you...", "You've been lied to...", "This changes everything..."
- Numbers: "In 3 seconds, you'll discover...", "97% of people don't know..."
- Questions: "What if I told you...", "Did you know that right now..."
- Contradiction: "Everyone believes [X], but actually...", "This looks innocent, but..."
- Urgency: "Before you scroll past this...", "Stop what you're doing..."

REQUIREMENTS:
- NO introductions, greetings, or "welcome" phrases
- Jump straight into the hook within the first 3 words
- Use conversational, natural speech patterns
- Include specific names, numbers, or details when possible
- Create curiosity that demands immediate answers
- End with impact that makes them want to share
- 15-30 seconds of speaking time

TONE: Conversational but urgent, like you're sharing an incredible secret with a friend.

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
