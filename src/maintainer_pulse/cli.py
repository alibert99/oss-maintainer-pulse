from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from . import __version__
from .analysis import analyze
from .github import fetch_items, load_items
from .report import render_csv, render_html, render_json, render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maintainer-pulse",
        description="Generate a GitHub issue and pull request health report for maintainers.",
    )
    parser.add_argument(
        "repository",
        nargs="?",
        help="Repository as owner/name or https://github.com/owner/name. Optional when --input is used.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Path to exported GitHub issues JSON. Skips network access when provided.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the report to this path. Defaults to stdout.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "html", "json", "csv"),
        default="markdown",
        help="Report format.",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=30,
        help="Number of idle days before an open item is considered stale.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=2,
        help="Maximum GitHub API pages to fetch when reading live data.",
    )
    parser.add_argument(
        "--token-env",
        default="GITHUB_TOKEN",
        help="Environment variable containing a GitHub token for live fetches.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.stale_days < 1:
        parser.error("--stale-days must be at least 1")
    if args.max_pages < 1:
        parser.error("--max-pages must be at least 1")
    if args.input is None and not args.repository:
        parser.error("provide a repository or --input")

    try:
        if args.input:
            items = load_items(args.input)
            repository = args.repository or args.input.stem
        else:
            token = os.environ.get(args.token_env)
            items = fetch_items(args.repository, token=token, max_pages=args.max_pages)
            repository = args.repository

        pulse = analyze(items, repository, stale_days=args.stale_days)
        rendered = _render(args.format, pulse)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
            if not rendered.endswith("\n"):
                sys.stdout.write("\n")
    except Exception as exc:
        print(f"maintainer-pulse: {exc}", file=sys.stderr)
        return 1

    return 0


def _render(format_name: str, pulse):
    if format_name == "markdown":
        return render_markdown(pulse)
    if format_name == "html":
        return render_html(pulse)
    if format_name == "json":
        return render_json(pulse)
    if format_name == "csv":
        return render_csv(pulse)
    raise ValueError(f"Unsupported format: {format_name}")
