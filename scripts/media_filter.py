"""SerpAPI 'has this already been covered?' screen.

The senior-research-digest pipeline has no equivalent step, because a digest
written for readers is still useful when the underlying study made the news. A
digest written to generate pitches is not: an editor will not commission a story
The Guardian ran last week. So this screen sits between the cheap title screen
and the expensive abstract fetch, and drops anything already picked up by more
than a couple of outlets.

Degrades gracefully — with no SERPAPI_KEY set, every candidate passes and is
labelled as unverified rather than silently presented as a fresh find.

The same applies when SerpAPI is up but not answering. A circuit breaker
(`serp_breaker`, shared with ns_check.py) stops the screen after a run of
consecutive failures instead of paying the full timeout on every remaining
candidate: on 2026-09-05 every lookup timed out, and retrying through the whole
budget burned ~16 minutes and took the 30-minute job down with it. A screen that
cannot run should cost seconds, not the job.
"""

import os
import time
import requests

try:
    from . import serp_breaker
except ImportError:  # run as a plain script, not a package
    import serp_breaker

SERPAPI_URL = "https://serpapi.com/search.json"
SERPAPI_DELAY = 1.0
SERPAPI_TIMEOUT = int(os.getenv("SERPAPI_TIMEOUT_SECONDS", "15"))
UNVERIFIED_NOTE = "Not verified — no SerpAPI key configured"

# Thresholds and budgets live in serp_breaker, which this screen shares with
# ns_check.py. Sharing matters: they run back to back against the same upstream,
# so a per-screen budget lets the two of them spend twice the ceiling between
# them while each looks well-behaved on its own.
SERP_ENGINE = "google_news"

# Covers both ways the breaker opens — a run of failures, or a time budget spent
# on responses too slow to use. Either way the screen did not verify this
# candidate, which is the only thing the digest prompt needs to know.
CIRCUIT_OPEN_NOTE = "Not verified — SerpAPI unavailable this run"


def _news_hit_count(title: str, api_key: str) -> int:
    """Number of Google News results for this title, or -1 if the lookup failed."""
    try:
        resp = requests.get(
            SERPAPI_URL,
            params={"engine": "google_news", "q": title, "api_key": api_key},
            timeout=SERPAPI_TIMEOUT,
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

        if serp_breaker.is_open(SERP_ENGINE):
            # Upstream is down. Keep the candidate and say so — no call, no sleep.
            passed.append(candidate)
            notes[candidate["pmid"]] = CIRCUIT_OPEN_NOTE
            continue

        with serp_breaker.timed(SERP_ENGINE) as t:
            hits = _news_hit_count(candidate["title"], api_key)
            t.ok = hits != -1

        if hits == -1:
            passed.append(candidate)
            notes[candidate["pmid"]] = "Not verified — SerpAPI lookup failed"
            continue

        time.sleep(SERPAPI_DELAY)

        if hits < threshold:
            passed.append(candidate)
            notes[candidate["pmid"]] = f"Not widely covered ✓ ({hits} news hits)"
        else:
            skipped += 1
            print(f"  PMID {candidate['pmid']}: {hits} news hits — dropped")

    unverified = sum(1 for n in notes.values() if n == CIRCUIT_OPEN_NOTE)
    summary = f"  Media filter: {len(passed)} passed, {skipped} already covered"
    if unverified:
        summary += f", {unverified} unchecked (SerpAPI gave out)"
    print(summary)
    return passed, notes
