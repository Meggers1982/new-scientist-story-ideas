"""Generate a New Scientist story-ideas digest using the Claude API."""

import json
import re
from datetime import datetime

import anthropic

from llm import MODEL, call, response_text


SYSTEM_PROMPT = """\
You are a commissioning editor's research assistant, building a shortlist of story
ideas for [PUBLICATION] — specifically its [SECTION] desk. You will be given PubMed
abstracts sourced exclusively from peer-reviewed mental health, psychiatry, and brain
science journals, pre-screened for novelty signals and for not having been widely
covered in the news already.

Select the studies that would genuinely make a story and write a structured entry for
each one.

## Selection criteria
- Prioritize: human-subjects studies, RCTs, large cohorts, longitudinal data,
  pre-registered work, and replications (successful or failed)
- Favor the counterintuitive, the first-of-its-kind, and the result that overturns
  something readers think they already know
- A finding is more pitchable when a reader can picture themselves in it — their
  memory, sleep, mood, attention, habits, relationships
- Skip: editorials, letters, methodology-only papers, animal-only work, incremental
  confirmations of well-established findings, and anything whose only news value is
  that it was published

## Scoring
Give every entry an **NS fit** score from 1 to 10 for how well it suits [PUBLICATION]:
how surprising the result is, how solid the evidence is, and how easily it becomes a
600-word story. Be honest and use the range — a 9 should be rare. Do not include any
study you would score below 4; leave it out of the digest entirely.

## Matching New Scientist's own style
When real, currently-published New Scientist headlines are supplied below as a style
reference, write each entry's headline and Pitch angle to match their conventions —
tone, structure, how much (or how little) hype they carry — rather than a generic
science-news voice. Use them as a model to write like, never as content to copy or
reference by name. If no style reference is supplied, fall back to the entry-format
instructions below on their own.


## Spelling
Write in American English: "analyze", "behavior", "randomized", "center", "program",
"generalize". Many of these journals are British and their abstracts are not written
that way — convert as you write in your own voice. Never change spelling inside
something reproduced verbatim: journal titles (e.g. *Behaviour Research and Therapy*),
trial, instrument and cohort names, and direct quotations keep their original form.

## Entry format (use this exactly for every selected study)

### [Number]. [Compelling, plain-language headline — present tense, no hype]

**Journal:** *Name* | **Published:** Date
**PMID:** [ID] | **DOI:** [DOI or "Not available"]
**Novelty:** [Counterintuitive | Overturns prior research | First-in-class | Failed replication | New mechanism]
**NS fit:** [N]/10 — [one clause on what lifts or limits the score]
**Media check:** [copy the media-check line supplied for this PMID verbatim]
**NS.com check:** [copy the NS.com-check line supplied for this PMID verbatim]

**The study:** What researchers did, who participants were (N=, age range), key
finding in plain language. 2–4 sentences.

**Why it matters:** What this changes about how we understand the mind or brain, and
for whom. 1–2 sentences. No inflation — if the honest answer is "not much yet, but
it opens a line of enquiry", say that.

**Story angles:**
- **Pitch angle:** How you would sell this to [PUBLICATION]'s [SECTION] desk. Lead with
  the surprise. Name the hook, the person or scenario the piece would open on, and the
  one researcher or group worth calling. Do NOT imply clinical action based on
  observational data alone.
- **Wider angle:** A different, larger framing — a feature, a trend piece, or a story
  for a general-interest or specialist outlet other than [PUBLICATION]. Name the angle
  and say which kind of outlet it fits. Must be a genuinely different story, not a
  rewording of the pitch angle.

**Caveats:** Flag any that apply — small N (under 100 for quantitative studies),
single-center, observational design (cannot establish causation), industry funding
(name the funder), self-reported outcomes, population may not generalize, short
follow-up, no control group, preprint or secondary analysis. Write "None significant"
if none apply.

---

After all entries, write a citation table:

## Citation Reference

| # | PMID | Journal | Date | DOI |
|---|------|---------|------|-----|
[one row per entry]

Do not include your own top-level title or heading (e.g. a line starting with
"# New Scientist Story Ideas") anywhere in your response — the output file already
has this title in its header. Start directly with the first entry.

Finally, append a JSON block (used internally — do not explain it):
```json
{"selected_pmids": ["pmid1", "pmid2"]}
```
"""

# Thinking tokens share this budget with the visible digest, so it is well above
# what the markdown alone needs.
MAX_TOKENS = 32000
MAX_CONTINUATIONS = 3
CONTINUATION_PROMPT = (
    "Continue exactly where you left off. Do not repeat any content already "
    "written, and do not restart from the beginning."
)


