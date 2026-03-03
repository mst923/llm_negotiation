from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .prompts import (
    DICTATOR_ANONYMOUS_PROMPT,
    DICTATOR_PROMPT,
    SYSTEM_PROMPT,
    ULTIMATUM_PROMPT,
    UNFAIR_RECEIVER_PROMPT,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"

DEFAULT_MODEL = "gpt-4o-mini-2024-07-18"
DEFAULT_TEMPERATURE = 1.0
DEFAULT_ITERATIONS = 100


@dataclass(frozen=True)
class GameConfig:
    name: str
    prompt: str
    result_subdir: str
    agent_name: str
    strategic: bool
    result_keys: dict[str, str]
    """Maps CSV column name -> JSON key in the LLM response."""

    system_prompt: str = SYSTEM_PROMPT
    model: str = DEFAULT_MODEL
    temperature: float = DEFAULT_TEMPERATURE
    iterations: int = DEFAULT_ITERATIONS
    run_id: str = "1"
    verbose: bool = False

    def output_dir(self) -> Path:
        strategy_label = "strategic" if self.strategic else "not_strategic"
        return RESULTS_DIR / self.result_subdir / strategy_label

    def output_path(self) -> Path:
        return self.output_dir() / f"{self.name}_{self.run_id}.csv"


GAME_REGISTRY: dict[str, dict] = {
    "ultimatum": dict(
        prompt=ULTIMATUM_PROMPT,
        result_subdir="ultimatum",
        agent_name="Proposer",
        strategic=False,
        result_keys={"offer": "offer", "reason": "reasoning"},
    ),
    "dictator": dict(
        prompt=DICTATOR_PROMPT,
        result_subdir="dictator",
        agent_name="Player_Red",
        strategic=True,
        result_keys={"offer": "offer", "reason": "reasoning"},
    ),
    "dictator_anonymous": dict(
        prompt=DICTATOR_ANONYMOUS_PROMPT,
        result_subdir="dictator_anonymous",
        agent_name="Player_Red",
        strategic=False,
        result_keys={"offer": "offer", "reason": "reasoning"},
    ),
    "unfair_receiver": dict(
        prompt=UNFAIR_RECEIVER_PROMPT,
        result_subdir="unfair_receiver",
        agent_name="Receiver",
        strategic=False,
        result_keys={"decision": "decision", "reason": "reasoning"},
    ),
}


def build_config(game: str, **overrides) -> GameConfig:
    """Build a GameConfig for the named game, applying any CLI overrides."""
    if game not in GAME_REGISTRY:
        raise ValueError(f"Unknown game {game!r}. Choose from: {list(GAME_REGISTRY)}")
    params = {**GAME_REGISTRY[game], "name": game, **overrides}
    return GameConfig(**params)
