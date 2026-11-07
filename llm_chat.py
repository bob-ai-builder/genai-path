"""llm_chat.py — talk to an LLM from your terminal (Phase 1 deliverable).

Usage:
  python llm_chat.py "Explain a hash map in two sentences." \
      --model claude-haiku-5-5 --system "You are a terse senior engineer."
"""
import argparse
import sys
import time

import anthropic
from dotenv import load_dotenv

load_dotenv(override=True)  # reads ANTHROPIC_API_KEY from .env
client = anthropic.Anthropic()


def chat(prompt, model, system=None, temperature=None, max_tokens=1024):
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system
    if temperature is not None:
        # Current Claude models removed temperature; try it, fall back if rejected.
        try:
            return client.messages.create(**kwargs, extra_body={"temperature": temperature})
        except anthropic.BadRequestError as e:
            print(f"[note] API rejected temperature: {e.message}", file=sys.stderr)
    return client.messages.create(**kwargs)


def main():
    ap = argparse.ArgumentParser(description="Send one prompt to Claude.")
    ap.add_argument("prompt")
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--system", help="system prompt: persona and rules")
    ap.add_argument("--temperature", type=float, help="randomness, where the model supports it")
    ap.add_argument("--max-tokens", type=int, default=1024)
    a = ap.parse_args()

    start = time.perf_counter()
    msg = chat(a.prompt, a.model, a.system, a.temperature, a.max_tokens)
    secs = time.perf_counter() - start

    # Replies can also contain thinking blocks, so keep only the text blocks.
    print("".join(b.text for b in msg.content if b.type == "text"))
    u = msg.usage
    print(f"\n[{a.model} · {u.input_tokens} in / {u.output_tokens} out · "
          f"{secs:.1f}s · stop: {msg.stop_reason}]", file=sys.stderr)


if __name__ == "__main__":
    main()