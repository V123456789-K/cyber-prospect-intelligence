# Architecture

## Flow

Raw .zst dataset
        |
        v
Streaming extraction
        |
        v
JSONL working dataset
        |
        v
Python normalization
        |
        v
Deterministic signal engine
        |
        v
Prospect scoring
        |
        +------------------+
        |                  |
        v                  v
   Streamlit UI       LLM summary
        |                  |
        +--------+---------+
                 |
                 v
             Sales user

## Rule vs LLM Split

Rules are used for parsing, normalization, signal extraction, scoring,
filtering and ranking because these operations need to be deterministic,
auditable and inexpensive.

The LLM is used only for natural-language interpretation of already observed
signals.

The LLM does not determine the underlying score.

## Cost Model

The scoring pipeline operates without an LLM.

LLM calls are made only when a user requests a prospect explanation. This
keeps inference costs proportional to actual usage rather than processing
the entire dataset with an LLM.

## Trade-offs

A deterministic scoring model is easier to audit but may miss contextual
relationships that a language model could identify.

An LLM can provide better explanations but introduces cost, latency and
hallucination risk.

The MVP therefore keeps the authoritative scoring logic outside the LLM.
