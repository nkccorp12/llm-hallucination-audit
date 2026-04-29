# Research Roadmap

## 1. Mission Statement

This repository exists to publish a public methodology for evaluating production AI decision systems. The goal is to turn a private audit pattern into a reusable, inspectable, and citable research asset that other teams can replicate on small, documented prompt sets. It is an evidence framework for real deployment behavior, not a certification program.

## 2. Research Question

On a small, domain-specific, documented prompt set, does a multi-LLM peer-review council show more stable outputs and fewer critical failure modes than single-model baselines?

This question is tested under controlled conditions with shared prompts, shared scoring rules, anonymized outputs, and transparent reporting of uncertainty.

## 3. Scope And Non-Goals

### In Scope

- 35 to 45 anonymized prompts derived from real production usage where possible
- 3 prompt categories with explicit labels and source notes
- 5 systems compared: 4 single-model baselines plus 1 multi-LLM council system
- A failure taxonomy covering factual hallucination, confident wrong answer, policy violation, and refusal failure
- Faithfulness scoring on a 0 to 1 scale with model and system level aggregation
- Bootstrap 95% confidence intervals for all core metrics
- A technical report that documents methodology, limitations, and findings

### Non-Goals

- Any certification claim about safety, compliance, or legal adequacy
- Any claim that one provider is the universal "best model"
- Any generic benchmark intended to represent all domains or all tasks
- Any opinion-content evaluation where ground truth or review criteria are inherently subjective
- Any hidden or proprietary scoring process that cannot be explained in the report

## 4. Four-Week Phases

### Week 1 - Setup

**Goal:** establish the evaluation harness, test set, and paper skeleton.

**Artifacts**

- `eval/adapters/council_api.py`
  - Implement the adapter that calls the `ai-council-whitelabel` API endpoint.
  - Normalize response payloads into the same schema used by single-model runs.
  - Preserve stage metadata needed for later appendix examples.
- `eval/adapters/single_model.py`
  - Implement provider adapters for GPT, Claude, Gemini, and Mistral.
  - Standardize request config, retry behavior, response parsing, and refusal tagging.
  - Ensure the output shape matches the council adapter for fair comparison.
- `prompts/production_anonymized.yml`
  - Curate 35 to 45 anonymized prompts.
  - Split prompts into 3 labeled categories such as factual lookup, policy-sensitive reasoning, and refusal-required cases.
  - Include prompt IDs, category, source notes, and expected scoring mode.
- `paper/outline.md`
  - Draft section structure for the report.
  - Lock core claims, hypotheses, and limitations before results are generated.
  - Add an appendix placeholder for anonymized stage artifacts and failure examples.

**Exit Criteria**

- Both adapter paths produce a shared result schema.
- The prompt set is versioned and reviewed for anonymization quality.
- The paper outline contains the exact hypotheses that the later report will test.

### Week 2 - Run And Score

**Goal:** execute comparison runs, score outputs, and quantify uncertainty.

**Artifacts**

- `eval/scorer.py`
  - Compute `factual_accuracy_rate`, `hallucination_rate`, `faithfulness_mean`, and `refusal_appropriateness`.
  - Support per-prompt labels, per-system summaries, and exportable metric tables.
  - Keep scoring rules explicit and traceable to prompt metadata.
- `eval/bootstrap.py`
  - Compute non-parametric bootstrap 95% confidence intervals for each metric.
  - Support paired comparisons where the same prompt set is used across systems.
  - Record bootstrap settings so the report can state the method precisely.
- `results/2026-05-council-vs-singles/`
  - Store raw outputs, normalized responses, scoring outputs, and summary tables.
  - Separate run metadata from scored results so analyses are reproducible.
  - Include a manifest that identifies prompt set version, model versions if known, and run date.
- `paper/figures/`
  - Generate charts for metric comparison, confidence intervals, and failure distribution.
  - Produce at least one figure for metric comparison and one for failure taxonomy breakdown.
- `tests/test_scorer.py`
  - Add unit tests for metric calculations, edge cases, and CI output shape.
  - Cover zero-denominator handling, refusal-opportunity counting, and missing-score behavior.

