from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from .models import WorkItem

GITHUB_API = "https://api.github.com"


def load_items(path: str | Path) -> list[WorkItem]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    raw_items = _extract_items(payload)
    return [WorkItem.from_github_issue(item) for item in raw_items]


def fetch_items(repository: str, *, token: str | None = None, max_pages: int = 2) -> list[WorkItem]:
    owner, name = _split_repository(repository)
    encoded_owner = urllib.parse.quote(owner, safe="")
    encoded_name = urllib.parse.quote(name, safe="")
    token = token or os.environ.get("GITHUB_TOKEN")
    items: list[WorkItem] = []

    for page in range(1, max_pages + 1):
        query = urllib.parse.urlencode({"state": "all", "per_page": "100", "page": str(page)})
        url = f"{GITHUB_API}/repos/{encoded_owner}/{encoded_name}/issues?{query}"
        request = urllib.request.Request(url, headers=_headers(token))
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"GitHub API request failed with {exc.code}: {detail}") from exc

        if not isinstance(payload, list):
            raise RuntimeError("GitHub API returned an unexpected response")
        items.extend(WorkItem.from_github_issue(item) for item in payload)
        if len(payload) < 100:
            break

    return items


def _extract_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("items", "data", "issues"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    raise ValueError("Expected a GitHub issues list or an object containing items/data/issues")


def _split_repository(repository: str) -> tuple[str, str]:
    parts = repository.strip().removeprefix("https://github.com/").strip("/").split("/")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError("Repository must look like owner/name or https://github.com/owner/name")
    return parts[0], parts[1]


def _headers(token: str | None) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "oss-maintainer-pulse",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

