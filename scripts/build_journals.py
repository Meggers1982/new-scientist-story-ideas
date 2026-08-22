"""Regenerate scripts/journals.py from the curated journal CSV.

The CSV (`data/Mental Health - Brain Mental Health.csv`) is the editable source
of truth — add or remove a journal there, then run this to rebuild the module
the pipeline imports:

    python3 scripts/build_journals.py

Rows with neither a print nor an electronic ISSN are dropped, because the
PubMed query is built entirely from ISSNs and such a row would be invisible
to it either way.
"""

import csv
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CSV_PATH = REPO_ROOT / "data" / "Mental Health - Brain Mental Health.csv"
OUT_PATH = REPO_ROOT / "scripts" / "journals.py"

HEADER = '''"""Mental health and brain science journal ISSNs, generated from
`data/Mental Health - Brain Mental Health.csv`.

Regenerate with `python3 scripts/build_journals.py` after editing the CSV.
"""

# (journal_name, issn, [NLM categories]) — prefers the electronic ISSN,
# falls back to print. Rows with no ISSN at all are dropped.
MIND_JOURNALS: list[tuple[str, str, list[str]]] = [
'''

FOOTER = ''']

ISSNS: list[str] = [issn for _, issn, _ in MIND_JOURNALS]

CATEGORIES: list[str] = sorted({c for _, _, cats in MIND_JOURNALS for c in cats})
'''


def main() -> None:
    rows: list[tuple[str, str, list[str]]] = []
    seen: set[str] = set()
    dropped: list[str] = []

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            issn = (row.get("ISSN (Online)") or "").strip() or (row.get("ISSN (Print)") or "").strip()
            title = (row.get("Journal Title") or "").strip().rstrip(".")
            cats = [c.strip() for c in (row.get("Categories") or "").split(";") if c.strip()]
            if not issn:
                dropped.append(title)
                continue
            if issn in seen:
                continue
            seen.add(issn)
            rows.append((title, issn, cats))

    body = "".join(f"    ({t!r}, {i!r}, {c!r}),\n" for t, i, c in rows)
    OUT_PATH.write_text(HEADER + body + FOOTER, encoding="utf-8")

    print(f"Wrote {len(rows)} journals to {OUT_PATH.relative_to(REPO_ROOT)}")
    if dropped:
        print(f"Dropped {len(dropped)} row(s) with no ISSN: {', '.join(dropped)}")


if __name__ == "__main__":
    main()
