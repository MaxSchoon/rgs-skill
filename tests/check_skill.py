#!/usr/bin/env python3
"""Structural gates for the RGS skill (standard library only).

Enforces what CONTRIBUTING.md promises, so a PR cannot silently break the
agent contract:

  1. SKILL.md: under 32 KiB and 500 lines; front matter with `name` and a
     `description` under 1024 characters.
  2. Every `references/<file>.md` link in any Markdown file resolves, and
     every reference is linked from SKILL.md.
  3. Each reference has the standard shape: front matter with `reference_id`
     (matching the file name), `verified_on` (ISO 8601 date) and
     `rgs_version`; exactly one H1; a `**Load this when:**` and a
     `**Do not load this when:**` line; a `## Contents` list whose links
     resolve; `## Sources` as the last H2.
  4. Citation markers: every `[Sn]` in a reference body resolves to a
     `**[Sn]**` entry in its Sources list, every entry is cited, and every
     entry carries an `[viewed YYYY-MM-DD]` date and a URL.
  5. The licence surface is present: LICENSE (Apache-2.0), LICENSE-CONTENT
     (CC BY 4.0), LICENSES/MIT.txt, NOTICE, ATTRIBUTION.md, rsl.xml and
     llms.txt exist, SKILL.md's front matter points at NOTICE, and SKILL.md
     and every reference carry the attribution the licence requires.
  6. The bundled script byte-compiles.

Run: python3 tests/check_skill.py
Exits non-zero (with `::error::` annotations for GitHub Actions) on any
violation.
"""

from __future__ import annotations

import py_compile
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
REFERENCES = ROOT / "references"
SCRIPT = ROOT / "scripts" / "rgs_lookup.py"

LICENSE_FILES = ("LICENSE", "LICENSE-CONTENT", "LICENSES/MIT.txt", "NOTICE",
                 "ATTRIBUTION.md", "rsl.xml", "llms.txt")
# The credit the licence requires (ATTRIBUTION.md § The short string).
ATTRIBUTION_PARTS = ("Max Schoon", "Ontos B.V.", "RGS Skill", "github.com/MaxSchoon/rgs-skill")

MAX_SKILL_BYTES = 32 * 1024
MAX_SKILL_LINES = 500
MAX_DESCRIPTION_CHARS = 1024
MIN_DESCRIPTION_CHARS = 40

REQUIRED_FRONT_MATTER = ("reference_id", "verified_on", "rgs_version")
LOAD_MARKS = ("**Load this when:**", "**Do not load this when:**")
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")

SOURCE_MARKER = re.compile(r"\[S(\d+)\]")
SOURCE_ENTRY = re.compile(r"^\s*-\s*\*\*\[S(\d+)\]\*\*(.*)$", re.M)
VIEWED = re.compile(r"\[viewed (\d{4}-\d{2}-\d{2})\]")
URL = re.compile(r"https?://\S+")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.M)
SAME_DOC_LINK = re.compile(r"\]\(#([^)\s]+)\)")
REF_LINK = re.compile(r"references/([A-Za-z0-9._-]+\.md)")
FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"(`+)[^\n]*?\1")

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"::error::{msg}")


def failures_since(mark: int) -> int:
    return len(errors) - mark


def parse_front_matter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    out: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#", "-")):
            key, _, value = line.partition(":")
            out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def mask_fences(text: str) -> str:
    """Blank fenced blocks and inline code, preserving offsets."""
    out: list[str] = []
    marker = ""
    for line in text.split("\n"):
        if marker:
            closing = line.strip()
            out.append(" " * len(line))
            if closing and closing[0] == marker[0] and closing == closing[0] * len(closing) and len(closing) >= len(marker):
                marker = ""
            continue
        opened = FENCE.match(line)
        if opened:
            marker = opened.group(1)
            out.append(" " * len(line))
            continue
        out.append(INLINE_CODE.sub(lambda m: " " * len(m.group()), line))
    return "\n".join(out)


