# Cyber Prospect Intelligence

A lightweight sales-intelligence MVP for cybersecurity teams. It turns observable internet-facing infrastructure data into explainable prospect signals, deterministic research-priority scores, and an evidence-grounded AI research workflow.

## Live Application

https://cyber-prospect-intelligence-expmmebpspmyeosfzviynr.streamlit.app/

## What It Does

1. Prioritizes prospects using observable infrastructure signals.
2. Filters and investigates prospects by country and research-priority score.
3. Shows the deterministic evidence behind each score.
4. Optionally generates an LLM-assisted research summary grounded only in the observed evidence ledger.

The score is a **research-priority heuristic**, not a claim of cybersecurity need, buying intent, vulnerability, compromise, or breach.

## Rule vs. LLM Split

**Python owns:** parsing, normalization, signal extraction, scoring, filtering, ranking, and evaluation.

**LLM owns only:** natural-language synthesis of the supplied evidence ledger, suggested research questions, and separation of observed facts from possible interpretation and missing information.

The LLM does not calculate the authoritative score and is instructed not to invent company facts or assert vulnerabilities, breaches, compromise, or confirmed buying intent.

## Dataset Support

The application supports ordinary JSONL and Zstandard JSONL (.zst). Set DATASET_PATH to the dataset location. The source .zst file is intentionally not committed because large source datasets are excluded by .gitignore.

## AI Research Assistant

The app uses the OpenAI Responses API when OPENAI_API_KEY is configured. The default model is gpt-5-mini; OPENAI_MODEL can override it.

If no API key is configured, the application continues to work as a deterministic prospecting tool and reports that AI research is not configured.

The prompt is versioned at prompts/v2/prospect_summary.txt.

## Observability and Cost Monitoring

Each LLM call records a compact runtime trace in logs/llm_calls.jsonl containing UTC timestamp, model, prompt version, status, latency, input/output tokens, and estimated cost. Rates are configurable with LLM_INPUT_PRICE_PER_MILLION and LLM_OUTPUT_PRICE_PER_MILLION. These are estimates, not provider billing records. Full prompts, responses, and API keys are not logged.

## Evaluation

Run python evals/evaluate.py for the deterministic evaluation.

Run python evals/evaluate_llm.py for the LLM harness. evals/datasets/llm_evals.json contains 20 labelled cases covering sparse, partial, mixed, and full evidence. The harness validates the dataset contract, score bounds, four required response sections, and forbidden-claim safety. Without OPENAI_API_KEY it performs contract validation only and does not claim model results.

## Repository Structure

cyber-prospect-intelligence/
|-- app/ (data.py, main.py, llm.py, observability.py, scoring.py)
|-- data/ (sample.jsonl)
|-- docs/ (planning.md, architecture.md, how-build.md)
|-- evals/ (datasets, results, evaluate.py, evaluate_llm.py)
|-- prompts/ (v1 and v2)
|-- skills/ (SKILL.md)
|-- README.md
|-- requirements.txt

## Local Setup

python -m venv .venv
pip install -r requirements.txt
streamlit run app/main.py

For AI, configure OPENAI_API_KEY and optionally OPENAI_MODEL. For Streamlit hosting, use the app Secrets settings; never commit keys.