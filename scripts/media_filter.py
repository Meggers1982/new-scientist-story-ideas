"""SerpAPI 'has this already been covered?' screen.

The senior-research-digest pipeline has no equivalent step, because a digest
written for readers is still useful when the underlying study made the news. A
digest written to generate pitches is not: an editor will not commission a story
The Guardian ran last week. So this screen sits between the cheap title screen
and the expensive abstract fetch, and drops anything already picked up by more
than a couple of outlets.

Degrades gracefully — with no SERPAPI_KEY set, every candidate passes and is
labelled as unverified rather than silently presented as a fresh find.

The same applies when SerpAPI is up but not answering. A circuit breaker stops
the screen after a run of consecutive failures instead of paying the full
timeout on every remaining candidate: on 2026-09-05 every lookup timed out, and
retrying through the whole budget burned ~16 minutes and took the 30-minute job
down with it. A screen that cannot run should cost seconds, not the job.
"""

import os
import time
import requests

SERPAPI_URL = "https://serpapi.com/search.json"
SERPAPI_DELAY = 1.0
SERPAPI_TIMEOUT = int(os.getenv("SERPAPI_TIMEOUT_SECONDS", "15"))
UNVERIFIED_NOTE = "Not verified — no SerpAPI key configured"

# Consecutive failed lookups before the screen gives up for the rest of the run.
# One or two timeouts are noise; three in a row means the upstream is down and
# every further call is just spending the job's time budget to learn that again.
SERPAPI_FAILURE_THRESHOLD = int(os.getenv("SERPAPI_FAILURE_THRESHOLD", "3"))

# Hard ceiling on wall-clock time spent in this screen, regardless of outcome.
# Backstop for slow-but-not-failing responses, which the breaker never sees.
SERPAPI_TIME_BUDGET_SECONDS = float(os.getenv("SERPAPI_TIME_BUDGET_SECONDS", "300"))

CIRCUIT_OPEN_NOTE = "Not verified — SerpAPI unavailable this run"
BUDGET_SPENT_NOTE = "Not verified — past this run's SerpAPI time budget"


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

    started = time.monotonic()
    consecutive_failures = 0
    give_up_note: str | None = None

    for i, candidate in enumerate(candidates):
        if give_up_note:
            # Screen is done for this run. Keep the candidate, say why it's unchecked.
            passed.append(candidate)
            notes[candidate["pmid"]] = give_up_note
            continue

        if i >= max_lookups:
            # Past the lookup budget: keep the rest, but don't claim they're clean.
            passed.append(candidate)
            notes[candidate["pmid"]] = "Not verified — past this run's SerpAPI lookup budget"
            continue

        if time.monotonic() - started > SERPAPI_TIME_BUDGET_SECONDS:
            print(
                f"  Media filter: {SERPAPI_TIME_BUDGET_SECONDS:.0f}s time budget spent "
                f"after {i} lookup(s) — skipping the rest"
            )
            give_up_note = BUDGET_SPENT_NOTE
            passed.append(candidate)
            notes[candidate["pmid"]] = give_up_note
            continue

        hits = _news_hit_count(candidate["title"], api_key)

        if hits == -1:
            consecutive_failures += 1
            passed.append(candidate)
            notes[candidate["pmid"]] = "Not verified — SerpAPI lookup failed"

            if consecutive_failures >= SERPAPI_FAILURE_THRESHOLD:
                print(
                    f"  Media filter: {consecutive_failures} consecutive SerpAPI "
                    f"failures — giving up on the screen for this run"
                )
                give_up_note = CIRCUIT_OPEN_NOTE
            else:
                time.sleep(SERPAPI_DELAY)
            continue

        consecutive_failures = 0
        time.sleep(SERPAPI_DELAY)

        if hits < threshold:
            passed.append(candidate)
            notes[candidate["pmid"]] = f"Not widely covered ✓ ({hits} news hits)"
        else:
            skipped += 1
            print(f"  PMID {candidate['pmid']}: {hits} news hits — dropped")

    unverified = sum(
        1 for n in notes.values() if n in (CIRCUIT_OPEN_NOTE, BUDGET_SPENT_NOTE)
    )
    summary = f"  Media filter: {len(passed)} passed, {skipped} already covered"
    if unverified:
        summary += f", {unverified} unchecked (SerpAPI gave out)"
    print(summary)
    return passed, notes
