# New Scientist Story Ideas

Automated pipeline that searches PubMed for recent mental health and brain
science research, drops anything the press already has, uses Claude to write a
pitchable story-ideas digest, fact-checks its own output against the source
abstracts, and publishes every run to a browsable dashboard —
**https://meggers1982.github.io/new-scientist-story-ideas/**

Built on the same methodology as
[senior-research-digest](https://github.com/Meggers1982/senior-research-digest):
one sequential pipeline per day, a rotating subject focus, markdown digests that
accumulate in `outputs/` and are never overwritten, a self-fact-check pass, and a
per-topic memory file that gives the trends section a longer horizon than the
last run. The differences from that repo are noted in **Where this differs**
below.

## How it works

`.github/workflows/daily-digest.yml` runs `scripts/main.py` on a daily cron
(12:00 UTC / 07:00 ET) via GitHub Actions. Each run:

1. **Searches PubMed** (`pubmed.py`) across 325 curated mental health, psychiatry
   and brain science journals (`journals.py`) for articles from the last 30 days,
   optionally filtered to a subject focus.
2. **Picks today's focus** — either a manual override, a fixed topic from
   `config/digest_config.json`, or the next topic in the daily rotation
   (`main.py`'s `DEFAULT_FOCUS_ROTATION` / `config["focus_rotation"]`).
3. **Screens cheaply** (`screening.py`) — drops studies already covered by a
   previous digest, plus editorials, errata and animal-only work, then ranks the
   rest by how strongly the title signals novelty.
4. **Drops what's already been reported** (`media_filter.py`) — checks each
   candidate against Google News via SerpAPI and discards anything with 3+ hits.
5. **Generates the digest** (`digest_generator.py`) — Claude selects the most
   pitchable studies from up to 40 abstracts and writes a structured entry for
   each (headline, novelty type, NS fit score, study summary, why it matters,
   pitch angle, wider angle, caveats).
6. **Fact-checks itself** (`fact_checker.py`) — a second Claude pass compares
   every entry against the original abstract and flags inaccuracies with a
   ✅/⚠️/❌ verdict per study. It also challenges the NS fit score.
7. **Compares against history** (`trends.py`) — Claude compares the new digest to
   the most recent prior digest on the same topic and to a running per-topic
   memory file (`topic_memory/<topic>.md`), producing a "Research Trends &
   Continuity" section plus a "Bigger Picture: Feature Pitch" if the batch
   suggests a larger story, with 3-4 real outlets that specific angle could go to.
8. **Records what it covered** — selected PMIDs go into `seen_pmids.json` so the
   same study is never pitched twice.
9. **Rebuilds the dashboard** (`build_dashboard_data.py`) — parses every digest +
   fact-check in `outputs/` into `docs/data/`.
10. **Commits everything back** — `outputs/`, `topic_memory/`, `docs/` and
    `seen_pmids.json` are committed and pushed by the workflow, so history
    accumulates in the repo and GitHub Pages redeploys automatically.

Nothing is ever overwritten: if two digests would land on the same filename
(e.g. two runs on the same topic in one month), `main.py` appends "(Part N)".

## Where this differs from senior-research-digest

Four deliberate changes, each because this repo generates pitches rather than
reader-facing summaries:

- **A media filter.** A digest written for readers is still useful when the
  study made the news; a pitch is not — an editor won't commission a story the
  Guardian ran last week. `media_filter.py` sits between the title screen and
  the abstract fetch. It degrades gracefully: with no `SERPAPI_KEY` set, every
  candidate passes and is labelled "Not verified" rather than being silently
  presented as a fresh find.
- **A PMID ledger.** `seen_pmids.json` records every study ever written up, and
  those are dropped before screening. A study that has been pitched once is not
  a new story idea. The senior digest has no equivalent, because re-covering a
  finding for a new audience is fine there.
- **Different entry fields.** Its two "story angles" (to/about an audience) are
  replaced by a **Pitch angle** (how to sell it to New Scientist) and a **Wider
  angle** (a different, larger story elsewhere), plus **Novelty**, **NS fit**
  (1-10, honest use of the range) and **Media check** per entry.
- **GitHub Pages, not Vercel.** The senior repo is private, so Pages isn't
  available on the free plan and it deploys to Vercel with Git integration
  deliberately disconnected. This repo is public, so Pages is free and serves
  `/docs` on every push to `main` — no deploy step, no Vercel secrets.

Two portability fixes were also needed at this repo's scale, both worth knowing
if you sync changes back the other way:

- **ISSN batches are sampled round-robin.** The senior pipeline searches ~146
  journals over 90 days and rarely fills its PMID quota, so taking batches in
  order was harmless. Here, 325 journals over 30 days returns 5,000+ articles on
  a broad run, and an in-order fill would exhaust the 300-PMID quota on the first
  two batches — leaving ~275 journals unread every day. `search_by_issns` now
  draws from every batch newest-first and interleaves them.
- **Text is read from all content blocks.** `response.content[0].text` returns
  `""` on Claude Opus 5, because adaptive thinking is on by default and the first
  block is a thinking block. That fails silently — an empty digest, no exception.
  `llm.py`'s `response_text` joins the blocks that actually carry text; all three
  Claude passes go through it.

## Dashboard

`docs/index.html` is a static, no-build dashboard that reads `docs/data/` and
lets you browse **every digest ever generated** — filter by topic, search by
headline/PMID/journal, see each study's NS fit score and fact-check verdict
inline, and export any run to .docx. When a run includes a feature pitch, a
"Jump to Feature Pitch" link appears in the run header.

The data is split so first load stays flat as runs accumulate: `data/index.json`
holds only what the sidebar and search box need, and each run's full body lives
in `data/runs/<id>.json`, fetched on demand when that run is opened.

GitHub Pages serves the `/docs` folder of `main`, so a push is a deploy. To view
it locally without pushing:

```bash
cd docs && python3 -m http.server 8000
# open http://localhost:8000
```

To rebuild the dashboard data by hand (e.g. after editing a past digest):

```bash
python3 scripts/build_dashboard_data.py
```

This parser expects the exact markdown structure Claude is instructed to produce
in `digest_generator.py`'s `SYSTEM_PROMPT` (`### N. Headline`, `**Journal:**`,
`**PMID:**`, `**NS fit:**`, `**Story angles:**` with `Pitch angle`/`Wider angle`
bullets, etc.) and `fact_checker.py`'s per-study verdict line
(`**PMID:** ... | **Verdict:** ...`). If either prompt's output format changes,
update the corresponding regexes in `build_dashboard_data.py` too.

## The archive

This repo previously ran a different pipeline that accumulated every screened
study into a single `data/results.json` — 904 studies. That file is preserved
verbatim at `archive/legacy-results.json`.

`scripts/migrate_legacy_results.py` back-converted the 778 of those published
within 60 days of the cutover into 46 markdown digests in `outputs/`, one per
original run date, so the dashboard has history from day one. They are stamped
`**Source:** Converted from the previous JSON pipeline` and carry no trends
section and no per-study fact-check verdicts, because the old pipeline never
produced those — those fields render as "—" rather than being invented. The old
pipeline's nested `ns_pitch` object is flattened into the Pitch angle field;
Wider angle reads "Not generated by the previous pipeline."

All 904 PMIDs — not just the converted ones — were written into
`seen_pmids.json`, so nothing the old pipeline covered can be pitched again.

The migration is a one-time script that has already been run. It skips files
that already exist, so re-running it is safe but pointless.

## Running locally

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
export SERPAPI_KEY=...       # optional — without it the media filter is skipped
export NCBI_API_KEY=...      # optional — raises PubMed rate limit from 3 to 10 req/sec
cd scripts
python3 main.py
```

Set `DIGEST_FOCUS` to override today's rotation (e.g.
`DIGEST_FOCUS="sleep" python3 main.py`). An empty value is treated as "no
override" and falls through to the rotation, so the broad digest cannot be forced
this way — it only runs when the rotation lands on it.

A run takes roughly 15-25 minutes, most of it the SerpAPI lookups (1 req/sec, up
to 60) and the three Claude passes.

### Choosing topic wording

A focus is ANDed into the PubMed query as an exact phrase match
(`"<focus>"[Title/Abstract]`) with no synonym or MeSH expansion, so the exact
string decides how many articles a topic can draw from. Measured across all 325
journals over one 30-day window:

| Wording | Articles | | Wording | Articles |
| --- | --- | --- | --- | --- |
| *(broad — no focus)* | 5347 | | `artificial intelligence` | 117 |
| `depression` | 685 | | `ADHD` | 112 |
| `anxiety` | 602 | | `psychotherapy` | 97 |
| `stress` | 509 | | `neuroimaging` | 96 |
| `memory` | 364 | | `addiction` | 89 |
| `sleep` | 360 | | `social media` | 88 |
| `autism` | 214 | | `exercise` | 87 |
| `schizophrenia` | 214 | | `dementia` | 77 |
| `trauma` | 193 | | `loneliness` | 56 |
| `decision-making` | 176 | | `cannabis` | 55 |
| `bipolar` | 124 | | `obsessive-compulsive` | 50 |
| `emotion regulation` | 121 | | `consciousness` | 41 |

Aim for roughly 75+ articles; the pipeline reads up to 40 abstracts. The 20
topics in the rotation are the ones that clear that bar. Measured-but-excluded
topics sit below it and would produce a thin digest on their own —
`psychedelic` (36), `brain stimulation` (30), `ketamine` (22), `adolescent
mental health` (20), `gut microbiome` (8) — they are better reached through the
broad run than as their own rotation slot.

Note that closely related phrasings pull largely separate literature — a topic is
only as broad as its literal string.

Renaming a rotation topic breaks two continuity links, both keyed to the focus
string: `topic_memory/<slug>.md` (rename the file to match) and the prior-digest
lookup in `trends.py`, which matches the `Focus` field exactly and so will not
see digests filed under the old name.

## Configuration

Edit `config/digest_config.json` and commit — the next run picks it up:

- `publication` / `section` — who the pitch angles are written for.
- `reader_profile` — the readership the digest is told to write toward.
- `subject_focus` — leave empty to rotate through `focus_rotation` daily, or set
  a fixed topic to always search that one.
- `focus_rotation` — the list of topics rotated through by day-of-year.
- `days_back` — PubMed lookback window (days).
- `media_threshold` — news hits at or above which a study is dropped as already
  covered.
- `max_candidates` — how many screened studies go to the media filter.
- `max_abstracts` — how many survivors get full abstracts fetched and sent to
  Claude.

### The journal list

`data/Mental Health - Brain Mental Health.csv` is the editable source of truth.
Edit it, then regenerate the module the pipeline imports:

```bash
python3 scripts/build_journals.py
```

Rows with neither a print nor an electronic ISSN are dropped, since the PubMed
query is built entirely from ISSNs.

## Required secrets (GitHub Actions)

Set these under repo Settings → Secrets and variables → Actions:

- `ANTHROPIC_API_KEY` — required, used for digest generation, fact-checking and
  trends synthesis.
- `SERPAPI_KEY` — optional but strongly recommended; without it the media filter
  is skipped and entries are labelled "Not verified".
- `NCBI_API_KEY` — optional, raises the PubMed rate limit.

## Repo layout

```
scripts/
  main.py                    entry point — orchestrates the full pipeline
  pubmed.py                  PubMed E-utilities client
  journals.py                generated list of (journal, ISSN, categories)
  build_journals.py          regenerates journals.py from the CSV
  screening.py               pre-Claude title screen and novelty ranking
  media_filter.py            SerpAPI "already covered?" check
  llm.py                     shared Claude call + text extraction helpers
  digest_generator.py        Claude prompt + call that writes the digest
  fact_checker.py            Claude prompt + call that fact-checks the digest
  trends.py                  Claude prompt + call for trends/feature pitch + topic memory
  build_dashboard_data.py    parses outputs/*.md into docs/data/
  migrate_legacy_results.py  one-time back-conversion of the old JSON archive
outputs/                     every digest + fact-check ever generated (.md)
topic_memory/                per-topic running memory used by trends.py
docs/                        static dashboard, served by GitHub Pages
archive/legacy-results.json  the previous pipeline's full 904-study archive
data/                        the curated journal CSV
config/digest_config.json    publication, rotation and threshold settings
seen_pmids.json              every PMID ever written up — never pitched twice
.github/workflows/           daily cron (daily-digest.yml)
```
