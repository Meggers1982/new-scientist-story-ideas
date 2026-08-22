"""PubMed E-utilities client with ISSN-batch search.

Ported from the senior-research-digest pipeline. The one substantive change is
in `search_by_issns`: that pipeline searches ~146 journals over a 90-day window
and rarely fills its PMID quota, so taking batches in order until the quota was
full was harmless. This pipeline searches 325 journals over 30 days and pulls
5,000+ articles on a broad run, so an in-order fill would exhaust the quota on
the first two ISSN batches and never look at the other ~275 journals. Batches
are therefore drawn round-robin, newest-first within each batch, so every
journal in the list gets a shot at the shortlist.
"""

import math
import time
import requests
from datetime import datetime, timedelta
from typing import Optional


EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
_RATE_DELAY_NO_KEY = 0.4  # seconds between calls (safe for 3 req/sec without API key)
_RATE_DELAY_WITH_KEY = 0.11  # seconds between calls (safe for 10 req/sec with API key)

SKIP_PUBTYPES = {
    "editorial", "letter", "comment", "news", "biography",
    "case reports", "published erratum", "retraction of publication",
}


def _get(url: str, params: dict, timeout: int = 30) -> requests.Response:
    delay = _RATE_DELAY_WITH_KEY if params.get("api_key") else _RATE_DELAY_NO_KEY
    time.sleep(delay)
    resp = requests.get(url, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp


def _date_range(days_back: int) -> tuple[str, str]:
    end = datetime.now()
    start = end - timedelta(days=days_back)
    return start.strftime("%Y/%m/%d"), end.strftime("%Y/%m/%d")


def search_by_issns(
    issns: list[str],
    days_back: int = 30,
    subject_focus: str = "",
    max_per_batch: int = 25,
    max_total: int = 300,
    ncbi_api_key: Optional[str] = None,
) -> list[str]:
    """Search PubMed across a list of ISSNs and return unique PMIDs, newest first.

    ISSNs are batched into groups of `max_per_batch` to stay within URL limits.
    If `subject_focus` is provided it is ANDed with each batch query as an exact
    phrase (no MeSH or synonym expansion — see README on choosing topic wording).

    Each batch contributes at most its fair share of `max_total`, and the
    per-batch results are interleaved round-robin, so a handful of prolific
    journals cannot crowd the rest of the list out of the shortlist.
    """
    start_date, end_date = _date_range(days_back)
    batches = [issns[i : i + max_per_batch] for i in range(0, len(issns), max_per_batch)]
    # Over-request per batch so that batches which come up short can be topped
    # up by the ones that don't, while still capping any single batch's share.
    per_batch = max(10, math.ceil(max_total / max(1, len(batches))) * 3)

    batch_results: list[list[str]] = []
    for n, batch in enumerate(batches, start=1):
        issn_term = " OR ".join(f"{issn}[issn]" for issn in batch)
        if subject_focus:
            term = f'({issn_term}) AND ("{subject_focus}"[Title/Abstract])'
        else:
            term = issn_term

        params: dict = {
            "db": "pubmed",
            "term": term,
            "mindate": start_date,
            "maxdate": end_date,
            "datetype": "pdat",
            "sort": "pub_date",
            "retmax": per_batch,
            "retmode": "json",
        }
        if ncbi_api_key:
            params["api_key"] = ncbi_api_key

        try:
            resp = _get(f"{EUTILS_BASE}/esearch.fcgi", params)
            batch_results.append(resp.json().get("esearchresult", {}).get("idlist", []))
        except Exception as e:
            print(f"  Warning: ISSN batch {n}/{len(batches)} failed: {e}")
            batch_results.append([])

    # Interleave: one PMID from each batch per pass, until the quota is full.
    all_pmids: list[str] = []
    seen: set[str] = set()
    for depth in range(per_batch):
        for results in batch_results:
            if depth >= len(results):
                continue
            pmid = results[depth]
            if pmid not in seen:
                seen.add(pmid)
                all_pmids.append(pmid)
                if len(all_pmids) >= max_total:
                    return all_pmids

    return all_pmids


def fetch_summaries(
    pmids: list[str],
    ncbi_api_key: Optional[str] = None,
    batch_size: int = 100,
) -> dict:
    """Fetch document summaries for a list of PMIDs, in batches."""
    merged: dict = {}
    for i in range(0, len(pmids), batch_size):
        batch = pmids[i : i + batch_size]
        params: dict = {
            "db": "pubmed",
            "id": ",".join(batch),
            "retmode": "json",
        }
        if ncbi_api_key:
            params["api_key"] = ncbi_api_key
        try:
            result = _get(f"{EUTILS_BASE}/esummary.fcgi", params).json().get("result", {})
        except Exception as e:
            print(f"  Warning: esummary batch {i // batch_size + 1} failed: {e}")
            continue
        for key, value in result.items():
            if key != "uids":
                merged[key] = value
    return merged


def summary_fields(summary: dict) -> dict:
    """Flatten the fields of an esummary record this pipeline cares about."""
    return {
        "title": (summary.get("title") or "").strip(),
        "journal": (summary.get("fulljournalname") or summary.get("source") or "").strip(),
        "pubdate": (summary.get("pubdate") or "").strip(),
        "pubtype": [p.lower() for p in summary.get("pubtype", [])],
        "doi": next(
            (
                a.get("value", "")
                for a in summary.get("articleids", [])
                if a.get("idtype") == "doi"
            ),
            "",
        ),
    }


def fetch_abstract(
    pmid: str,
    ncbi_api_key: Optional[str] = None,
) -> str:
    """Fetch the full abstract text for a single PMID."""
    params: dict = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "text",
        "rettype": "abstract",
    }
    if ncbi_api_key:
        params["api_key"] = ncbi_api_key

    resp = _get(f"{EUTILS_BASE}/efetch.fcgi", params)
    return resp.text.strip()


def fetch_abstracts_for_pmids(
    pmids: list[str],
    ncbi_api_key: Optional[str] = None,
    min_length: int = 150,
) -> dict[str, str]:
    """Fetch abstracts for all PMIDs, skipping short/empty responses."""
    results: dict[str, str] = {}
    for pmid in pmids:
        try:
            text = fetch_abstract(pmid, ncbi_api_key)
            if len(text) >= min_length:
                results[pmid] = text
            else:
                print(f"  Skipping PMID {pmid} — abstract too short ({len(text)} chars)")
        except requests.HTTPError as e:
            print(f"  Warning: HTTP error fetching PMID {pmid}: {e}")
        except Exception as e:
            print(f"  Warning: Could not fetch PMID {pmid}: {e}")
    return results
