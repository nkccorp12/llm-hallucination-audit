# Audit Report Template

## Executive Summary
3-5 sentences: scope, key findings, recommended actions.

## Scope
- Models tested: [list]
- Prompt set: [adversarial / factuality / domain-specific]
- Test set size: [N]
- Date range: [from / to]

## Methodology
Reference: METHODOLOGY.md

## Test Set
- Categories tested: [list]
- Prompt examples: [3-5 representative ones]

## Metrics
- factual_accuracy_rate
- hallucination_rate
- faithfulness_mean
- refusal_appropriateness
- inter-rater agreement
All with bootstrap 95% CI.

## Results
[Table: model x metric]

## Failure Clusters
[Top 3-5 categories where models hallucinated]

## Recommendations
[Concrete actions for the team]

## Re-test Plan
- Cadence: [e.g. monthly]
- Trigger conditions: [e.g. model upgrade]
