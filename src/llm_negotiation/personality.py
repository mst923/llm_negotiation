from __future__ import annotations

import logging
import random
from enum import Enum

from autogen import ConversableAgent

from .prompts import PERSONALITY_SYSTEM_MESSAGE
from .schemas import PersonalityResponse, build_response_format

logger = logging.getLogger(__name__)


class Region(str, Enum):
    NORTH_AMERICA = "North America"
    SOUTH_AMERICA = "South America"
    EUROPE = "Europe"
    EAST_ASIA = "East Asia"
    SOUTH_ASIA = "South Asia"
    SOUTHEAST_ASIA = "Southeast Asia"
    MIDDLE_EAST = "Middle East"
    AFRICA = "Africa"
    OCEANIA = "Oceania"


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    LGBTQ = "LGBTQ"


_GENDER_WEIGHTS = {
    Gender.MALE: 0.45,
    Gender.FEMALE: 0.45,
    Gender.LGBTQ: 0.10,
}


def _random_demographics() -> tuple[Region, int, Gender]:
    """Generate random region, age, and gender."""
    region = random.choice(list(Region))
    age = random.randint(5, 80)
    gender = random.choices(
        list(_GENDER_WEIGHTS.keys()),
        weights=list(_GENDER_WEIGHTS.values()),
        k=1,
    )[0]
    return region, age, gender


def generate_personality(api_key: str, model: str) -> dict[str, str] | None:
    """Generate a random personality and return a dict of attributes.

    Returns a dict with keys ``region``, ``name``, ``age``, ``gender``,
    ``occupation``.  Returns ``None`` when the generation fails.
    """
    region, age, gender = _random_demographics()

    system_message = PERSONALITY_SYSTEM_MESSAGE.format(
        region=region.value,
        age=age,
        gender=gender.value,
    )

    # Some models (e.g. gpt-5-mini) only support temperature=1.
    temp: float | None = random.uniform(0, 1)
    if "gpt-5" in model:
        temp = None  # omit → use model default

    llm_extra: dict = {}
    if temp is not None:
        llm_extra["temperature"] = temp

    personality_agent = ConversableAgent(
        name="Personality_Agent",
        system_message=system_message,
        llm_config={
            "config_list": [
                {
                    "model": model,
                    "api_key": api_key,
                    "response_format": build_response_format(PersonalityResponse),
                }
            ],
            **llm_extra,
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
            message="Generate a name and occupation for this person.",
            max_turns=1,
        )
        content = result.chat_history[-1]["content"]
        data = PersonalityResponse.model_validate_json(content)
        return {
            "region": region.value,
            "name": data.name,
            "age": str(age),
            "gender": gender.value,
            "occupation": data.occupation,
        }
    except Exception as exc:
        logger.warning("Personality generation failed: %s", exc)
        return None
