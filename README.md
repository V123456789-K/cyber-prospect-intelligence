# Cyber Prospect Intelligence

A lightweight sales-intelligence MVP for cybersecurity teams. It turns observable internet-facing infrastructure data into explainable prospect signals, deterministic scores, and a focused research workflow.

## Live Application

https://cyber-prospect-intelligence-expmmebpspmyeosfzviynr.streamlit.app/

## What It Does

The MVP is designed around three salesperson-facing use cases:

1. Prospect prioritization using observable infrastructure signals.
2. Prospect investigation by inspecting the evidence behind a score.
3. Sales research assistance using observed signals without treating them as proof of a vulnerability or breach.

Infrastructure observations are treated as research signals, not confirmed security findings.

## Product Flow

Raw infrastructure data
    |
    v
Data normalization
    |
    v
Signal extraction
    |
    v
Deterministic prospect scoring
    |
    +--------------------+
    |                    |
    v                    v
Prospect list      Prospect detail
                         |
                         v
                AI research prompt

## Scoring Approach

The authoritative prospect score is rule-based and explainable.

The scoring logic uses observable fields such as:

- domain information
- hostnames
- organization identity
- ASN
- geographic information
- operating system
- detected technology or module
- reverse DNS information
- network transport

The score is capped at 100.

The scoring logic is implemented in Python and does not depend on an LLM. This makes the score deterministic, reproducible, and auditable.

## Rule vs. LLM Split

Deterministic operations remain in code.

Rules handle:

- parsing
- normalization
- signal extraction
- scoring
- filtering
- ranking
- evaluation

The versioned AI prompt defines a future natural-language interpretation layer for already-observed signals. The current MVP does not call an external LLM.

The AI layer should not invent infrastructure facts, calculate the authoritative score, or claim that an observation proves a vulnerability or breach.

See docs/architecture.md for the architecture and design trade-offs.
## Evaluation

The repository contains a labelled evaluation dataset and a deterministic evaluation harness.

The latest evaluation was run with:

python evals/evaluate.py

Result:

eval_001: PASS (score=70)
eval_002: PASS (score=0)

2/2 evaluation cases passed.

The saved result is available at:

evals/results/latest.json

## Repository Structure

cyber-prospect-intelligence/
|
+-- app/
|   +-- data.py
|   +-- main.py
|   +-- scoring.py
|
+-- data/
|   +-- sample.jsonl
|
+-- docs/
|   +-- planning.md
|   +-- architecture.md
|   +-- how-build.md
|
+-- evals/
|   +-- datasets/
|   |   +-- prospect_evals.json
|   +-- results/
|   |   +-- latest.json
|   +-- evaluate.py
|
+-- prompts/
|   +-- v1/
|       +-- prospect_summary.txt
|
+-- skills/
|   +-- SKILL.md
|
+-- README.md
+-- app.py
+-- inspect_firmable.py
+-- requirements.txt

## Local Setup

Create a virtual environment:

python -m venv .venv

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app/main.py


