# How We Build

## Development Loop

The development process followed a short iterative loop:

1. Inspect the source data.
2. Build a small working sample rather than loading the full dataset.
3. Implement deterministic processing and scoring.
4. Run the application locally.
5. Inspect errors and iterate.
6. Add AI-specific skills, prompts and evaluation cases.
7. Document architecture and trade-offs.
8. Package the project for GitHub and deployment.

## Agentic Tools

AI assistance was used for project scaffolding, implementation ideas,
debugging, documentation structure and prompt/evaluation design.

## Where AI Saved Time

AI was particularly useful for generating initial project structure,
boilerplate code and documentation templates, allowing more time to focus
on product decisions.

## Where AI Cost More Than Manual Work

For small debugging issues, repeatedly changing generated code can sometimes
take longer than inspecting the actual file and error directly. The lesson
was to validate individual components before making additional changes.

## Known Weakness

The current scoring model is an MVP heuristic rather than a validated
measure of commercial buying intent. A production system should validate
signals against labelled sales outcomes and continuously monitor precision,
false positives and signal drift.
