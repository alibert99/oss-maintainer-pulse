from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


def parse_github_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).astimezone(timezone.utc)


@dataclass(frozen=True)
class WorkItem:
    number: int
    title: str
    state: str
    labels: tuple[str, ...]
    author: str
    html_url: str
    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None
    comments: int
    is_pull_request: bool
    milestone_title: str | None = None
    draft: bool = False

    @classmethod
    def from_github_issue(cls, payload: dict[str, Any]) -> "WorkItem":
        labels = tuple(
            label.get("name", str(label)) if isinstance(label, dict) else str(label)
            for label in payload.get("labels", [])
        )
        user = payload.get("user") or {}
        created_at = parse_github_datetime(payload.get("created_at"))
        updated_at = parse_github_datetime(payload.get("updated_at"))
        if created_at is None or updated_at is None:
            raise ValueError(f"GitHub item #{payload.get('number')} is missing timestamps")

        pull_request = payload.get("pull_request") or {}
        milestone = payload.get("milestone") or {}
        return cls(
            number=int(payload["number"]),
            title=str(payload.get("title") or "").strip(),
            state=str(payload.get("state") or "open").lower(),
            labels=labels,
            author=str(user.get("login") or "unknown"),
            html_url=str(payload.get("html_url") or ""),
            created_at=created_at,
            updated_at=updated_at,
            closed_at=parse_github_datetime(payload.get("closed_at")),
            comments=int(payload.get("comments") or 0),
            is_pull_request="pull_request" in payload,
            milestone_title=_milestone_title(milestone),
            draft=bool(pull_request.get("draft", False)),
        )


def _milestone_title(milestone: Any) -> str | None:
    if not isinstance(milestone, dict):
        return None
    title = str(milestone.get("title") or "").strip()
    return title or None
