"""LLM-first ranking logic skeleton.

This module provides a lightweight orchestration layer for ranking candidates
by delegating scoring and breakdown computation to an LLM. It intentionally
avoids implementing numeric scoring logic locally; instead it builds prompts,
calls an LLM (via a provided client or the `llm_backend` module), parses the
LLM's structured JSON response, and returns a canonical result shape.

Why this file?
- Centralizes prompt construction, response parsing, and validation.
- Provides a single interface for the rest of the app to call (evaluate_candidates_with_llm).
- Makes it easy to stub the LLM during tests and to swap LLM providers later.

Planned responsibilities:
- normalize and validate candidate/config shapes
- build a repeatable prompt template
- call the LLM through a pluggable client
- parse and validate JSON responses into a canonical result
- provide audit-friendly output (raw prompt/response)

This file contains a minimal, ready-to-use skeleton and a simple orchestration
function you can call in your pipeline. The actual LLM call is delegated to
`call_llm()` which is easy to stub in tests.
"""

from typing import Any, Dict, List, Optional
import json
import time


def normalize_candidate(raw: Dict[str, Any]) -> Dict[str, Any]:
	"""Return a normalized candidate dict (lightweight).

	This function can be extended to canonicalize field names, lower-case
	strings, and ensure required subkeys exist. Keep it minimal so the LLM
	receives a predictable shape.
	"""
	c = dict(raw)
	# Ensure some keys exist to avoid KeyError in prompts
	c.setdefault("education", {})
	c.setdefault("skills", {})
	c.setdefault("general_skills", [])
	c.setdefault("personal_information", {})
	c.setdefault("available_types_of_work", [])
	return c


def build_prompt_for_candidate(candidate: Dict[str, Any], config: Dict[str, Any]) -> str:
	"""Construct a plain-text prompt for the LLM.

	Keep prompts small and include an explicit JSON output schema example so
	the LLM returns easy-to-parse JSON.
	"""
	cand = normalize_candidate(candidate)
	prompt = (
		"You are an assistant that scores candidates for a software engineering role.\n"
		"Return a single STRICT JSON object EXACTLY in the format shown in the example.\n"
		"Important: The response must be valid JSON, with keys and strings in double quotes, no comments, no trailing commas, and no Markdown code fences. Respond with ONLY the JSON object and nothing else.\n\n"
		"Candidate (input):\n"
		f"{json.dumps(cand, ensure_ascii=False, indent=2)}\n\n"
		"Config (rules):\n"
		f"{json.dumps(config, ensure_ascii=False, indent=2)}\n\n"
		"RESPONSE FORMAT EXAMPLE (must be valid JSON):\n"
		"{\n"
		"  \"score\": 0.82,\n"
		"  \"breakdown\": {\n"
		"    \"experience\": 0.9,\n"
		"    \"education\": 0.6,\n"
		"    \"general\": 0.7,\n"
		"    \"optional_bonus\": 0.05\n"
		"  },\n"
		"  \"passed_required\": true,\n"
		"  \"reasons\": [\"Short explanation here\"],\n"
		"  \"explanation\": \"One or two sentence explanation\"\n"
		"}\n\n"
		"Score the candidate now and return only the JSON object. Do not wrap it in backticks or markdown."
	)
	return prompt


def call_llm(prompt: str, llm_client: Optional[Any] = None, **opts) -> str:
	"""Call the LLM and return the raw string response.

	If `llm_client` is provided and callable, it will be used. Otherwise this
	function attempts to import `functions.llm_backend`
	and call a common function name `score_candidate(prompt)` if present.
	"""
	# If a client callable is provided, prefer it
	if llm_client and callable(llm_client):
		return llm_client(prompt, **opts)

	# Lazy import to avoid hard dependency during tests
	try:
		import llm_backend
	except Exception:
		raise NotImplementedError("No llm_client provided and llm_backend is unavailable")

	# Prefer a function named `score_candidate` if implemented
	if hasattr(llm_backend, "score_candidate") and callable(llm_backend.score_candidate):
		return llm_backend.score_candidate(prompt, **opts)

	raise NotImplementedError("llm_backend.score_candidate not implemented")


