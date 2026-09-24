# How I Build

## Development loop
1. Convert the take-home requirements into product, engineering, evaluation and documentation deliverables.
2. Inspect the existing repository before changing it.
3. Keep parsing, normalization, signal extraction and scoring deterministic.
4. Build the smallest Streamlit workflow exposing evidence behind prioritization.
5. Add a versioned AI prompt and compact evidence ledger.
6. Add labelled eval cases for grounding and unsupported-claim safety.
7. Add request-level observability and configurable cost estimation.
8. Run deterministic tests first, then model-backed evaluation only when credentials are configured.
9. Audit the repository and hosted deployment separately; never mark an external integration as tested without exercising it.

## Verification principle
Distinguish implemented, locally tested, and externally verified. A missing API key or unavailable large dataset is recorded as an untested integration rather than a passing test.
