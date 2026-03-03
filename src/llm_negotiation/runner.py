from __future__ import annotations

import csv
import logging
import os

from autogen import ConversableAgent
from dotenv import load_dotenv

from .config import GameConfig
from .parsing import parse_response
from .personality import generate_personality

logger = logging.getLogger(__name__)


def run_experiment(config: GameConfig) -> None:
    """Run *config.iterations* rounds of the configured game and write CSV."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment or .env")

    system_prompt = config.system_prompt
    user_message = config.prompt

    agent_llm_config = [
        {
            "model": config.model,
            "api_key": api_key,
            "response_format": {"type": "json_object"},
        }
    ]

    data: list[dict[str, str]] = []

    for i in range(config.iterations):
        logger.info("Iteration %d/%d", i + 1, config.iterations)

        # --- personality generation ---
        features = generate_personality(api_key, config.model)
        if features is None:
            logger.warning("Skipping iteration %d: personality generation failed", i + 1)
            continue

        # --- build system message ---
        sys_msg = system_prompt + (
            f"Important: Please pretend that you are a human in the game "
            f"with the following features when making the decision:{features}."
        )
        if config.strategic:
            sys_msg += " You are also strategic thinking."

        # --- game agent ---
        agent = ConversableAgent(
            name=config.agent_name,
            system_message=sys_msg,
            llm_config={
                "config_list": agent_llm_config,
                "temperature": config.temperature,
            },
            human_input_mode="NEVER",
        )

        support = ConversableAgent(
            name="agent_support",
            llm_config=False,
            human_input_mode="NEVER",
        )

        try:
            chat_result = support.initiate_chat(
                agent,
                message=user_message,
                max_turns=1,
                clear_history=False,
            )
        except Exception as exc:
            logger.warning("API call failed at iteration %d: %s", i + 1, exc)
            continue

        content = chat_result.chat_history[-1]["content"]
        row = parse_response(content, config.result_keys)
        if row is None:
            logger.warning("Skipping iteration %d: could not parse response", i + 1)
            continue

        data.append(row)
        if config.verbose:
            logger.info("  Result: %s", row)

    if not data:
        raise RuntimeError("All iterations failed — no data collected")

    # --- write CSV ---
    out_dir = config.output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = config.output_path()

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)

    logger.info("Wrote %d rows to %s", len(data), out_path)
