# Mental Health & Brain Science Research Digest

A GitHub Actions workflow that searches a curated list of mental health and brain science journals on PubMed, filters out widely covered stories, and emails a weekly digest with fact-checked study summaries and New Scientist Mind story pitches.

---

## How it works

1. **PubMed search** — Queries journals by ISSN for studies published in the past 30 days
2. **Title screening** — Prioritises studies with signals of novelty (first-in-class, counterintuitive, overturns prior research)
3. **SERPAPI media filter** — Checks Google News and skips any study with 3+ news results
4. **Abstract fetch** — Retrieves full abstracts for shortlisted studies
5. **Claude pass 1 (writer)** — Writes plain-language digest entries with caveats
6. **Claude pass 2 (editor/fact-checker)** — Verifies each entry against the abstract, corrects errors, and adds a New Scientist Mind pitch angle
7. **Email** — Sends the finished digest via Resend to meagan.lea.morris@gmail.com

---

## Schedule

Runs automatically every **Monday at 9:00 AM ET**. Can also be triggered manually via Actions → Run workflow.

---

## Categories

The digest searches 13 parallel jobs across these journal categories:

| Category | Journals | Jobs |
|---|---|---|
| Psychology | 135 | 3 (chunks 1–3) |
| Psychiatry | 111 | 2 (chunks 1–2) |
| Behavioral Sciences | 88 | 2 (chunks 1–2) |
| Brain | 23 | 1 |
| Neurology | 21 | 1 |
| Psychophysiology | 22 | 1 |
| Psychopharmacology | 14 | 1 |
| Social Sciences | 7 | 1 |
| Substance-Related Disorders | 4 | 1 |

Large categories are split into chunks so each job processes ~45 journals rather than 100+, keeping run times under 20 minutes.

---

## Manual trigger

Go to **Actions → Mental Health Research Digest → Run workflow**.

- Leave **category** blank to run all 13 jobs
- Enter an exact category name (e.g. `Brain`) to run just that category

---

## Required secrets

Add these in **Settings → Secrets and variables → Actions**:

| Secret | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key (`sk-ant-...`) |
| `SERPAPI_KEY` | SerpAPI key for Google News filtering |
| `RESEND_API_KEY` | Resend API key (`re_...`) for email delivery |

---

## Repo structure

```
.github/
  workflows/
    mh-digest.yml       # GitHub Actions workflow
scripts/
  mh_digest.py          # Main pipeline script
data/
  Mental Health - Brain Mental Health.csv   # Curated journal list with ISSNs
requirements.txt
```

---

## Email output

Each study entry in the digest includes:

- Plain-language headline and summary
- Groundbreaking criteria met (counterintuitive / overturns prior research / first-in-class)
- Media coverage status (verified via SERPAPI)
- Caveats and limitations
- ⚠️ Fact-check note (if the editor pass corrected anything)
- 📰 New Scientist Mind pitch — suggested headline, opening hook, pitch angle, and caveats for the journalist
