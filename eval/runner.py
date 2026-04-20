"""Multi-LLM audit runner — minimal, hackable.

Sends each prompt in a YAML test set to N model providers in parallel,
returns a 4-column DataFrame (prompt_id, provider, response, latency_ms).

Designed to be readable in 15 minutes. Production use will fork from
here and add: rate-limiting, cost tracking, retry policy, persistence.

Usage:
    from eval.runner import Runner
    r = Runner.from_env()
    df = r.run_set("prompts/factuality.yml", providers=["gpt", "claude", "gemini"])
    df.to_parquet("results/run_2026-04-20.parquet")
"""
from __future__ import annotations

import os
import time
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Callable


# ── Provider adapters ──────────────────────────────────────────────────────


def _gpt(prompt: str) -> str:
    """OpenAI Responses API. Requires OPENAI_API_KEY."""
    import openai
    client = openai.OpenAI()
    resp = client.responses.create(
        model="gpt-5",
        input=prompt,
    )
    return getattr(resp, "output_text", "")


def _claude(prompt: str) -> str:
    """Anthropic Messages API. Requires ANTHROPIC_API_KEY."""
    import anthropic
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in msg.content if hasattr(b, "text"))


def _gemini(prompt: str) -> str:
    """Google Gemini API. Requires GOOGLE_API_KEY."""
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-pro")
    return model.generate_content(prompt).text


def _mistral(prompt: str) -> str:
    """Mistral API. Requires MISTRAL_API_KEY."""
    from mistralai.client import MistralClient
    client = MistralClient()
    resp = client.chat(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content


PROVIDERS: dict[str, Callable[[str], str]] = {
    "gpt": _gpt,
    "claude": _claude,
    "gemini": _gemini,
    "mistral": _mistral,
}


@dataclass
class Result:
    prompt_id: str
    provider: str
    response: str
    latency_ms: int
    error: str = ""


class Runner:
    """Parallel multi-provider runner."""

    def __init__(self, max_workers: int = 8):
        self.max_workers = max_workers

    @classmethod
    def from_env(cls):
        return cls(max_workers=int(os.environ.get("RUNNER_WORKERS", "8")))

    def _call_one(self, prompt_id: str, prompt: str, provider: str) -> Result:
        fn = PROVIDERS[provider]
        t0 = time.time()
        try:
            text = fn(prompt)
            return Result(prompt_id, provider, text, int((time.time() - t0) * 1000))
        except Exception as e:
            return Result(prompt_id, provider, "", int((time.time() - t0) * 1000), str(e))

    def run_set(self, yml_path: str, providers: list[str]) -> list[Result]:
        items = yaml.safe_load(open(yml_path))
        jobs = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures = []
            for item in items:
                pid = item["id"]
                prompt = item["prompt"]
                for prov in providers:
                    futures.append(pool.submit(self._call_one, pid, prompt, prov))
            for f in as_completed(futures):
                jobs.append(f.result())
        return jobs


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python runner.py <prompts.yml> <provider1,provider2,...>")
        sys.exit(2)
    runner = Runner.from_env()
    results = runner.run_set(sys.argv[1], sys.argv[2].split(","))
    for r in results:
        ok = "✓" if not r.error else "✗"
        print(f"{ok} [{r.provider:8}] {r.prompt_id:20} {r.latency_ms:5}ms  "
              f"{(r.error or r.response[:60])!r}")
