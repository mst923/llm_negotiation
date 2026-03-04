"""Analyze how often agents mention the proposer being a computer program in their reasoning.

Uses an LLM (gpt-5.2) to classify each reasoning text.

Usage:
    uv run python analysis/run_computer_mention_analysis.py
"""

import csv
import json
import logging
import os
import pathlib
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RESULTS_DIR = pathlib.Path("results")
OUTPUT_DIR = pathlib.Path("analysis/computer_mention")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PERSONAS = ["normal", "strategic", "greedy", "benevolent"]
CLASSIFIER_MODEL = "gpt-5.2"
WORKERS = 20

SYSTEM_PROMPT = """\
You are a text classifier. Given a reasoning text from a game participant who received an unfair proposal from a computer program, determine whether the participant explicitly mentions or references the fact that the proposer is a computer program / algorithm / machine (not a human) as part of their reasoning for their decision.

Classify as:
- "yes" if the reasoning explicitly mentions the proposer being a computer/program/algorithm/machine and uses this fact as part of their justification
- "no" if the reasoning does not mention the proposer being a computer, or only discusses fairness/money without referencing the computer aspect

Respond with a single JSON object: {"classification": "yes" or "no", "evidence": "brief quote or explanation"}
"""


def classify_reason(client: OpenAI, reason: str, idx: int) -> dict:
    """Classify a single reasoning text."""
    try:
        resp = client.chat.completions.create(
            model=CLASSIFIER_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Reasoning text:\n{reason}"},
            ],
            response_format={"type": "json_object"},
        )
        content = resp.choices[0].message.content
        result = json.loads(content)
        return {"idx": idx, "classification": result.get("classification", "error"), "evidence": result.get("evidence", "")}
    except Exception as exc:
        logger.warning("Classification failed for idx %d: %s", idx, exc)
        return {"idx": idx, "classification": "error", "evidence": str(exc)}


def analyze_model(game_model: str) -> pd.DataFrame:
    """Load computer-condition data for a given game model and classify all reasons."""
    logger.info("=" * 60)
    logger.info("Analyzing model: %s", game_model)
    logger.info("=" * 60)

    dfs = []
    for persona in PERSONAS:
        path = RESULTS_DIR / "unfair_receiver_computer" / persona / game_model / "unfair_receiver_1.csv"
        if path.exists():
            tmp = pd.read_csv(path)
            dfs.append(tmp)
        else:
            logger.warning("Not found: %s", path)

    if not dfs:
        logger.error("No data found for model %s", game_model)
        return pd.DataFrame()

    df = pd.concat(dfs, ignore_index=True)
    df["decision"] = df["decision"].str.strip().str.lower()
    logger.info("Total rows: %d", len(df))

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    results = []
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = {
            executor.submit(classify_reason, client, row["reason"], idx): idx
            for idx, row in df.iterrows()
        }
        for future in as_completed(futures):
            results.append(future.result())

    result_df = pd.DataFrame(results).set_index("idx").sort_index()
    df["mentions_computer"] = result_df["classification"]
    df["evidence"] = result_df["evidence"]

    # Save detailed results
    out_path = OUTPUT_DIR / f"computer_mention_{game_model}.csv"
    df.to_csv(out_path, index=False)
    logger.info("Saved detailed results to %s", out_path)

    return df


def print_summary(df: pd.DataFrame, game_model: str) -> None:
    """Print summary statistics."""
    print(f"\n{'=' * 60}")
    print(f"Summary: {game_model}")
    print(f"{'=' * 60}")

    total = len(df)
    mentions = (df["mentions_computer"] == "yes").sum()
    print(f"\nOverall: {mentions}/{total} ({mentions/total:.1%}) mention computer as part of reasoning")

    # By persona
    print(f"\n--- By Persona ---")
    for persona in PERSONAS:
        sub = df[df["persona"] == persona]
        n = len(sub)
        m = (sub["mentions_computer"] == "yes").sum()
        print(f"  {persona:12s}: {m:3d}/{n} ({m/n:.1%})")

    # By decision
    print(f"\n--- By Decision ---")
    for decision in ["accept", "reject"]:
        sub = df[df["decision"] == decision]
        n = len(sub)
        if n == 0:
            continue
        m = (sub["mentions_computer"] == "yes").sum()
        print(f"  {decision:12s}: {m:3d}/{n} ({m/n:.1%})")

    # By persona × decision
    print(f"\n--- By Persona × Decision ---")
    cross = df.groupby(["persona", "decision"]).apply(
        lambda g: pd.Series({
            "n": len(g),
            "mentions": (g["mentions_computer"] == "yes").sum(),
            "rate": (g["mentions_computer"] == "yes").mean(),
        })
    )
    cross["rate"] = cross["rate"].map("{:.1%}".format)
    print(cross.to_string())

    # By gender
    print(f"\n--- By Gender ---")
    for gender in sorted(df["gender"].unique()):
        sub = df[df["gender"] == gender]
        n = len(sub)
        m = (sub["mentions_computer"] == "yes").sum()
        print(f"  {gender:12s}: {m:3d}/{n} ({m/n:.1%})")


def main():
    models = ["gpt-5-mini", "gpt-4o-mini-2024-07-18"]

    all_results = {}
    for model in models:
        df = analyze_model(model)
        if not df.empty:
            all_results[model] = df
            print_summary(df, model)

    # Comparison
    if len(all_results) == 2:
        print(f"\n{'=' * 60}")
        print("Model Comparison")
        print(f"{'=' * 60}")
        for model, df in all_results.items():
            total = len(df)
            mentions = (df["mentions_computer"] == "yes").sum()
            print(f"  {model}: {mentions}/{total} ({mentions/total:.1%})")


if __name__ == "__main__":
    main()
