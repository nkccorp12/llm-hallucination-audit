# Methodology: Multi-LLM Hallucination Audit

A practical methodology for measuring hallucinations, factuality and
bias in production LLM systems. Designed for B2B engagements where the
output of an audit becomes part of compliance evidence (EU AI Act,
ISO/IEC 23894, ISO 27001, DORA, BaFin context).

---

## Step 1: Define what "hallucination" means for your system

Industry-wide definitions are too vague to be operational. Be specific.

For each system under audit, classify failure modes into four buckets:

| Bucket | Example | Why it matters |
|---|---|---|
| **Factual hallucination** | Model invents a contract clause that does not exist in the source | Direct legal risk |
| **Confident wrong answer** | Model gives correct-sounding but wrong arithmetic | Decision-quality risk |
| **Policy violation** | Answer follows the user but breaks an internal guideline | Brand & compliance risk |
| **Refusal failure** | Model answers a question it should refuse | Liability risk |

Each bucket needs its own scoring rule. Mixing them gives a single
meaningless number.

---

## Step 2: Build a representative test set

Three sources of test items, in order of importance:

1. **Real prompts your users actually sent** (anonymized, deduped). At
   least 30, ideally 100+. These tell you about real-world failure
   modes.
2. **Adversarial prompts** that probe known weak spots:
   leading questions, prompt injection, contradictory context,
   out-of-domain queries.
3. **Ground-truth probes**: questions with a single canonical correct
   answer your auditor knows ahead of time. These quantify factuality
   independent of subjective rubrics.

Together you should reach 80 to 200 items for a meaningful per-week run.

Store as YAML in `prompts/`. Version it in git.

---

## Step 3: Multi-model peer review

Send each test item to N models (we typically use 4: GPT-5, Claude 4.6,
Gemini 2.5 Pro, Mistral Large). Then send the N answers, anonymized as
"Answer A", "Answer B", …, to a fifth model acting as **arbiter**.

Anonymization is non-negotiable: research and our own experiments show
arbiters favor outputs that match their own brand's writing style.
Anonymizing eliminates this bias.

The arbiter scores each answer on:

- **Faithfulness** to source (when source is provided)
- **Internal consistency** (does the answer contradict itself)
- **Inter-answer agreement** (does this answer match what the others say)
- **Refusal appropriateness** (when applicable)

We do not collapse these into a single score. The audit report shows
each dimension separately so the reader can weigh them per business
context.

---

## Step 4: Statistical aggregation

Per test item, you have a 4×N matrix (4 dimensions × N models).

Aggregate by:

- **Per-dimension mean** with **95% bootstrapped confidence intervals**,
  use bootstrap, not normal-theory CIs, because LLM scores are not
  normally distributed
- **Per-model means** to compare providers fairly
- **Inter-rater agreement** between human annotators on a 10 to 20%
  sample to validate the arbiter's scoring

Avoid these traps:

- Using a single arbiter run as ground truth, you need a sample of
  human evaluations to validate it
- Reporting accuracy without CIs, meaningless under small N
- Reporting "average score" across mixed buckets, see Step 1

---

## Step 5: Failure clustering

The most actionable output is a **catalog of failure modes**, not a
single number.

For every test item where the system failed:

1. Tag the failure type (factual / confident-wrong / policy / refusal)
2. Tag the trigger (long context / numeric reasoning / multi-hop /
   adversarial / ambiguous source)
3. Sort failures into clusters of 3+ similar cases
4. For each cluster, the report includes: prompt example, all model
   outputs, why they failed, fix recommendation

Clusters are what your engineering team can actually act on. Single
failures are noise.

---

## Step 6: Re-run protocol

Audits go stale fast. The right cadence:

- **Weekly automatic run** on the same test set after every model update
  or prompt change (whichever comes first)
- **Monthly extension**: add 5 to 10 new test items based on the previous
  month's user complaints
- **Quarterly full review**: re-validate the test set, retire items
  that no longer reflect production traffic

Compare each run against the previous one. Significant deltas
(per-dimension drop > 5pp at 95% CI) trigger investigation.

---

## Step 7: What to put in the compliance report

A defensible report includes:

1. **Scope statement**: what was audited, what was not
2. **Methodology section**: exactly the 6 steps above, with config
3. **Test set statistics**: count, distribution by source/bucket
4. **Per-dimension results** with CIs and inter-rater agreement
5. **Failure catalog** with redacted examples
6. **Recommendations**: prioritized by impact and effort
7. **Re-test plan**: when, how, by whom

This is what an auditor or DPO will ask for. Build the report
template once and reuse it across engagements.

---

## What this methodology does *not* do

- Replace human review of edge cases, the arbiter is good but not
  authoritative
- Catch failure modes you did not test for, coverage is bounded by
  your test set
- Predict failure rate on radically different distributions
- Prove the system is "safe", only that it passed *this* test
  battery on *this* date

Treat audit results as evidence, not certificates.

---

## Recommended reading

- ISO/IEC 23894:2023, *AI Risk Management*
- EU AI Act, esp. high-risk system requirements (Art. 9, 10, 14, 15)
- Liang et al., *Holistic Evaluation of Language Models* (HELM)
- Anthropic, *Constitutional AI*, for arbiter design ideas
- OpenAI, *Evals* framework, for test-set patterns
