from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TextIO

from .audit import audit_repository
from .report import render_json, render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="oss-repo-auditor",
        description="Create a local open-source repository hygiene report.",
    )
    parser.add_argument("path", type=Path, help="Repository path to audit.")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Report format.",
    )
    parser.add_argument(
        "--fail-under",
        type=int,
        metavar="SCORE",
        help="Exit with status 2 if the audit score is below this threshold.",
    )
    return parser


def main(argv: list[str] | None = None, stdout: TextIO | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    out = stdout or sys.stdout

    if not args.path.exists() or not args.path.is_dir():
        parser.error(f"{args.path} is not a directory")

    report = audit_repository(args.path)
    rendered = render_json(report) if args.format == "json" else render_markdown(report)
    out.write(rendered)
    if args.fail_under is not None and report.score < args.fail_under:
        return 2
    return 0
