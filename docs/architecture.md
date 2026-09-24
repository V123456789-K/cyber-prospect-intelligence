# Architecture

Dataset (.jsonl / .zst) -> Python normalization -> observable evidence + deterministic signals -> rule-based research-priority score -> prospect list / investigation -> evidence ledger -> optional LLM -> grounded summary.

## Rule vs LLM
Python owns parsing, normalization, signal extraction, scoring, filtering, ranking and evaluation. These operations are deterministic and auditable.

The LLM owns only natural-language synthesis of an evidence ledger. It does not calculate the authoritative score, add external facts, or establish vulnerability, breach, compromise, buying intent or confirmed security need.

## Data boundary
DATASET_PATH selects the runtime dataset. .zst files are streamed through Zstandard rather than requiring the compressed file to be committed.

## Observability
LLM metadata is appended to logs/llm_calls.jsonl: model, prompt version, status, latency, token counts and estimated cost. Secrets and full model content are excluded.

## Trade-offs
Deterministic scoring improves reproducibility but is a research-priority heuristic, not a claim about actual customer need. LLM summaries improve usability but add latency, cost and hallucination risk, so the evidence ledger and prompt contract constrain the model.
