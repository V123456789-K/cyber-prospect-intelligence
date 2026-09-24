# Planning

## Product
Cyber Prospect Intelligence is a lightweight sales-intelligence application for cybersecurity sales research.

## Product workflow
1. Load the runtime internet-infrastructure dataset or the included small sample.
2. Normalize observable records.
3. Extract deterministic signals and calculate an explainable research-priority score.
4. Filter and rank prospects.
5. Inspect the evidence behind a selected prospect.
6. Optionally request an evidence-grounded AI research summary.

## AI-native design
Python remains authoritative for parsing, normalization, signal extraction, scoring, filtering and ranking. The LLM receives a compact evidence ledger and is instructed not to invent facts or claim vulnerability, breach, buying intent or confirmed security need.

## Dataset
The application supports JSONL and Zstandard-compressed .zst JSONL through DATASET_PATH. The large required assignment dataset is intentionally not committed to Git; .gitignore excludes .zst files. The included sample keeps local development reproducible.

## Evaluation
The repository contains deterministic scoring evals plus 20 labelled LLM contract-evaluation cases. The LLM harness validates required output sections and prohibited unsupported claims when an API key is available. Without an API key it validates the labelled dataset structure but does not claim model inference was run.

## Observability and cost
Each LLM request records timestamp, model, prompt version, status, latency, token usage and estimated cost. API keys and full prompts/responses are not logged. Cost rates are configurable with LLM_INPUT_PRICE_PER_MILLION and LLM_OUTPUT_PRICE_PER_MILLION.
