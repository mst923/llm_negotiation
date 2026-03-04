from __future__ import annotations

import csv
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from autogen import ConversableAgent
from dotenv import load_dotenv

from .config import PERSONA_PROMPTS, GameConfig
from .parsing import parse_response
from .personality import generate_personality

logger = logging.getLogger(__name__)

PERSONALITY_KEYS = ["persona", "proposal_source", "region", "name", "age", "gender", "occupation"]


def _run_single_iteration(
    iteration: int,
    config: GameConfig,
    api_key: str,
) -> dict[str, str] | None:
    """Run a single game iteration. Returns a CSV row dict or None on failure."""
    logger.info("Iteration %d/%d", iteration, config.iterations)

    # --- personality generation ---
    personality = generate_personality(api_key, config.effective_personality_model)
    if personality is None:
        logger.warning("Skipping iteration %d: personality generation failed", iteration)
        return None

    # --- build system message ---
    features = ", ".join(f"{k}: {v}" for k, v in personality.items())
    sys_msg = config.system_prompt + (
        f"Important: Please pretend that you are a human in the game "
        f"with the following features when making the decision:{features}."
    )
    sys_msg += PERSONA_PROMPTS[config.persona]

    agent_llm_config = [
        {
            "model": config.model,
            "api_key": api_key,
            "response_format": config.response_format,
        }
    ]

    # --- game agent ---
    game_llm_extra: dict = {}
    if "gpt-5" not in config.model:
        game_llm_extra["temperature"] = config.temperature

    agent = ConversableAgent(
        name=config.agent_name,
        system_message=sys_msg,
        llm_config={
            "config_list": agent_llm_config,
            **game_llm_extra,
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
            message=config.prompt,
            max_turns=1,
            clear_history=False,
        )
    except Exception as exc:
        logger.warning("API call failed at iteration %d: %s", iteration, exc)
        return None

    content = chat_result.chat_history[-1]["content"]
    row = parse_response(content, config.response_model, config.csv_fields)
    if row is None:
        logger.warning("Skipping iteration %d: could not parse response", iteration)
        return None

    row = {"persona": config.persona, "proposal_source": config.proposal_source, **personality, **row}
    if config.verbose:
        logger.info("  Result: %s", row)
    return row


def run_experiment(config: GameConfig) -> None:
    """Run *config.iterations* rounds of the configured game and write CSV."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment or .env")

    data: list[dict[str, str]] = []

    with ThreadPoolExecutor(max_workers=config.workers) as executor:
        futures = {
            executor.submit(_run_single_iteration, i + 1, config, api_key): i + 1
            for i in range(config.iterations)
        }
        for future in as_completed(futures):
            iteration = futures[future]
            try:
                row = future.result()
            except Exception as exc:
                logger.warning("Iteration %d raised: %s", iteration, exc)
                continue
            if row is not None:
                data.append(row)

    if not data:
        raise RuntimeError("All iterations failed — no data collected")

    # --- write CSV ---
    out_dir = config.output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = config.output_path()

    fieldnames = PERSONALITY_KEYS + list(config.csv_fields.keys())
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    logger.info("Wrote %d rows to %s", len(data), out_path)
