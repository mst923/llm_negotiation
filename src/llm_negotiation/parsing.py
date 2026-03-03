from __future__ import annotations

import json
import logging

logger = logging.getLogger(__name__)


def parse_response(content: str, result_keys: dict[str, str]) -> dict[str, str] | None:
    """Parse JSON from an LLM response and extract the configured keys.

    *result_keys* maps ``{csv_column: json_key}``.
    Returns ``None`` when the content cannot be parsed or a key is missing.
    """
    try:
        data = json.loads(content)
    except (json.JSONDecodeError, TypeError) as exc:
        logger.warning("JSON parse failed: %s — raw content: %s", exc, content[:200])
        return None

    try:
        return {col: data[json_key] for col, json_key in result_keys.items()}
    except KeyError as exc:
        logger.warning("Missing key %s in response: %s", exc, list(data.keys()))
        return None