**Exit Criteria**

- All five systems have completed comparable runs on the same prompt set.
- Every reported metric includes a bootstrap 95% CI.
- The scorer test suite covers the main metric logic and passes locally.

### Week 3 - Report

**Goal:** convert results into a citable technical report and release package.

**Artifacts**

- `paper/technical-report.md`
  - Write the v0.9 draft with abstract, research question, methodology, results, limitations, and next steps.
  - Use precise language about evidence, uncertainty, and domain limits.
  - Include the council system as a case study, not as a universal winner claim.
- `paper/figures/*.png`
  - Finalize publication-quality figures with stable labels and captions.
  - Ensure figure filenames match references in the report.
- `CITATION.cff`
  - Update to v0.2 with the new report and release metadata.
  - Ensure citation fields match the planned release tag and title.
- `.zenodo.json`
  - Add metadata for DOI deposit and archive description.
  - Include keywords for evaluation, hallucination, and AI audit methodology.
- `CHANGELOG.md`
  - Add a v0.2.0 entry that summarizes the new methodology, report, and artifacts.

**Exit Criteria**

- The report is complete enough to circulate as v0.9.
- All cited files exist and can be mapped to a release artifact.
- DOI deposit metadata is ready before the release is cut.

### Week 4 - Publish And Distribute

**Goal:** publish the package, mint a DOI, and prepare external distribution materials.

**Artifacts**

- `v0.2.0` GitHub Release
  - Attach the technical report and link the reproducibility artifacts.
  - Use release notes consistent with `CHANGELOG.md`.
- Zenodo DOI mint
  - Archive the tagged release and verify the metadata matches the citation file.
- `docs/blog/`
  - Draft 3 posts:
  - `docs/blog/01-methodology-overview.md`
  - `docs/blog/02-council-vs-single-models.md`
  - `docs/blog/03-how-to-run-your-own-audit.md`
- `docs/talks/agentcon-2026.md`
  - Draft a talk deck outline with narrative, figures, and speaker notes.
- `docs/distribution/outreach.md`
  - Create an outreach checklist covering launch channels, target communities, and follow-up actions.

**Exit Criteria**

- The repository has a public tagged release and DOI-backed citation path.
- Distribution materials exist in the repo and reflect the same claims as the report.
- External messaging does not overstate results beyond the measured scope.

## 5. Metrics Definition

All reported metrics must be computed per system on the same prompt set and reported with bootstrap 95% confidence intervals.

### `factual_accuracy_rate`

**Definition**

The share of prompts with a verifiably correct answer among prompts that have a defined canonical or document-grounded truth condition.

**Formula**

`factual_accuracy_rate = correct_answers / factual_scored_prompts`

**Reference**

Grounded in the repository's factuality audit framing in `METHODOLOGY.md`, Step 2 and Step 4.

### `hallucination_rate`

**Definition**

The share of prompts where the output contains a material unsupported claim, invented fact, invented citation, or invented document content under the active scoring rules.

**Formula**

`hallucination_rate = hallucination_failures / scored_prompts`

**Reference**

Aligned with the failure taxonomy in `METHODOLOGY.md`, especially factual hallucination and confident wrong answer categories.

### `faithfulness_mean`

**Definition**

The mean faithfulness score across scored prompts, where each prompt receives an arbiter score in `[0, 1]` for agreement with the provided source material or documented ground truth.

**Formula**

`faithfulness_mean = (sum of faithfulness scores) / faithfulness_scored_prompts`

**Reference**

Aligned with `METHODOLOGY.md`, Step 3, where faithfulness to source is a primary scoring dimension.

### `refusal_appropriateness`

**Definition**

The share of refusal-opportunity prompts where the system refused when refusal was correct, or answered when answering was correct, according to prompt labels and scoring guidance.

**Formula**

`refusal_appropriateness = correctly_handled_refusal_opportunities / total_refusal_opportunities`

**Reference**

Aligned with the refusal failure bucket in `METHODOLOGY.md`, Step 1 and Step 3.

### `inter_rater_agreement`

**Definition**

