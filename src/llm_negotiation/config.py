from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from .prompts import (
    DICTATOR_ANONYMOUS_PROMPT,
    DICTATOR_PROMPT,
    SYSTEM_PROMPT,
    ULTIMATUM_PROMPT,
    UNFAIR_RECEIVER_COMPUTER_PROMPT,
    UNFAIR_RECEIVER_PROMPT,
)
from .schemas import ProposerResponse, ReceiverResponse, build_response_format

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"

DEFAULT_MODEL = "gpt-4o-mini-2024-07-18"
DEFAULT_TEMPERATURE = 1.0
DEFAULT_ITERATIONS = 100
DEFAULT_WORKERS = 1

PERSONA_PROMPTS: dict[str, str] = {
    "normal": "",
    "strategic": " You are a strategic agent.",
    "greedy": " You are a greedy agent.",
    "benevolent": " You are a benevolent agent.",
    "openness": " You score high on openness to experience: you are curious, creative, and open-minded.",
    "conscientiousness": " You score high on conscientiousness: you are organized, disciplined, and goal-oriented.",
    "extraversion": " You score high on extraversion: you are outgoing, energetic, and sociable.",
    "agreeableness": " You score high on agreeableness: you are friendly, compassionate, and cooperative.",
    "neuroticism": " You score high on neuroticism: you are emotionally sensitive, anxious, and cautious.",
}


@dataclass(frozen=True)
class GameConfig:
    name: str
    prompt: str
    result_subdir: str
    agent_name: str
    persona: str
    response_model: type[BaseModel]
    csv_fields: dict[str, str]
    """Maps CSV column name -> model field name."""

    system_prompt: str = SYSTEM_PROMPT
    model: str = DEFAULT_MODEL
    personality_model: str = ""
    temperature: float = DEFAULT_TEMPERATURE
    iterations: int = DEFAULT_ITERATIONS
    workers: int = DEFAULT_WORKERS
    run_id: str = "1"
    verbose: bool = False
    proposal_source: str = "human"

    @property
    def effective_personality_model(self) -> str:
        """Return personality_model if set, otherwise fall back to model."""
        return self.personality_model or self.model

    @property
    def response_format(self) -> dict[str, Any]:
        return build_response_format(self.response_model)

    def output_dir(self) -> Path:
        return RESULTS_DIR / self.result_subdir / self.persona / self.model

    def output_path(self) -> Path:
        return self.output_dir() / f"{self.name}_{self.run_id}.csv"


GAME_REGISTRY: dict[str, dict] = {
    "ultimatum": dict(
        prompt=ULTIMATUM_PROMPT,
        result_subdir="ultimatum",
        agent_name="Proposer",
        persona="normal",
        response_model=ProposerResponse,
        csv_fields={"offer": "offer", "reason": "reasoning"},
    ),
    "dictator": dict(
        prompt=DICTATOR_PROMPT,
        result_subdir="dictator",
        agent_name="Player_Red",
        persona="strategic",
        response_model=ProposerResponse,
        csv_fields={"offer": "offer", "reason": "reasoning"},
    ),
    "dictator_anonymous": dict(
        prompt=DICTATOR_ANONYMOUS_PROMPT,
        result_subdir="dictator_anonymous",
        agent_name="Player_Red",
        persona="normal",
        response_model=ProposerResponse,
        csv_fields={"offer": "offer", "reason": "reasoning"},
    ),
    "unfair_receiver": dict(
        prompt=UNFAIR_RECEIVER_PROMPT,
        result_subdir="unfair_receiver",
        agent_name="Receiver",
        persona="normal",
        response_model=ReceiverResponse,
        csv_fields={"decision": "decision", "reason": "reasoning"},
    ),
}


def build_config(game: str, **overrides) -> GameConfig:
    """Build a GameConfig for the named game, applying any CLI overrides."""
    if game not in GAME_REGISTRY:
        raise ValueError(f"Unknown game {game!r}. Choose from: {list(GAME_REGISTRY)}")
    params = {**GAME_REGISTRY[game], "name": game, **overrides}
    if game == "unfair_receiver" and params.get("proposal_source") == "computer":
        params["prompt"] = UNFAIR_RECEIVER_COMPUTER_PROMPT
        params["result_subdir"] = "unfair_receiver_computer"
    return GameConfig(**params)
