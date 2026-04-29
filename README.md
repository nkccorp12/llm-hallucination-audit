# LLM Hallucination Audit

Public reference implementation for LLM hallucination evaluation:
adversarial prompts, multi-LLM arbiter, factuality scoring.
By DeepThink AI ( https://think-agents.ai ).

This repository is intended as a compact public reference asset. It shows
the evaluation structure, runnable core code, and the methodology used to
audit LLM behavior in a way that is readable, reusable, and easy to cite.
It is not presented as a finished product, certification, or benchmark.

## What this repo contains today

- Prompt sets: `prompts/adversarial.yml`, `prompts/factuality.yml`
- Runnable code: `eval/runner.py`, `eval/arbiter.py`
- Methodology document: `METHODOLOGY.md`

The current scope is deliberately small. The goal is to make the public
version honest and inspectable, while leaving room for stricter testing,
reporting, and packaging in later phases.

## Roadmap

- pytest test suite (Phase 1)
- GitHub Actions CI (Phase 1)
- Faithfulness scorer with bootstrap CIs (Phase 2)
- Anonymized finance-audit case (Phase 2)
- Streamlit demo + v0.2.0 release (Phase 3)
- Bias audit prompts (later)

## Quickstart

1. Clone the repo
2. Install dependencies (`requirements.txt` coming in Phase 1)
3. Set API keys (Anthropic, OpenAI)
4. Run: `python -m eval.runner prompts/factuality.yml`

You can adapt the prompt YAML files to your own domain, replay the same test
set across models, and inspect the arbiter output as a starting point for a
repeatable audit workflow.

## Methodology

See `METHODOLOGY.md` for the audit approach, model arbiter logic, and metric
definitions.

## License

MIT, see `LICENSE`.

## Citation

See `CITATION.cff`.

## About

Built by Fabian Bäumler, Co-Founder of DeepThink AI.

- Site: https://think-agents.ai
- Live RAG demo: https://think-agents.ai/rag
