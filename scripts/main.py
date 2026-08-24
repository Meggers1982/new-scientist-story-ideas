"""Daily New Scientist story-ideas pipeline — entry point for GitHub Actions."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from journals import ISSNS
from pubmed import search_by_issns, fetch_summaries, fetch_abstracts_for_pmids
from screening import screen
from media_filter import apply_media_filter
from digest_generator import generate_digest
from fact_checker import run_fact_check
from trends import generate_trends_section
from build_dashboard_data import main as rebuild_dashboard_data
from build_aggregator_feed import main as rebuild_aggregator_feed


REPO_ROOT = Path(__file__).parent.parent
OUTPUTS_DIR = REPO_ROOT / "outputs"
TOPIC_MEMORY_DIR = REPO_ROOT / "topic_memory"
CONFIG_PATH = REPO_ROOT / "config" / "digest_config.json"
SEEN_PMIDS_PATH = REPO_ROOT / "seen_pmids.json"

# Fallback if config/digest_config.json is missing a rotation. Kept in sync with
# the config file — see the README on why each topic is on the list.
DEFAULT_FOCUS_ROTATION = [
    "",                       # Broad — all mind and brain topics
    "depression",
    "memory",
    "sleep",
    "anxiety",
    "autism",
    "schizophrenia",
    "trauma",
    "decision-making",
    "stress",
    "bipolar",
    "emotion regulation",
    "artificial intelligence",
    "ADHD",
    "psychotherapy",
    "neuroimaging",
    "addiction",
    "social media",
    "exercise",
    "dementia",
]


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


def pick_subject_focus(config: dict) -> str:
    """Pick today's subject focus.

    Priority:
      1. DIGEST_FOCUS env var (set by workflow_dispatch input)
      2. config["subject_focus"] if non-empty string
      3. config["focus_rotation"] list, rotated by day-of-year
      4. DEFAULT_FOCUS_ROTATION, rotated by day-of-year
    """
    override = os.environ.get("DIGEST_FOCUS", "").strip()
    if override:
        return override

    fixed = config.get("subject_focus", "").strip()
    if fixed:
        return fixed

    rotation = config.get("focus_rotation") or DEFAULT_FOCUS_ROTATION
    if not rotation:
        return ""

    day = datetime.now().timetuple().tm_yday
    focus = rotation[day % len(rotation)]
    print(f"Rotating focus #{day % len(rotation)}: '{focus or '(broad)'}'")
    return focus


def load_seen_pmids() -> set[str]:
    """PMIDs already written up in a previous digest.

    A study that has been pitched once is not a new story idea, so these are
    dropped before screening rather than resurfacing every time a topic comes
    back around the rotation.
    """
    if not SEEN_PMIDS_PATH.exists():
        return set()
    try:
        return set(json.loads(SEEN_PMIDS_PATH.read_text()).get("pmids", []))
    except (json.JSONDecodeError, OSError) as e:
        print(f"  Warning: could not read seen_pmids.json ({e}) — treating as empty")
        return set()


def save_seen_pmids(seen: set[str]) -> None:
    SEEN_PMIDS_PATH.write_text(
        json.dumps(
            {"updated": datetime.now().strftime("%Y-%m-%d"), "pmids": sorted(seen)},
            indent=2,
        ),
        encoding="utf-8",
    )


def unique_output_path(base_path: Path) -> Path:
    if not base_path.exists():
        return base_path
    stem, suffix, parent = base_path.stem, base_path.suffix, base_path.parent
    for n in range(2, 20):
        candidate = parent / f"{stem} (Part {n}){suffix}"
        if not candidate.exists():
            return candidate
    return base_path


def main() -> None:
    # ── Environment ──────────────────────────────────────────────────────────
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    ncbi_api_key = os.environ.get("NCBI_API_KEY") or None
    serpapi_key = os.environ.get("SERPAPI_KEY", "")

    if not anthropic_api_key:
        sys.exit("ERROR: ANTHROPIC_API_KEY is not set.")

    # ── Config ───────────────────────────────────────────────────────────────
    config = load_config()
    subject_focus = pick_subject_focus(config)
    publication = config.get("publication", "New Scientist")
    section = config.get("section", "New Scientist Mind")
    reader_profile = config.get("reader_profile", "curious general readers")
    days_back = config.get("days_back", 30)
    media_threshold = config.get("media_threshold", 3)
    max_candidates = config.get("max_candidates", 60)
    max_abstracts = config.get("max_abstracts", 40)

    print(f"\n{'=' * 60}")
    print(f"Story Ideas Pipeline — {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Journals  : {len(ISSNS)} mental health and brain science journals")
    print(f"Focus     : {subject_focus or '(broad — all mind and brain topics)'}")
    print(f"Target    : {publication} / {section}")
    print(f"{'=' * 60}\n")

    OUTPUTS_DIR.mkdir(exist_ok=True)
    seen_pmids = load_seen_pmids()
    print(f"{len(seen_pmids)} PMIDs already covered by previous digests\n")

    # ── Step 1: Search PubMed by ISSN ────────────────────────────────────────
    print("Searching PubMed across all mind and brain journals...")
    pmids = search_by_issns(
        issns=ISSNS,
        days_back=days_back,
        subject_focus=subject_focus,
        max_per_batch=25,
        max_total=300,
        ncbi_api_key=ncbi_api_key,
    )
    print(f"Found {len(pmids)} article IDs")

    if not pmids:
        print("No articles found. Exiting.")
        sys.exit(0)

    # ── Step 2: Fetch summaries and screen on title ──────────────────────────
    print("\nFetching summaries...")
    summaries = fetch_summaries(pmids, ncbi_api_key=ncbi_api_key)
    print(f"Fetched {len(summaries)} summaries")

    candidates = screen(summaries, already_covered=seen_pmids, max_candidates=max_candidates)
    print(f"{len(candidates)} candidates after screening")

    if not candidates:
        print("Nothing survived screening. Exiting.")
        sys.exit(0)

    # ── Step 3: Drop anything the press already has ──────────────────────────
    print("\nChecking existing media coverage...")
    candidates, media_notes = apply_media_filter(
        candidates, api_key=serpapi_key, threshold=media_threshold
    )

    if not candidates:
        print("Every candidate was already widely covered. Exiting.")
        sys.exit(0)

    # ── Step 4: Fetch abstracts ──────────────────────────────────────────────
    shortlist = [c["pmid"] for c in candidates[:max_abstracts]]
    print(f"\nFetching abstracts (up to {max_abstracts})...")
    abstracts = fetch_abstracts_for_pmids(shortlist, ncbi_api_key=ncbi_api_key)
    print(f"Retrieved {len(abstracts)} abstracts with usable content")

    if not abstracts:
        print("No usable abstracts. Exiting.")
        sys.exit(0)

    # ── Step 5: Generate digest ──────────────────────────────────────────────
    print("\nGenerating digest...")
    digest_content, selected_pmids = generate_digest(
        subject_focus=subject_focus,
        publication=publication,
        section=section,
        reader_profile=reader_profile,
        abstracts=abstracts,
        media_notes=media_notes,
        journal_count=len(ISSNS),
        days_back=days_back,
        api_key=anthropic_api_key,
    )
    print(f"Digest generated — {len(selected_pmids)} studies selected")

    month_year = datetime.now().strftime("%B %Y")
    focus_tag = f" — {subject_focus.title()}" if subject_focus else ""
    digest_filename = f"New Scientist Story Ideas{focus_tag} — {month_year}.md"
    digest_path = unique_output_path(OUTPUTS_DIR / digest_filename)

    # ── Step 6: Run fact checker ─────────────────────────────────────────────
    print("\nRunning fact checker...")
    fact_check_content = run_fact_check(
        digest_content=digest_content,
        selected_pmids=selected_pmids,
        ncbi_api_key=ncbi_api_key,
        anthropic_api_key=anthropic_api_key,
        subject_focus=subject_focus,
    )

    fact_check_path = OUTPUTS_DIR / (digest_path.stem + " Fact Check.md")
    fact_check_path.write_text(fact_check_content, encoding="utf-8")
    print(f"Fact check saved: outputs/{fact_check_path.name}")

    # ── Step 7: Compare against the prior digest on this topic ───────────────
    print("\nGenerating trends & continuity section...")
    trends_section = generate_trends_section(
        subject_focus=subject_focus,
        digest_content=digest_content,
        outputs_dir=OUTPUTS_DIR,
        memory_dir=TOPIC_MEMORY_DIR,
        api_key=anthropic_api_key,
    )
    digest_content = digest_content.rstrip() + "\n\n---\n\n" + trends_section + "\n"

    digest_path.write_text(digest_content, encoding="utf-8")
    print(f"Digest saved: outputs/{digest_path.name}")

    # ── Step 8: Record what was covered so it isn't pitched twice ────────────
    save_seen_pmids(seen_pmids | set(selected_pmids))
    print(f"Recorded {len(selected_pmids)} PMIDs as covered")

    # ── Step 9: Rebuild dashboard data ───────────────────────────────────────
    print("\nRebuilding dashboard data...")
    rebuild_dashboard_data()

    # ── Step 10: Refresh the feed research-digest-dashboard pulls ────────────
    print("\nRebuilding aggregator feed...")
    rebuild_aggregator_feed()

    print("\nDone ✓")


if __name__ == "__main__":
    main()
