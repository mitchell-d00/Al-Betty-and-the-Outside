"""Rebuild the two current PDF documents; never rewrite the historical PDF/ZIP."""

import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://github.com/mitchell-d00/Al-Betty-and-the-Outside/blob/main/"
SOURCES = (
    ("papers/archive/Empirical-Al-Betty-and-the-Outside-2026-11-27.md",
     "Empirical Al, Betty and the Outside"),
    ("papers/TeamBuilding-Governance-Prompt.md", "TeamBuilding Governance Prompt"),
)


def pdf_text(source):
    text = source.read_text(encoding="utf-8")
    text = re.sub(r"\A# [^\n]+\n", "", text, count=1)
    text = re.sub(r"^\*\*Mitchell D[^\n]*\n", "", text, count=1, flags=re.M)

    def link(match):
        target = match.group(1)
        if "://" in target or target.startswith(("#", "mailto:")):
            return match.group(0)
        name, _, anchor = target.partition("#")
        path = (source.parent / name).resolve().relative_to(ROOT).as_posix()
        url = BASE_URL + quote(path)
        return "](" + url + ("#" + anchor if anchor else "") + ")"

    text = re.sub(r"\]\(([^)]+)\)", link, text)
    # Keep these short tables together instead of leaving two rows over a page.
    lines = text.splitlines()
    result = []
    for index, line in enumerate(lines):
        if line.startswith("|") and index + 1 < len(lines) and re.fullmatch(r"[| :\-]+", lines[index + 1]):
            result.extend([r"\needspace{10\baselineskip}", ""])
        result.append(line)
    return "\n".join(result) + "\n"


def main():
    with tempfile.TemporaryDirectory(prefix="teambuilding-font-cache-") as cache:
        environment = dict(os.environ, SOURCE_DATE_EPOCH="1795737600", XDG_CACHE_HOME=cache)
        header = Path(cache) / "layout.tex"
        header.write_text(r"\usepackage{needspace}" + "\n", encoding="utf-8")
        for name, title in SOURCES:
            source = ROOT / name
            command = [
                "pandoc", "--from=markdown+smart", "--standalone", "--pdf-engine=xelatex",
                "--include-in-header", str(header),
                "-V", "geometry:margin=0.8in", "-V", "fontsize=10pt",
                "-V", "mainfont=DejaVu Serif", "-V", "monofont=DejaVu Sans Mono",
                "-V", "colorlinks=true", "-V", "urlcolor=blue",
                "-M", f"title={title}", "-M", "author=Mitchell D. McPhetridge",
                "-M", "date=27 November 2026", "--output", str(source.with_suffix(".pdf")),
            ]
            subprocess.run(command, input=pdf_text(source), text=True, cwd=ROOT,
                           env=environment, check=True)
            print(source.with_suffix(".pdf").relative_to(ROOT))


if __name__ == "__main__":
    main()
