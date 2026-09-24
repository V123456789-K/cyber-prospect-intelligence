# How I Build

## Development Loop

I used an iterative AI-assisted development workflow: break the take-home
requirements into small deliverables, implement the smallest useful product
slice, run the application and evaluation harness, inspect the results, and
then refine the repository and documentation.

The development loop was:

1. Translate the take-home requirements into product, engineering, evaluation
   and documentation deliverables.
2. Inspect the infrastructure dataset and identify observable prospect signals.
3. Implement normalization and deterministic scoring first.
4. Build the Streamlit prospecting and investigation interface.
5. Add the skills definition, versioned research prompt and labelled
   evaluation dataset.
6. Run the evaluation harness and verify the scoring behavior.
7. Deploy the application and verify that the hosted workflow works.
8. Audit the repository against the original take-home requirements.
9. Refine documentation and explicitly document the rule-versus-LLM boundary.

## Where AI Saved Time

AI assistance was useful for:

- Breaking the take-home requirements into concrete implementation tasks.
- Scaffolding and reviewing repository structure.
- Identifying edge cases in the scoring and evaluation logic.
- Reviewing documentation for consistency with the implementation.
- Iterating on the Streamlit workflow and repository artifacts.

## Where AI Cost More Than Manual Work

For small repository operations and simple text edits, manual terminal commands
can be faster than asking an AI assistant.

AI-generated explanations also require verification because plausible-sounding
text can introduce unsupported assumptions. For that reason, the authoritative
prospect score remains deterministic Python rather than an LLM output.

## Known Weakness

The current evaluation set is intentionally small. It verifies the deterministic
score range, expected observable signals and prohibited unsupported claims, but
it does not provide broad coverage of the full source dataset or evaluate
large-scale human judgement of sales-summary quality.

A production version should expand the labelled evaluation set to cover missing
fields, unusual records, conflicting signals and evidence-grounding quality.

## AI-Native Design

The repository includes:

- `skills/SKILL.md` for the prospect-intelligence workflow.
- `prompts/v1/prospect_summary.txt` for a versioned AI research-summary
  contract.
- `evals/` for repeatable evaluation of the deterministic evidence/scoring
  layer.

The current MVP does not require an external LLM API. The versioned prompt
defines an explicit extension point for future evidence-grounded summaries
without allowing a model to become the authoritative scoring mechanism.
