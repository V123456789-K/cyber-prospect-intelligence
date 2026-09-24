"""LLM-assisted prospect research, grounded only in deterministic evidence.

The LLM interprets evidence; it does not score prospects or discover facts.
"""

import json
import os
import time
from pathlib import Path

from observability import log_llm_call

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "v2" / "prospect_summary.txt"


def build_evidence(record: dict, score: int, signals: list) -> dict:
    """Build a compact evidence ledger from fields already present in the dataset."""
    allowed = {}
    for key in (
        "ip", "organization", "asn", "country", "city", "domains",
        "hostnames", "os", "transport", "module", "timestamp"
    ):
        value = record.get(key)
        if value not in (None, "", [], {}):
            allowed[key] = value
    return {
        "observable_fields": allowed,
        "deterministic_score": score,
        "deterministic_signals": signals,
    }


def _setting(name: str, default=None):
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st
        return st.secrets.get(name, default)
    except Exception:
        return default


def summarize_prospect(
    record: dict,
    score: int,
    signals: list,
    prompt_version: str = "v2",
) -> dict:
    """Call the configured OpenAI model and return text plus usage metadata."""
    api_key = _setting("OPENAI_API_KEY")
    if not api_key:
        return {
            "status": "missing_api_key",
            "text": "LLM research is not configured. Set OPENAI_API_KEY to enable AI-assisted research.",
            "usage": {},
        }

    try:
        from openai import OpenAI
    except ImportError:
        return {
            "status": "missing_dependency",
            "text": "The OpenAI Python package is not installed.",
            "usage": {},
        }

    try:
        prompt_template = PROMPT_PATH.read_text(encoding="utf-8-sig")
        evidence = build_evidence(record, score, signals)
        prompt = prompt_template.replace(
            "{{evidence_ledger}}",
            json.dumps(evidence, indent=2, ensure_ascii=False),
        )
    except Exception as exc:
        return {
            "status": "prompt_error",
            "text": f"Unable to load the research prompt: {type(exc).__name__}.",
            "usage": {},
        }

    model = _setting("OPENAI_MODEL", "gpt-5-mini")
    started = time.perf_counter()

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(model=model, input=prompt)
        output_text = getattr(response, "output_text", "") or ""
        text = output_text.strip()

        usage_obj = getattr(response, "usage", None)
        input_tokens = getattr(usage_obj, "input_tokens", None) or 0
        output_tokens = getattr(usage_obj, "output_tokens", None) or 0
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)

        log_llm_call({
            "request": {"model": model, "prompt_version": prompt_version},
            "response": {"status": "success"},
            "latency_ms": elapsed_ms,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        })

        return {
            "status": "success",
            "text": text,
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "model": model,
                "latency_ms": elapsed_ms,
            },
        }
    except Exception as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        log_llm_call({
            "request": {"model": model, "prompt_version": prompt_version},
            "response": {"status": "error", "error_type": type(exc).__name__},
            "latency_ms": elapsed_ms,
            "input_tokens": 0,
            "output_tokens": 0,
        })
        return {
            "status": "error",
            "text": f"LLM request failed: {type(exc).__name__}. Check the application logs.",
            "usage": {},
        }
