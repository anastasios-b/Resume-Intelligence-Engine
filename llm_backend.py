"""Minimal Cloudflare AI-backed LLM helper.

Provides a small wrapper around Cloudflare's AI HTTP API. The primary
entrypoint exposed here is `score_candidate(prompt, model=None, timeout=600)`
which POSTs a chat-style `messages` payload to the /ai/run endpoint and
returns the assistant message content as a string.

This file intentionally keeps behavior small and deterministic so callers can
handle RuntimeError exceptions and present user-friendly messages.
"""

from __future__ import annotations

import os
from typing import Optional

import requests

from constants import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_MODEL


def is_ollama_installed() -> bool:
	"""Compatibility shim: return True if Cloudflare AI configuration is present.

	The rest of the codebase calls this at startup; here we simply ensure that
	required Cloudflare env vars are set so the script can fail fast with a
	clear message if not.
	"""
	return bool(CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID)


def _get_cloudflare_config(model: Optional[str] = None) -> tuple[str, str, str]:
	"""Resolve Cloudflare account, token, and model from environment or args."""
	account_id = CLOUDFLARE_ACCOUNT_ID
	api_token = CLOUDFLARE_API_TOKEN
	model_name = model or CLOUDFLARE_MODEL

	if not account_id:
		raise RuntimeError("Missing CLOUDFLARE_ACCOUNT_ID environment variable.")
	if not api_token:
		raise RuntimeError("Missing CLOUDFLARE_API_TOKEN environment variable.")
	if not model_name:
		raise RuntimeError("Cloudflare model name is empty. Set CLOUDFLARE_MODEL or pass model explicitly.")

	return account_id, api_token, model_name


def score_candidate(prompt: str, model: Optional[str] = None, timeout: int = 600) -> str:
	"""Call Cloudflare AI /ai/run with the provided prompt and return its output.

	Args:
		prompt: text prompt fed to the model as a user message
		model: optional model name (falls back to CLOUDFLARE_MODEL or
		       '@cf/meta/llama-3-8b-instruct')
	timeout: seconds to wait for the HTTP request to complete

	Raises:
		RuntimeError: if configuration is missing or the HTTP request fails.
	"""
	account_id, api_token, model_name = _get_cloudflare_config(model)

	url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model_name}"
	headers = {
		"Authorization": f"Bearer {api_token}",
		"Content-Type": "application/json",
	}
	# Cloudflare's text generation models accept a single `prompt` string.
	full_prompt = (
		"You are an assistant that scores candidates for a software engineering role. "
		"Return a single STRICT JSON object following the schema described in the prompt. "
		"The JSON must be valid (double-quoted keys/strings, no comments, no trailing commas).\n\n"
		+ prompt
	)
	payload = {"prompt": full_prompt}

	try:
		resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
	except requests.RequestException as exc:
		raise RuntimeError(f"Error calling Cloudflare AI API: {exc}") from exc

	if not resp.ok:
		raise RuntimeError(f"Cloudflare AI API returned HTTP {resp.status_code}: {resp.text[:500]}")

	data = resp.json()
	# Cloudflare's /ai/run response for chat models typically contains the
	# assistant text under 'result.response' or 'result.output'. We first try
	# the more structured chat response, then fall back to simple fields.
	result = data.get("result") or {}
	text: Optional[str] = None

	# Try chat-style responses
	if isinstance(result, dict):
		if "response" in result:
			msg = result["response"]
			if isinstance(msg, dict):
				text = msg.get("content") or msg.get("message")
			elif isinstance(msg, str):
				# Some Cloudflare models return the assistant text as a raw string here
				text = msg
		elif "output" in result:
			msg = result["output"]
			if isinstance(msg, dict):
				text = msg.get("content") or msg.get("message")
			elif isinstance(msg, str):
				text = msg
		elif "output_text" in result:
			text = result.get("output_text")

	if not text and isinstance(result, str):
		text = result

	if not text:
		# Last resort: return the full JSON as a string so callers can inspect.
		text = str(data)

	return text


__all__ = ["is_ollama_installed", "score_candidate"]
