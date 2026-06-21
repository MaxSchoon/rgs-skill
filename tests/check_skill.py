#!/usr/bin/env python3
"""
check_skill.py — CI guardrails for the RGS skill.

Validates the things that silently break a skill if they regress:
  - SKILL.md exists, parses, and stays within skill-runtime size limits
    (body < 32 KiB; frontmatter `description` <= 1024 chars).
  - SKILL.md has the required `name` and `description` frontmatter keys.
  - Every `references/<file>.md` mentioned in SKILL.md actually exists
    (so the routing table never points at a missing file).
  - The bundled script byte-compiles.

Exits non-zero on any failure so it can gate merges as a required check.
Pure stdlib; no third-party dependencies.
"""
from __future__ import annotations

import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
DESC_LIMIT = 1024          # Anthropic SKILL.md description hard limit (chars)
BODY_LIMIT = 32 * 1024     # 32 KiB skill-body comfort/limit (bytes)

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def main() -> int:
    if not SKILL.exists():
        fail("SKILL.md is missing at the repo root.")
        return report()

    raw = SKILL.read_text(encoding="utf-8")

    # Body size (bytes).
    body_bytes = len(raw.encode("utf-8"))
    if body_bytes > BODY_LIMIT:
        fail(f"SKILL.md is {body_bytes} bytes (> {BODY_LIMIT}). Move content into references/.")

    # Frontmatter.
    fm_match = re.match(r"^---\n(.*?)\n---", raw, re.S)
    if not fm_match:
        fail("SKILL.md has no YAML frontmatter delimited by '---'.")
        return report()
    fm = fm_match.group(1)

    if not re.search(r"^name:\s*\S", fm, re.M):
        fail("SKILL.md frontmatter is missing a non-empty `name:`.")

    # description (supports folded `>-` scalars and single-line form).
    desc = ""
    folded = re.search(r"description:\s*>-?\s*\n(.*?)(?=\n[A-Za-z_-]+:\s|\Z)", fm, re.S)
    inline = re.search(r"description:\s*(?!>)(\S.*)", fm)
    if folded:
        desc = " ".join(l.strip() for l in folded.group(1).splitlines() if l.strip())
    elif inline:
        desc = inline.group(1).strip().strip('"').strip("'")
    else:
        fail("SKILL.md frontmatter is missing a `description:`.")

    if desc:
        if len(desc) > DESC_LIMIT:
            fail(f"description is {len(desc)} chars (> {DESC_LIMIT}). Trim it.")
        elif len(desc) < 40:
            fail(f"description is only {len(desc)} chars — too short to trigger reliably.")

    # Referenced reference files must exist.
    for ref in sorted(set(re.findall(r"references/([A-Za-z0-9_-]+\.md)", raw))):
        if not (ROOT / "references" / ref).exists():
            fail(f"SKILL.md references references/{ref}, which does not exist.")

    # Bundled script must compile.
    script = ROOT / "scripts" / "rgs_lookup.py"
    if not script.exists():
        fail("scripts/rgs_lookup.py is missing.")
    else:
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as exc:
            fail(f"scripts/rgs_lookup.py does not compile: {exc}")

    return report()


def report() -> int:
    if errors:
        print("check_skill.py: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("check_skill.py: OK — SKILL.md within limits, references resolve, script compiles.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
