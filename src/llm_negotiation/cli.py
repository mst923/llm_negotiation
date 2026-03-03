from __future__ import annotations

import argparse
import logging
import sys

from .config import DEFAULT_ITERATIONS, DEFAULT_MODEL, DEFAULT_TEMPERATURE, GAME_REGISTRY, build_config
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
        help=f"OpenAI model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=f"Sampling temperature (default: {DEFAULT_TEMPERATURE})",
    )

    strategic_group = parser.add_mutually_exclusive_group()
    strategic_group.add_argument(
        "--strategic",
        action="store_true",
        default=None,
        help="Enable strategic thinking prompt",
    )
    strategic_group.add_argument(
        "--no-strategic",
        action="store_true",
        default=None,
        help="Disable strategic thinking prompt",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
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
        "verbose": args.verbose,
    }

    if args.strategic is True:
        overrides["strategic"] = True
    elif args.no_strategic is True:
        overrides["strategic"] = False

    config = build_config(args.game, **overrides)
    try:
        run_experiment(config)
    except RuntimeError as exc:
        logging.error("%s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
