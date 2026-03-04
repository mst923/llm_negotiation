from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class ProposerResponse(BaseModel):
    """Response schema for ultimatum / dictator / dictator_anonymous games."""

    model_config = ConfigDict(extra="forbid")

    reasoning: str
    decision: str
    offer: int


class ReceiverResponse(BaseModel):
    """Response schema for unfair_receiver game."""

    model_config = ConfigDict(extra="forbid")

    reasoning: str
    decision: Literal["accept", "reject"]


class PersonalityResponse(BaseModel):
    """Response schema for personality generation (name and occupation only)."""

    model_config = ConfigDict(extra="forbid")

    name: str
    occupation: str


def build_response_format(model_class: type[BaseModel]) -> dict[str, Any]:
    """Build an OpenAI ``response_format`` dict from a Pydantic model.

    Returns a ``json_schema`` response format suitable for the OpenAI API.
    """
    return {
        "type": "json_schema",
        "json_schema": {
            "name": model_class.__name__,
            "schema": model_class.model_json_schema(),
            "strict": True,
        },
    }
