"""Minimal JSONL observability for LLM requests.

Only request metadata, token usage, latency and an estimated cost are stored;
API keys and full prompts/responses are never logged.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parents[1] / "logs" / "llm_calls.jsonl"


def _estimate_cost(input_tokens: int, output_tokens: int) -> float:
    # Prices are configurable because provider/model pricing can change.
    input_price = float(os.getenv("LLM_INPUT_PRICE_PER_MILLION", "0.20"))
    output_price = float(os.getenv("LLM_OUTPUT_PRICE_PER_MILLION", "1.20"))
    return round(
        (input_tokens * input_price + output_tokens * output_price) / 1_000_000,
        8,
    )


def log_llm_call(event: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **event,
    }
    record["estimated_cost_usd"] = _estimate_cost(
        int(record.get("input_tokens", 0)),
        int(record.get("output_tokens", 0)),
    )
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")
