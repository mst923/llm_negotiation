from __future__ import annotations

import argparse
import logging
import sys

from .config import DEFAULT_ITERATIONS, DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_WORKERS, GAME_REGISTRY, PERSONA_PROMPTS, build_config
from .runner import run_experiment


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="llm-negotiation",
        description="Run behavioral economics games with LLM agents",
    )
    parser.add_argument(
        "game",
        choices=list(GAME_REGISTRY),
        help="Game type to run",
    )
    parser.add_argument(
        "-n", "--iterations",
        type=int,
        default=DEFAULT_ITERATIONS,
        help=f"Number of iterations (default: {DEFAULT_ITERATIONS})",
    )
    parser.add_argument(
        "-r", "--run-id",
        default="1",
        help="Run identifier for the output filename (default: 1)",
    )
    parser.add_argument(
        "-m", "--model",
        default=DEFAULT_MODEL,
        help=f"OpenAI model for the game agent (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--personality-model",
        default=None,
        help="OpenAI model for personality generation (default: same as --model)",
    )
    parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=f"Sampling temperature (default: {DEFAULT_TEMPERATURE})",
    )

    parser.add_argument(
        "--persona",
        choices=list(PERSONA_PROMPTS),
        default=None,
        help="Persona to use (default: per-game default)",
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"Number of parallel workers (default: {DEFAULT_WORKERS})",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--proposal-source",
        choices=["human", "computer"],
        default="human",
        help="Proposal source for unfair_receiver game (default: human)",
    )

    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    overrides: dict = {
        "iterations": args.iterations,
        "run_id": args.run_id,
        "model": args.model,
        "temperature": args.temperature,
        "workers": args.workers,
        "verbose": args.verbose,
        "proposal_source": args.proposal_source,
    }

    if args.persona is not None:
        overrides["persona"] = args.persona
    if args.personality_model is not None:
        overrides["personality_model"] = args.personality_model

    config = build_config(args.game, **overrides)
    try:
        run_experiment(config)
    except RuntimeError as exc:
        logging.error("%s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
