# LLM Hallucination Audit

> A practical multi-LLM peer-review framework for measuring hallucinations,
> bias and policy compliance in production B2B language-model systems.

Built and used in production by [DeepThink AI](https://think-agents.ai)
when shipping LLM-based products into regulated environments
(finance, ISO 27001, EU AI Act). Released under MIT so you can drop it
into your own evaluation pipeline.

This repository is **a methodology + working reference code** — not a
turnkey SaaS.

---

## Why this exists

If you ship a single LLM into production, you have a single point of failure
for hallucinations. Standard benchmarks (MMLU, HellaSwag, TruthfulQA) are
generic and overestimate production quality on your real use cases.

We built this because we needed a defensible way to answer three questions
when a B2B client asked us to put GPT or Claude in front of regulated data:

1. **How often does the model hallucinate on our actual queries?**
2. **Does the answer agree with what the other top models would say?**
3. **Can we prove that to a compliance officer?**

The pattern below is what we now use on every client engagement.

---

## The pattern: peer-reviewed multi-model evaluation

```
                  ┌──────────────┐
   prompt  ───┬──▶│  GPT-5       │──┐
              │   ├──────────────┤  │       ┌──────────────┐
              ├──▶│  Claude 4.6  │──┼──────▶│  arbiter     │──▶  scored
              │   ├──────────────┤  │       │  (cross-     │     answer +
              ├──▶│  Gemini 2.5  │──┘       │   review)    │     confidence
              │   ├──────────────┤          └──────────────┘
              └──▶│  Mistral L   │
                  └──────────────┘
```

Three deliberate design choices:

1. **Anonymize before peer review.** When the arbiter sees `Answer A`,
   `Answer B`, `Answer C`, it has no way to play favorites by brand. This
   matters because most "AI judges" leak provider preferences.
2. **Score on disagreement, not majority.** A 3-vs-1 split is more
   informative than a 4-0 consensus — disagreement points at the exact
   places the system is unstable. We surface those for human review.
3. **Track the test set, not the score.** The same input set is replayed
   weekly so drift after model updates becomes visible. A single number
   ("89% accuracy") is meaningless without trajectory.

In our internal data, this pattern reduced acted-on hallucinations by
**~38%** vs. picking a single best model — at the cost of roughly 3.5×
inference spend on audited paths.

---

## Repository contents

```
.
├── README.md               this file
├── METHODOLOGY.md          long-form: how to build a defensible audit
├── prompts/
│   ├── adversarial.yml     30 prompts that reliably break weak systems
│   ├── factuality.yml      40 fact-recall prompts with ground truth
│   └── bias.yml            20 prompts probing demographic disparities
├── eval/
│   ├── runner.py           orchestrates multi-model calls
│   ├── arbiter.py          peer-review scoring with anonymization
│   └── scorer.py           statistical aggregation + confidence intervals
└── examples/
    ├── 01-finance-audit.md a real-world walkthrough (numbers anonymized)
    └── 02-recruiting.md    bias-focused audit walkthrough
```

The runner targets the OpenAI Responses API, the Anthropic Messages API
and the Google Gemini API. Adding Mistral / Llama / open-weights is a
single adapter file — see `eval/runner.py` for the interface.

> Note: prompts/ and eval/ contain the structure and approach. The
> exact prompt sets and scoring rubrics live in our paid engagement
> deliverables, but the public repo is enough to reproduce the
> methodology end-to-end.

---

## What this is *not*

- **Not a benchmark.** Static benchmarks like HELM are great for model
  comparison; this is for evaluating *your specific system* against
  *your specific use cases*.
- **Not certification.** There is no recognized "AI audit standard"
  yet. Our methodology is aligned with ISO/IEC 23894 and the EU AI Act
  high-risk requirements but does not produce a binding seal.
- **Not a guarantee.** A model can pass an audit and still fail on a
  query you never tested. Audits reduce risk, they don't eliminate it.

---

## Use it in your own work

1. **Fork or copy** the prompt structures in `prompts/`
2. **Replace** the example test items with your domain (5–10 prompts is
   enough to start; 50+ is enterprise-grade)
3. **Run** `eval/runner.py` against the systems you actually ship
4. **Re-run weekly** to catch drift

If you'd rather have us run it for you (DACH B2B, German + English,
ISO-aligned), see [services/ki-audit-halluzinationen](
https://think-agents.ai/de/services/ki-audit-halluzinationen).

---

## Citation / academic use

If you use this methodology in a paper, blog post, or compliance
documentation, please cite:

> Bäumler, F. (2026). *LLM Hallucination Audit: A multi-model
> peer-review framework for production B2B systems.* DeepThink AI.
> https://github.com/nkccorp12/llm-hallucination-audit

---

## License

MIT. Use freely. Attribution appreciated.

## Maintainer

Fabian Bäumler — Principal Consultant, DeepThink AI
[think-agents.ai](https://think-agents.ai) ·
[LinkedIn](https://www.linkedin.com/in/baeumler/)

If you build something useful on top of this, open an issue with a link.
We'd love to see it.
