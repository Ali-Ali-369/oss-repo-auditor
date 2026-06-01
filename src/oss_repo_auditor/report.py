from __future__ import annotations

import json
from dataclasses import asdict

from .models import AuditReport


def render_markdown(report: AuditReport) -> str:
    lines = [
        "# OSS Repo Audit",
        "",
        f"- Path: {report.path}",
        f"- Score: {report.score}",
        f"- Grade: {report.grade}",
        "",
        "## Checks",
        "",
    ]
    for check in report.checks:
        marker = "PASS" if check.status == "pass" else "FAIL"
        lines.append(f"- {marker} {check.name}: {check.detail}")
    return "\n".join(lines).rstrip() + "\n"


def render_json(report: AuditReport) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True) + "\n"