def generate_digest(
    subject_focus: str,
    publication: str,
    section: str,
    reader_profile: str,
    abstracts: dict[str, str],
    media_notes: dict[str, str],
    journal_count: int,
    days_back: int,
    api_key: str,
    ns_notes: dict[str, str] | None = None,
    ns_style_examples: list[dict] | None = None,
    model: str = MODEL,
) -> tuple[str, list[str]]:
    """Generate a formatted story-ideas digest from PubMed abstracts.

    `ns_notes` and `ns_style_examples` come from `ns_check.py`'s
    newscientist.com-specific checks: per-PMID overlap notes (same shape as
    `media_notes`) and, separately, a handful of real current New Scientist
    headlines used as a style reference. Both are optional — a caller that
    doesn't pass them gets the general media-filter behaviour only, same as
    before this was added.

    Returns:
        (full_digest_markdown, list_of_selected_pmids)
    """
    client = anthropic.Anthropic(api_key=api_key)

    run_date = datetime.now().strftime("%Y-%m-%d")

    focus_label = subject_focus if subject_focus else "Broad (all mind and brain topics)"
    header = "\n".join([
        "# New Scientist Story Ideas",
        f"**Run date:** {run_date} | **Coverage window:** Last {days_back} days",
        f"**Journals searched:** {journal_count} | **Articles screened:** {len(abstracts)}",
        f"**Focus:** {focus_label}",
        f"**Publication:** {publication} | **Section:** {section}",
    ]) + "\n\n---\n\n"

    if not abstracts:
        return header + "_No articles with usable abstracts were found for this run._", []

    ns_notes = ns_notes or {}
    abstracts_block = "\n\n".join(
        f"--- PMID {pmid} ---\n"
        f"Media check: {media_notes.get(pmid, 'Not verified')}\n"
        f"NS.com check: {ns_notes.get(pmid, 'Not verified')}\n\n{text}"
        for pmid, text in abstracts.items()
    )

    system = (
        SYSTEM_PROMPT
        .replace("[PUBLICATION]", publication)
        .replace("[SECTION]", section)
    )

    style_block = ""
    if ns_style_examples:
        examples_text = "\n".join(
            f'- "{ex["headline"]}"' + (f" — {ex['snippet']}" if ex.get("snippet") else "")
            for ex in ns_style_examples
        )
        style_block = (
            "\n**Style reference — real, currently-published New Scientist headlines in this "
            "subject area** (write your own headlines and pitch angles to match their "
            "conventions; do not copy their content or phrasing):\n"
            f"{examples_text}\n"
        )

    focus_line = f"**Subject focus:** {subject_focus}\n" if subject_focus else ""
    user_message = (
        f"Please build a story-ideas digest from the {len(abstracts)} abstracts below.\n\n"
        f"**Publication:** {publication}\n"
        f"**Section:** {section}\n"
        f"**Readers:** {reader_profile}\n"
        + focus_line
        + style_block
        + "\nInclude every study you would score 4 or above — do not cap the count. "
        "Leave out everything you would score below 4.\n\n"
        f"{'=' * 60}\n"
        f"{abstracts_block}\n"
        f"{'=' * 60}"
    )

    # Cache the system prompt and the (large) initial abstracts message so that
    # continuation retries below re-read this prefix from cache instead of
    # reprocessing it at full price on every retry. Continuation turns are small
    # and left uncached to keep the request under the API's breakpoint limit.
    system_blocks = [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
    messages = [
        {
            "role": "user",
            "content": [{"type": "text", "text": user_message, "cache_control": {"type": "ephemeral"}}],
        }
    ]
    response = call(
        client,
        model=model,
        max_tokens=MAX_TOKENS,
        system=system_blocks,
        messages=messages,
    )
    chunk = response_text(response)
    body = chunk

    continuations = 0
    while response.stop_reason == "max_tokens" and continuations < MAX_CONTINUATIONS:
        # Echo back only THIS turn's partial text as the assistant message —
        # not the full accumulated body — so the conversation history mirrors
        # what actually happened turn-by-turn and doesn't duplicate content.
        messages.append({"role": "assistant", "content": chunk})
        messages.append({"role": "user", "content": CONTINUATION_PROMPT})
        response = call(
            client,
            model=model,
            max_tokens=MAX_TOKENS,
            system=system_blocks,
            messages=messages,
        )
        chunk = response_text(response)
        body += chunk
        continuations += 1

    if response.stop_reason == "max_tokens":
        print(
            "  WARNING: digest response still truncated after "
            f"{MAX_CONTINUATIONS} continuation(s) — output may be incomplete."
        )

    # Extract selected PMIDs from the trailing JSON block (search the full
    # accumulated text, not just the last continuation chunk)
    selected_pmids = list(abstracts.keys())
    json_match = re.search(r"```json\s*(\{[^`]+\})\s*```", body, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            selected_pmids = data.get("selected_pmids", selected_pmids)
        except json.JSONDecodeError:
            pass
        body = body[: json_match.start()].rstrip()

    # Strip a leading H1 title line if the model included its own (belt and
    # suspenders alongside the system prompt instruction not to) — the file
    # header above already carries this title.
    stripped = body.lstrip("\n")
    first_line_end = stripped.find("\n")
    first_line = stripped if first_line_end == -1 else stripped[:first_line_end]
    if re.match(r"^#\s+.*Story Ideas", first_line.strip()):
        rest = "" if first_line_end == -1 else stripped[first_line_end + 1 :]
        body = rest.lstrip("\n")

    return header + body, selected_pmids
