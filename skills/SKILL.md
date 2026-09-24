# Cyber Prospect Intelligence Skill

## Purpose
Turn raw internet-infrastructure observations into explainable cybersecurity prospect research signals without presenting them as confirmed security findings.

## Workflow
1. Parse and normalize the supplied record.
2. Extract observable fields and deterministic signals.
3. Calculate the authoritative research-priority score with Python rules.
4. Filter and rank prospects deterministically.
5. Build an evidence ledger containing only observed data.
6. Optionally use the LLM to summarize the evidence ledger.
7. Clearly identify unknowns and the next research question.

## Rule vs. LLM
**Python owns:** parsing, normalization, signal extraction, scoring, filtering, ranking, and evaluation.

**LLM owns:** natural-language synthesis of an already-built evidence ledger.

The LLM must not calculate the authoritative score, invent company facts, assert vulnerabilities or breaches, or infer confirmed buying intent.

## Output contract
Every AI summary should separate observations from hypotheses, identify missing information, and suggest a concrete research question.
