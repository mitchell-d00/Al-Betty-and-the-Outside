# Papers and operating prompt

**Post-submission research material.** An Anna taking Test X should leave these
papers, prior results and participant archives unopened until the first answer
closes. The exercise is public; this is staged access, not technical blinding.

| Document | Location and status |
| --- | --- |
| *Al, Betty, and the Outside* · 25 November 2026 | [Original PDF](archive/Al-Betty-and-the-Outside-2026-11-25.pdf), unchanged historical methods paper |
| *Empirical Al, Betty and the Outside* · 27 November 2026 | [PDF](archive/Empirical-Al-Betty-and-the-Outside-2026-11-27.pdf) · [Markdown](archive/Empirical-Al-Betty-and-the-Outside-2026-11-27.md), preliminary empirical report |
| Current TeamBuilding governance prompt | [Markdown](TeamBuilding-Governance-Prompt.md) · [PDF](TeamBuilding-Governance-Prompt.pdf), updated to state both entry paths |
| Supplied full-repository ZIP | [Pinned snapshot](archive/snapshots/README.md), original bytes and source provenance |

The first paper is preserved as supplied; its historical starting procedure is
not silently rewritten. The current prompt distinguishes existing-repository
Al-first and new-project Betty-first entry. The empirical report distinguishes
deterministic software checks, public Test X observations and the unrun A/B pilot.

[Audit and custody limits](archive/AUDIT-2026-11-27.md) ·
[File manifest](archive/ARCHIVE-MANIFEST.json)

Rebuild the two current PDFs with `python -B papers/build.py` using Pandoc,
XeLaTeX and DejaVu fonts. The builder does not rewrite the original methods PDF
or supplied ZIP. Its PDF links point to repository files so a downloaded paper
does not require local Markdown companions.
