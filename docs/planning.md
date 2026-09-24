# Planning

## Product

Cyber Prospect Intelligence is a lightweight sales-intelligence application
for cybersecurity teams.

## Problem

Security sales teams may have large amounts of internet-facing infrastructure
data but need a faster way to identify organizations worth researching.

## Chosen Use Cases

### 1. Prospect prioritization

Rank observable infrastructure records using deterministic signals.

### 2. Prospect investigation

Show the evidence behind an individual prospect score.

### 3. Sales research assistance

Provide a structured, evidence-grounded prompt for generating a concise
research explanation from observed signals.

## Why These Use Cases

They demonstrate a complete workflow from raw infrastructure data to an
actionable sales research experience without requiring unsupported assumptions
about a company's security posture.

## MVP Scope

- Dataset sampling
- Data normalization
- Signal extraction
- Explainable scoring
- Prospect filtering
- Prospect detail view
- Versioned AI research prompt
- Evaluation dataset
- Deterministic evaluation harness

## Current Implementation Boundary

The current MVP implements the data processing, signal extraction,
deterministic scoring, filtering and prospect investigation workflow.

The versioned prompt in `prompts/v1/prospect_summary.txt` defines the
AI-assisted research-summary contract, but the current application does not
make external LLM API calls.

This keeps the submitted MVP runnable without an external model provider or
API key while preserving a clear extension point for an LLM integration.

## Success Criteria

A salesperson should be able to:

1. Filter prospects by country and minimum score.
2. Prioritize records using an explainable score.
3. Inspect the observable evidence contributing to the score.
4. Understand which additional information would need to be researched
   before making a sales conclusion.

The system must not present infrastructure observations as proof of a
vulnerability, breach or confirmed security need.

## Cost Model

The current scoring pipeline has zero LLM inference cost because scoring and
filtering are deterministic Python operations.

A future LLM integration should call the model only when a user requests an
individual prospect explanation rather than processing the entire dataset.

This keeps inference costs proportional to user-triggered research activity.

## Trade-offs

A deterministic scoring model is easier to audit, reproduce and test, but it
may miss contextual relationships that a language model could identify.

An LLM could improve natural-language research summaries, but would introduce
API cost, latency and hallucination risk.

The MVP therefore keeps the authoritative scoring logic outside the LLM and
treats the versioned prompt as an explicit integration boundary.
