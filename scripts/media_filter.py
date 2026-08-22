"""SerpAPI 'has this already been covered?' screen.

The senior-research-digest pipeline has no equivalent step, because a digest
written for readers is still useful when the underlying study made the news. A
digest written to generate pitches is not: an editor will not commission a story
The Guardian ran last week. So this screen sits between the cheap title screen
and the expensive abstract fetch, and drops anything already picked up by more
than a couple of outlets.

Degrades gracefully — with no SERPAPI_KEY set, every candidate passes and is
labelled as unverified rather than silently presented as a fresh find.
"""

import time
import requests

SERPAPI_URL = "https://serpapi.com/search.json"
SERPAPI_DELAY = 1.0
UNVERIFIED_NOTE = "Not verified — no SerpAPI key configured"


def _news_hit_count(title: str, api_key: str) -> int:
    """Number of Google News results for this title, or -1 if the lookup failed."""
    try:
        resp = requests.get(
            SERPAPI_URL,
            params={"engine": "google_news", "q": title, "api_key": api_key},
            timeout=15,
        )
        resp.raise_for_status()
        return len(resp.json().get("news_results", []))
    except Exception as e:
        print(f"  SerpAPI error for '{title[:60]}...': {e}")
        return -1


def apply_media_filter(
    candidates: list[dict],
    api_key: str,
    threshold: int = 3,
    max_lookups: int = 60,
) -> tuple[list[dict], dict[str, str]]:
    """Drop candidates already covered by `threshold`+ news outlets.

    Returns (surviving_candidates, media_note_by_pmid). The notes are handed to
    the digest prompt so each entry can state what the check actually found,
    rather than asserting novelty the pipeline never verified.
    """
    if not api_key:
        print("  No SERPAPI_KEY set — skipping media filter")
        return candidates, {c["pmid"]: UNVERIFIED_NOTE for c in candidates}

    passed: list[dict] = []
    notes: dict[str, str] = {}
    skipped = 0

    for i, candidate in enumerate(candidates):
        if i >= max_lookups:
            # Past the lookup budget: keep the rest, but don't claim they're clean.
            passed.append(candidate)
            notes[candidate["pmid"]] = "Not verified — past this run's SerpAPI lookup budget"
            continue

        hits = _news_hit_count(candidate["title"], api_key)
        time.sleep(SERPAPI_DELAY)

        if hits == -1:
            passed.append(candidate)
            notes[candidate["pmid"]] = "Not verified — SerpAPI lookup failed"
        elif hits < threshold:
            passed.append(candidate)
            notes[candidate["pmid"]] = f"Not widely covered ✓ ({hits} news hits)"
        else:
            skipped += 1
            print(f"  PMID {candidate['pmid']}: {hits} news hits — dropped")

    print(f"  Media filter: {len(passed)} passed, {skipped} already covered")
    return passed, notes