def parse_llm_json_response(raw: str) -> Dict[str, Any]:
	"""Extract and parse the first JSON object found in the LLM response string.

	Returns a dict on success or raises ValueError on parse errors.
	"""
	# Strip common markdown code fences and whitespace
	text = raw.strip()
	if text.startswith("```"):
		# Remove leading fence line
		first_newline = text.find("\n")
		if first_newline != -1:
			text = text[first_newline + 1 :]
	if text.endswith("```"):
		text = text[: -3].strip()

	# Find first '{' and last '}' to be tolerant of surrounding text
	start = text.find("{")
	end = text.rfind("}")
	if start == -1 or end == -1 or end < start:
		raise ValueError("No JSON object found in LLM response")
	snippet = text[start:end+1]
	try:
		return json.loads(snippet)
	except json.JSONDecodeError as e:
		# Try a small heuristic: if the model forgot the final '}', append one once
		try:
			return json.loads(snippet + "}")
		except json.JSONDecodeError:
			preview = snippet[:200].replace("\n", " ")
			raise ValueError(f"Failed to parse JSON snippet: {e.msg} (pos {e.pos}). Snippet preview: {preview}") from e


def evaluate_candidates_with_llm(candidates: List[Dict[str, Any]], config: Dict[str, Any],
								 llm_client: Optional[Any] = None, concurrency: int = 1) -> List[Dict[str, Any]]:
	"""Evaluate each candidate by calling the LLM and returning canonical results.

	This function is intentionally sequential and simple; you can add
	concurrency later if needed.
	"""
	results: List[Dict[str, Any]] = []
	overall_start = time.time()
	total_candidates = len(candidates)
	
	for idx, cand in enumerate(candidates, start=1):
		candidate_start = time.time()
		candidate_name = cand.get("name", cand.get("id", "Unknown"))
		
		# Display progress with live timer
		print(f"  [{idx}/{total_candidates}] Processing: {candidate_name}...", end=" ", flush=True)
		
		prompt = build_prompt_for_candidate(cand, config)
		try:
			raw = call_llm(prompt, llm_client=llm_client)
			parsed = parse_llm_json_response(raw)
			candidate_elapsed = time.time() - candidate_start
			print(f"✓ ({candidate_elapsed:.1f}s)")
		except Exception as e:
			candidate_elapsed = time.time() - candidate_start
			print(f"✗ ({candidate_elapsed:.1f}s) - Error: {str(e)[:50]}")
			# On failure, record the error and continue
			results.append({
				"id": cand.get("id"),
				"name": cand.get("name"),
				"llm_score": None,
				"score_10": None,
				"breakdown": {},
				"passed_required": False,
				"reasons": [f"LLM error: {e}"],
				"raw_llm_output": None,
				"explanation": None,
			})
			continue

		# Convert parsed response into canonical result shape
		score = parsed.get("score")
		score_10 = (score * 10) if isinstance(score, (int, float)) else None
		breakdown = parsed.get("breakdown", {}) if isinstance(parsed.get("breakdown", {}), dict) else {}
		passed = bool(parsed.get("passed_required", False))
		reasons = parsed.get("reasons") or []
		explanation = parsed.get("explanation")

		results.append({
			"id": cand.get("id"),
			"name": cand.get("name"),
			"llm_score": float(score) if isinstance(score, (int, float)) else None,
			"score_10": float(score_10) if isinstance(score_10, (int, float)) else None,
			"breakdown": breakdown,
			"passed_required": passed,
			"reasons": list(reasons) if isinstance(reasons, list) else [str(reasons)],
			"raw_llm_output": raw,
			"explanation": explanation,
		})

	overall_elapsed = time.time() - overall_start
	print(f"\n  Total time: {overall_elapsed:.1f}s\n")

	# Sort by llm_score desc, placing None scores at the end
	def sort_key(r: Dict[str, Any]):
		return (r["llm_score"] is None, -(r["llm_score"] or 0))

	return sorted(results, key=sort_key)
