"""newscientist.com-specific coverage check + style reference for the digest prompt.

The general media filter (`media_filter.py`) checks whether any outlet has
already covered a candidate. That's necessary but not sufficient here: a study
can clear the general filter (fewer than `media_threshold` outlets) and still
be something New Scientist itself already ran, and an editor won't buy a pitch
for a story their own desk covered last week even if nobody else picked it up.

Two jobs, both scoped to newscientist.com specifically:

1. **Recency/overlap.** `check_ns_overlap` runs a `site:newscientist.com`
   SerpAPI search per candidate (same request/retry/rate-limit shape as
   `media_filter.apply_media_filter`) and drops anything with `threshold`+
   hits — New Scientist has already told this story recently.
2. **Style reference.** `fetch_ns_style_examples` pulls a handful of real,
   currently-published New Scientist headlines and snippets in the run's
   subject area, once per run rather than per candidate, so the digest prompt
   can show Claude how New Scientist actually frames a story instead of asking
   it to guess at house style from nothing.

Both degrade gracefully: with no SERPAPI_KEY, `check_ns_overlap` waves every
candidate through labelled unverified (the same convention as
media_filter.py), and `fetch_ns_style_examples` returns an empty list, which
digest_generator.py treats as "no reference available" rather than an error.
"""

import re
import time
import requests

SERPAPI_URL = "https://serpapi.com/search.json"
SERPAPI_DELAY = 1.0
UNVERIFIED_NOTE = "Not verified — no SerpAPI key configured"


def _ns_search(query: str, api_key: str, num: int = 5) -> list[dict]:
    """Raw organic results for a `site:newscientist.com` SerpAPI web search.

    Uses the "google" engine rather than "google_news" (media_filter.py's
    choice) because a site-scoped search needs the `site:` operator applied to
    a general web search, and the organic results carry a title + snippet per
    hit — exactly what the style-reference use needs, not just a count.
    Raises on request/parse failure so callers decide how to handle it.
    """
    resp = requests.get(
        SERPAPI_URL,
        params={
            "engine": "google",
            "q": f"site:newscientist.com {query}",
            "num": num,
            "api_key": api_key,
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json().get("organic_results", [])


def check_ns_overlap(
    candidates: list[dict],
    api_key: str,
    threshold: int = 2,
    max_lookups: int = 60,
) -> tuple[list[dict], dict[str, str]]:
    """Drop candidates newscientist.com has already covered `threshold`+ times.

    Mirrors `media_filter.apply_media_filter`'s contract: returns
    (surviving_candidates, ns_note_by_pmid). The notes are handed to the digest
    prompt so each entry can state what this check actually found, the same
    way the general media check does.
    """
    if not api_key:
        print("  No SERPAPI_KEY set — skipping newscientist.com overlap check")
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

        try:
            results = _ns_search(candidate["title"], api_key)
            hits = len(results)
        except Exception as e:
            print(f"  NS.com check error for '{candidate['title'][:60]}...': {e}")
            hits = -1
        time.sleep(SERPAPI_DELAY)

        if hits == -1:
            passed.append(candidate)
            notes[candidate["pmid"]] = "Not verified — SerpAPI lookup failed"
        elif hits < threshold:
            passed.append(candidate)
            notes[candidate["pmid"]] = f"No recent NS.com coverage found ✓ ({hits} hits)"
        else:
            skipped += 1
            print(f"  PMID {candidate['pmid']}: {hits} newscientist.com hits — dropped")

    print(f"  NS.com overlap check: {len(passed)} passed, {skipped} already on newscientist.com")
    return passed, notes


def fetch_ns_style_examples(subject_focus: str, api_key: str, max_examples: int = 5) -> list[dict]:
    """A handful of real, currently-published New Scientist headlines + snippets
    in this run's subject area, for the digest prompt to use as a style
    reference (headline conventions, tone, structure) — not as content to
    copy. Falls back to a broad mind/brain query on a broad (no-focus) run, so
    the reference set is never empty just because the topic itself is broad.

    Returns [] on no key, a failed lookup, or no results — a missing style
    reference degrades to "write from the system prompt's own guidance alone",
    not an error.
    """
    if not api_key:
        return []

    query = subject_focus if subject_focus else "mind brain psychology neuroscience"
    try:
        results = _ns_search(query, api_key, num=max_examples)
    except Exception as e:
        print(f"  NS style example fetch failed: {e}")
        return []

    examples = []
    for r in results[:max_examples]:
        # SerpAPI titles for newscientist.com pages carry a " - New Scientist"
        # suffix; strip it so the reference reads as a headline, not a <title> tag.
        headline = re.sub(r"\s*[-|]\s*New Scientist\s*$", "", (r.get("title") or "").strip())
        snippet = (r.get("snippet") or "").strip()
        if headline:
            examples.append({"headline": headline, "snippet": snippet, "link": r.get("link", "")})
    return examples