Agreement between human raters on a spot-checked subset of outputs used to validate the arbiter scoring process.

**Formula**

`inter_rater_agreement = Krippendorff alpha(human ratings)`

**Reference**

Aligned with `METHODOLOGY.md`, Step 4, which recommends human evaluation on a 10 to 20 percent sample to validate arbiter judgments.

### Confidence Intervals

For every metric above, report:

- point estimate
- bootstrap 95% CI
- denominator used
- any exclusion rules applied

The bootstrap implementation should live in `eval/bootstrap.py`, and the scored metric tables should retain enough metadata to reconstruct each estimate.

## 6. Repo Connection To The Council

```text
Council (ai-council-whitelabel) provides:
- API endpoint for orchestrated multi-LLM responses
- Stage 1+2+3 pipeline output
- Anonymized stage artifacts for paper appendix

Audit (llm-hallucination-audit) provides:
- Standardized evaluation harness
- Published methodology
- Comparison framework
- Citable artifact (DOI)
```

Operationally, the council repo is the production case-study system and this repo is the public research layer around it. The audit repo should never depend on private implementation details beyond the documented API and approved anonymized artifacts.

## 7. Risks And Mitigations

### Insufficient Real Data

- Risk: the prompt set is too synthetic to say anything useful about real production behavior.
- Mitigation: require at least 15 prompts drawn from real usage, anonymized and documented inside `prompts/production_anonymized.yml`.

### Scope Creep

- Risk: the repo tries to become a broad benchmark, toolkit, and paper at the same time.
- Mitigation: one week, one deliverable cluster; defer anything that does not unblock the next named artifact.

### Overclaim

- Risk: readers interpret the report as proof that a system is safe or certified.
- Mitigation: use "evidence framework" language throughout `paper/technical-report.md`, release notes, and blog drafts; explicitly reject certification framing.

### Arbiter Bias

- Risk: the arbiter favors certain answer styles or provider signatures.
- Mitigation: rotate the arbiter where feasible, anonymize all compared outputs, and validate 10 to 20 percent of scored items with human spot checks.

### Unfair Council Comparison

- Risk: the council appears better only because it uses more model calls, higher latency, or more cost.
- Mitigation: report cost and latency tradeoffs transparently alongside quality metrics and explain that comparison is about output stability versus operational overhead.

## 8. Definition Of Done

- `RESEARCH_ROADMAP.md` exists and matches the repo strategy.
- `eval/adapters/council_api.py` exists and can call the council endpoint.
- `eval/adapters/single_model.py` exists and supports GPT, Claude, Gemini, and Mistral.
- `prompts/production_anonymized.yml` contains 35 to 45 prompts across 3 categories.
- At least 15 prompts come from real production traffic after anonymization.
- `eval/scorer.py` computes all four core outcome metrics.
- `eval/bootstrap.py` computes bootstrap 95% CIs for every reported metric.
- `tests/test_scorer.py` covers metric logic and passes.
- `results/2026-05-council-vs-singles/` contains raw outputs, scored outputs, and summary tables for all 5 systems.
- `paper/technical-report.md` reaches v0.9 draft quality with methods, results, limitations, and appendix references.
- `paper/figures/` contains finalized publication figures used by the report.
- `CITATION.cff`, `.zenodo.json`, and `CHANGELOG.md` are updated for v0.2.0.
- A public `v0.2.0` release is tagged and archived in Zenodo.
- A DOI is minted and reflected in the citation metadata.
- `docs/blog/` contains 3 distribution drafts.
- `docs/talks/agentcon-2026.md` exists.
- `docs/distribution/outreach.md` exists.
- Public messaging consistently states that the artifact is methodology evidence, not certification.

## 9. Open Questions

- Which domain should anchor the first published prompt set: finance, legal, compliance, procurement, or another domain?
- What anonymization standard is acceptable for real prompts and stage artifacts before they can be published in `prompts/` and the paper appendix?
- Which exact four single-model baselines should be locked for the first report, including version naming conventions?
- What council API response fields can be exposed publicly without revealing private production implementation details?
- Should the first release report cost and latency as primary tables or as appendix material only?
