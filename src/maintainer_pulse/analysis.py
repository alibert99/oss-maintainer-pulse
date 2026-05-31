from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import re
from statistics import median

from .models import WorkItem

RELEASE_LABELS = {
    "blocker",
    "critical",
    "p0",
    "p1",
    "release",
    "release-blocker",
    "regression",
    "security",
}
QUICK_WIN_LABELS = {"documentation", "good first issue", "help wanted", "starter"}
REVIEW_LABELS = {"blocked", "needs review", "review", "waiting on maintainer"}
TITLE_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}


@dataclass(frozen=True)
class PulseMetrics:
    health_score: int
    open_issues: int
    open_pull_requests: int
    stale_items: int
    response_debt: int
    release_blockers: int
    stuck_pull_requests: int
    recent_closed: int
    median_days_to_close: float | None


@dataclass(frozen=True)
class DuplicateCandidate:
    first: WorkItem
    second: WorkItem
    similarity: float
    shared_terms: tuple[str, ...]


@dataclass(frozen=True)
class PulseReport:
    repository: str
    generated_at: datetime
    stale_days: int
    metrics: PulseMetrics
    queues: dict[str, list[WorkItem]]
    duplicate_candidates: list[DuplicateCandidate]
    recommendations: list[str]
    ai_summary: str | None = None
    ai_provider: str | None = None
    ai_model: str | None = None


def analyze(
    items: list[WorkItem],
    repository: str,
    *,
    stale_days: int = 30,
    now: datetime | None = None,
) -> PulseReport:
    now = now or datetime.now(timezone.utc)
    open_items = [item for item in items if item.state == "open"]
    open_issues = [item for item in open_items if not item.is_pull_request]
    open_pull_requests = [item for item in open_items if item.is_pull_request]

    stale = [item for item in open_items if idle_days(item, now) >= stale_days]
    response_debt = [
        item
        for item in open_items
        if item.comments == 0 and idle_days(item, now) >= 3 and not _has_label(item, "bot")
    ]
    release_blockers = [
        item
        for item in open_items
        if _has_any_label(item, RELEASE_LABELS) or "security" in item.title.lower()
    ]
    stuck_pull_requests = [
        item
        for item in open_pull_requests
        if idle_days(item, now) >= 7 or _has_any_label(item, REVIEW_LABELS)
    ]
    quick_wins = [
        item
        for item in open_issues
        if _has_any_label(item, QUICK_WIN_LABELS) and item.comments <= 4
    ]

    closed_recent = [
        item
        for item in items
        if item.closed_at is not None and item.closed_at >= now - timedelta(days=90)
    ]
    close_durations = [
        max((item.closed_at - item.created_at).total_seconds() / 86400, 0.0)
        for item in closed_recent
        if item.closed_at is not None
    ]
    median_days_to_close = round(median(close_durations), 1) if close_durations else None

    metrics = PulseMetrics(
        health_score=_score(
            open_count=len(open_items),
            stale_count=len(stale),
            response_debt_count=len(response_debt),
            release_blocker_count=len(release_blockers),
            stuck_pr_count=len(stuck_pull_requests),
            recent_closed_count=len(closed_recent),
        ),
        open_issues=len(open_issues),
        open_pull_requests=len(open_pull_requests),
        stale_items=len(stale),
        response_debt=len(response_debt),
        release_blockers=len(release_blockers),
        stuck_pull_requests=len(stuck_pull_requests),
        recent_closed=len(closed_recent),
        median_days_to_close=median_days_to_close,
    )
    queues = {
        "release_blockers": _sort_by_idle(release_blockers, now),
        "stuck_pull_requests": _sort_by_idle(stuck_pull_requests, now),
        "response_debt": _sort_by_idle(response_debt, now),
        "stale_items": _sort_by_idle(stale, now),
        "quick_wins": sorted(quick_wins, key=lambda item: (item.comments, item.created_at)),
    }
    return PulseReport(
        repository=repository,
        generated_at=now,
        stale_days=stale_days,
        metrics=metrics,
        queues=queues,
        duplicate_candidates=_duplicate_candidates(open_issues),
        recommendations=_recommend(metrics),
    )


def idle_days(item: WorkItem, now: datetime) -> int:
    return max(int((now - item.updated_at).total_seconds() // 86400), 0)


def age_days(item: WorkItem, now: datetime) -> int:
    return max(int((now - item.created_at).total_seconds() // 86400), 0)


def _has_label(item: WorkItem, target: str) -> bool:
    return target.lower() in {label.lower() for label in item.labels}


def _has_any_label(item: WorkItem, targets: set[str]) -> bool:
    labels = {label.lower() for label in item.labels}
    return bool(labels.intersection(targets))


def _sort_by_idle(items: list[WorkItem], now: datetime) -> list[WorkItem]:
    return sorted(items, key=lambda item: idle_days(item, now), reverse=True)


def _duplicate_candidates(
    items: list[WorkItem],
    *,
    threshold: float = 0.5,
    limit: int = 10,
) -> list[DuplicateCandidate]:
    candidates: list[DuplicateCandidate] = []
    tokenized = [(item, _title_terms(item.title)) for item in items]

    for index, (first, first_terms) in enumerate(tokenized):
        if len(first_terms) < 2:
            continue
        for second, second_terms in tokenized[index + 1 :]:
            if len(second_terms) < 2:
                continue

            shared = first_terms.intersection(second_terms)
            if len(shared) < 2:
                continue

            union = first_terms.union(second_terms)
            similarity = len(shared) / len(union)
            if similarity >= threshold:
                candidates.append(
                    DuplicateCandidate(
                        first=first,
                        second=second,
                        similarity=round(similarity, 2),
                        shared_terms=tuple(sorted(shared)),
                    )
                )

    return sorted(candidates, key=lambda candidate: candidate.similarity, reverse=True)[:limit]


def _title_terms(title: str) -> set[str]:
    return {
        term
        for term in re.findall(r"[a-z0-9]+", title.lower())
        if len(term) > 2 and term not in TITLE_STOP_WORDS
    }


def _score(
    *,
    open_count: int,
    stale_count: int,
    response_debt_count: int,
    release_blocker_count: int,
    stuck_pr_count: int,
    recent_closed_count: int,
) -> int:
    if open_count == 0:
        return 100

    stale_penalty = min((stale_count / open_count) * 30, 30)
    response_penalty = min(response_debt_count * 3, 15)
    blocker_penalty = min(release_blocker_count * 5, 20)
    review_penalty = min(stuck_pr_count * 4, 20)
    activity_credit = min(recent_closed_count, 10)

    score = 100 - stale_penalty - response_penalty - blocker_penalty - review_penalty
    return max(1, min(100, round(score + activity_credit)))


def _recommend(metrics: PulseMetrics) -> list[str]:
    recommendations: list[str] = []
    if metrics.release_blockers:
        recommendations.append(
            f"Resolve or explicitly defer {metrics.release_blockers} release blocker(s)."
        )
    if metrics.stuck_pull_requests:
        recommendations.append(
            f"Start review time with {metrics.stuck_pull_requests} stuck pull request(s)."
        )
    if metrics.response_debt:
        recommendations.append(
            f"Reply to {metrics.response_debt} open item(s) with no maintainer response."
        )
    if metrics.stale_items:
        recommendations.append(
            f"Close, relabel, or revive {metrics.stale_items} item(s) idle past the stale threshold."
        )
    if not recommendations:
        recommendations.append("Queue health is strong; keep the current review and release cadence.")
    return recommendations