def slugify(heading: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", heading)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def heading_slugs(text: str) -> set[str]:
    taken: set[str] = set()
    for _, h in HEADING.findall(mask_fences_keep_headings(text)):
        base = slugify(h)
        slug, n = base, 1
        while slug in taken:
            slug = f"{base}-{n}"
            n += 1
        taken.add(slug)
    return taken


def mask_fences_keep_headings(text: str) -> str:
    # Headings inside fences are not headings; blank fenced blocks only.
    out: list[str] = []
    marker = ""
    for line in text.split("\n"):
        if marker:
            closing = line.strip()
            out.append("")
            if closing and closing[0] == marker[0] and closing == closing[0] * len(closing) and len(closing) >= len(marker):
                marker = ""
            continue
        if FENCE.match(line):
            marker = FENCE.match(line).group(1)
            out.append("")
            continue
        out.append(line)
    return "\n".join(out)


def check_skill() -> None:
    mark = len(errors)
    if not SKILL.is_file():
        fail("SKILL.md is missing")
        return
    raw = SKILL.read_bytes()
    if len(raw) > MAX_SKILL_BYTES:
        fail(f"SKILL.md is {len(raw)} bytes; must stay under {MAX_SKILL_BYTES}")
    text = raw.decode("utf-8")
    lines = text.count("\n") + 1
    if lines > MAX_SKILL_LINES:
        fail(f"SKILL.md has {lines} lines; must stay under {MAX_SKILL_LINES}")
    fm = parse_front_matter(text)
    if fm is None:
        fail("SKILL.md has no YAML front matter")
        return
    if not fm.get("name"):
        fail("SKILL.md front matter is missing `name`")
    desc = fm.get("description", "")
    if not desc:
        fail("SKILL.md front matter is missing `description`")
    elif len(desc) > MAX_DESCRIPTION_CHARS:
        fail(f"SKILL.md description is {len(desc)} chars; must stay under {MAX_DESCRIPTION_CHARS}")
    elif len(desc) < MIN_DESCRIPTION_CHARS:
        fail(f"SKILL.md description is {len(desc)} chars; too short to trigger reliably")
    linked = set(REF_LINK.findall(text))
    for ref in sorted(p.name for p in REFERENCES.glob("*.md")):
        if ref not in linked:
            fail(f"references/{ref} is not linked from SKILL.md")
    if not failures_since(mark):
        print(f"SKILL.md OK ({len(raw)} bytes, {lines} lines, description {len(desc)} chars)")


def check_reference_links() -> None:
    mark = len(errors)
    known = {p.name for p in REFERENCES.glob("*.md")}
    sources = sorted(p for p in ROOT.rglob("*.md") if ".venv" not in p.parts and "node_modules" not in p.parts)
    checked = 0
    for src in sources:
        text = src.read_text(encoding="utf-8")
        label = src.relative_to(ROOT).as_posix()
        for rel in sorted(set(REF_LINK.findall(text))):
            checked += 1
            if rel not in known:
                fail(f"{label}: link to references/{rel} does not resolve")
    if not failures_since(mark):
        print(f"Reference links OK ({checked} checked across {len(sources)} files)")


def check_reference(path: Path) -> None:
    name = path.name
    raw = path.read_bytes()
    if b"\r\n" in raw:
        fail(f"{name}: CRLF line endings")
    if not raw.endswith(b"\n"):
        fail(f"{name}: no final newline")
    text = raw.decode("utf-8")
    if re.search(r"^(<{7}|={7}|>{7})", text, re.M):
        fail(f"{name}: merge conflict markers present")

    fm = parse_front_matter(text)
    if fm is None:
        fail(f"{name}: missing YAML front matter")
    else:
        for key in REQUIRED_FRONT_MATTER:
            if not fm.get(key):
                fail(f"{name}: front matter missing `{key}`")
        if fm.get("reference_id") and fm["reference_id"] != path.stem:
            fail(f"{name}: reference_id `{fm['reference_id']}` does not match the file name")
        if fm.get("verified_on") and not ISO_DATE.fullmatch(fm["verified_on"]):
            fail(f"{name}: verified_on `{fm['verified_on']}` is not YYYY-MM-DD")

    masked = mask_fences(text)
    for mark_text in LOAD_MARKS:
        if not re.search(rf"(?m)^{re.escape(mark_text)}", masked):
            fail(f"{name}: missing the `{mark_text}` line")

    heads = [(len(h), t) for h, t in HEADING.findall(mask_fences_keep_headings(text))]
    if len([t for lvl, t in heads if lvl == 1]) != 1:
        fail(f"{name}: expected exactly one H1")
    h2 = [t for lvl, t in heads if lvl == 2]
    if not h2:
        fail(f"{name}: no H2 sections")
        return
    if h2[0] != "Contents":
        fail(f"{name}: first H2 is {h2[0]!r}, expected 'Contents'")
    if not h2[-1].startswith("Sources"):
        fail(f"{name}: last H2 is {h2[-1]!r}, expected 'Sources'")
    for lvl, t in heads:
        if lvl == 2 and re.match(r"^\d+\.\s", t):
            fail(f"{name}: numbered heading {t!r}; use names, not numbers")

    targets = heading_slugs(text)
    for anchor in SAME_DOC_LINK.findall(masked):
        if anchor not in targets:
            fail(f"{name}: link to `#{anchor}` matches no heading")
    # Every H2 except Contents and Sources must appear in the Contents list.
    contents_block = re.search(r"^## Contents\n(.*?)^## ", masked, re.S | re.M)
    listed = set(SAME_DOC_LINK.findall(contents_block.group(1))) if contents_block else set()
    for t in h2[1:]:
        if slugify(t) not in listed:
            fail(f"{name}: section {t!r} is not in the Contents list")

    # Citation markers.
    entries = list(SOURCE_ENTRY.finditer(masked))
    body = masked[: entries[0].start()] if entries else masked
    used = set(SOURCE_MARKER.findall(body))
    defined: set[str] = set()
    for m in entries:
        n = m.group(1)
        if n in defined:
            fail(f"{name}: source entry [S{n}] is defined twice")
        defined.add(n)
        tail = text[m.start():m.end()]
        if not VIEWED.search(tail):
            fail(f"{name}: source entry [S{n}] has no `[viewed YYYY-MM-DD]` date")
        if not URL.search(tail):
            fail(f"{name}: source entry [S{n}] has no URL")
    if not defined:
        fail(f"{name}: no `**[Sn]**` entries in Sources")
    for orphan in sorted(used - defined, key=int):
        fail(f"{name}: [S{orphan}] is cited but has no source entry")
    for unused in sorted(defined - used, key=int):
        fail(f"{name}: source entry [S{unused}] is never cited in the body")
    if not used:
        fail(f"{name}: body cites no source markers")


def check_references() -> None:
    mark = len(errors)
    paths = sorted(REFERENCES.glob("*.md"))
    if not paths:
        fail("references/ holds no reference files")
    for path in paths:
        check_reference(path)
    if not failures_since(mark):
        print(f"Reference structure and citations OK ({len(paths)} files)")


def check_attribution() -> None:
    """The licence surface is present and every shipped file carries the credit.

    A licence obligation nobody checks quietly rots away: a reference added
    without its header would ship without the attribution ATTRIBUTION.md
    tells users to expect there.
    """
    mark = len(errors)
    for rel in LICENSE_FILES:
        if not (ROOT / rel).is_file():
            fail(f"{rel} is missing")
    if SKILL.is_file():
        text = SKILL.read_text(encoding="utf-8")
        fm = parse_front_matter(text) or {}
        if fm.get("license") != "see NOTICE":
            fail("SKILL.md front matter `license` must be `see NOTICE`")
        for part in ATTRIBUTION_PARTS:
            if part not in text:
                fail(f"SKILL.md lacks the attribution part {part!r}")
    for path in sorted(REFERENCES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        head = text.split(LOAD_MARKS[0], 1)[0]
        for part in ATTRIBUTION_PARTS:
            if part not in head:
                fail(f"{path.name}: attribution header (before the Load line) lacks {part!r}")
    if not failures_since(mark):
        print(f"Attribution OK ({len(LICENSE_FILES)} licence files, SKILL.md and references carry the credit)")


def check_script() -> None:
    if not SCRIPT.is_file():
        fail("scripts/rgs_lookup.py is missing")
        return
    try:
        py_compile.compile(str(SCRIPT), doraise=True)
        print("scripts/rgs_lookup.py compiles")
    except py_compile.PyCompileError as exc:
        fail(f"scripts/rgs_lookup.py does not compile: {exc}")


def main() -> int:
    check_skill()
    check_reference_links()
    check_references()
    check_attribution()
    check_script()
    if errors:
        print(f"\n{len(errors)} guardrail failure(s).")
        return 1
    print("\nAll skill guardrails passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
