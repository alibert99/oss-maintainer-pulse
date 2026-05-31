from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from .analysis import PulseReport
from .report import report_to_dict

DEFAULT_OPENAI_MODEL = "gpt-5-mini"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def generate_openai_summary(
    report: PulseReport,
    *,
    api_key: str,
    model: str = DEFAULT_OPENAI_MODEL,
    timeout: int = 30,
) -> str:
    if not api_key:
        raise ValueError("OpenAI API key is required for --ai-summary")

    payload = {
        "model": model,
        "instructions": (
            "You help open-source maintainers triage GitHub issue and pull request queues. "
            "Use only the report data provided. Be concise, practical, and cautious. "
            "Do not invent adoption, severity, ownership, or project facts. "
            "Return Markdown with three sections: Focus, Risks, Suggested next actions."
        ),
        "input": _prompt(report),
        "max_output_tokens": 700,
    }
    request = urllib.request.Request(
        OPENAI_RESPONSES_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "oss-maintainer-pulse",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API request failed with {exc.code}: {detail}") from exc

    text = _extract_output_text(response_payload)
    if not text:
        raise RuntimeError("OpenAI API response did not include text output")
    return text.strip()


def _prompt(report: PulseReport) -> str:
    data = report_to_dict(report, limit=8)
    return (
        "Summarize this Maintainer Pulse report for a maintainer. "
        "Prioritize release blockers, stuck pull requests, response debt, stale items, "
        "quick wins, and duplicate candidates.\n\n"
        f"{json.dumps(data, indent=2, sort_keys=True)}"
    )


def _extract_output_text(payload: dict[str, Any]) -> str:
    output_text = payload.get("output_text")
    if isinstance(output_text, str):
        return output_text

    parts: list[str] = []
    for item in payload.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if not isinstance(content, dict):
                continue
            text = content.get("text")
            if isinstance(text, str):
                parts.append(text)
    return "\n".join(parts)
