from __future__ import annotations

import logging

from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


def parse_response(
    content: str,
    response_model: type[BaseModel],
    csv_fields: dict[str, str],
) -> dict[str, str] | None:
    """Parse JSON from an LLM response using Pydantic validation.

    *response_model* is the Pydantic model to validate against.
    *csv_fields* maps ``{csv_column: model_field}``.
    Returns ``None`` when the content cannot be parsed or validation fails.
    """
    try:
        obj = response_model.model_validate_json(content)
    except ValidationError as exc:
        logger.warning("Validation failed: %s — raw content: %s", exc, content[:200])
        return None

    return {col: getattr(obj, field) for col, field in csv_fields.items()}
