# Prospect Intelligence Skill

## Purpose

Convert raw internet-infrastructure observations into useful cybersecurity
prospecting signals while keeping scoring deterministic and explainable.

## Workflow

1. Parse the source record.
2. Normalize organization, domain, hostname, location, ASN and technology fields.
3. Extract observable infrastructure signals.
4. Apply deterministic scoring rules.
5. Produce an evidence-backed prospect profile.
6. Use an LLM only to summarize the evidence for a salesperson.
7. Never invent company facts, technologies, incidents, or business needs.

## Rule vs LLM

Rules handle:
- Data parsing
- Normalization
- Signal extraction
- Scoring
- Filtering
- Ranking

LLM handles:
- Natural-language summaries
- Sales research suggestions
- Evidence explanation

## Output Requirements

Every AI-generated explanation must:
- Refer only to observed data.
- Clearly distinguish observations from hypotheses.
- Avoid unsupported claims.
- Identify missing information when evidence is insufficient.
