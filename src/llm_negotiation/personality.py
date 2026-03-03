from __future__ import annotations

import json
import logging
import random

from autogen import ConversableAgent

from .prompts import PERSONALITY_SYSTEM_MESSAGE

logger = logging.getLogger(__name__)


def generate_personality(api_key: str, model: str) -> str | None:
    """Generate a random personality and return a features string.

    Returns ``None`` when the personality generation fails.
    """
    temp = random.uniform(0, 1)

    personality_agent = ConversableAgent(
        name="Personality_Agent",
        system_message=PERSONALITY_SYSTEM_MESSAGE,
        llm_config={
            "config_list": [
                {
                    "model": model,
                    "api_key": api_key,
                    "response_format": {"type": "json_object"},
                }
            ],
            "temperature": temp,
        },
    )

    support = ConversableAgent(
        name="Personality_Support",
        llm_config=False,
        human_input_mode="NEVER",
    )

    try:
        result = support.initiate_chat(
            personality_agent,
            message="generate individuality of other agents",
            max_turns=1,
        )
        content = result.chat_history[-1]["content"]
        data = json.loads(content)
        name = data["name"]
        age = data["age"]
        gender = data["gender"]
        return f"name : {name}, age : {age}, gender : {gender}"
    except Exception as exc:
        logger.warning("Personality generation failed: %s", exc)
        return None
