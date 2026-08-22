"""Cheap, pre-Claude screening of PubMed summaries.

Two jobs: throw out article types that can never be a story (editorials,
errata, animal-only work), and rank what's left by how strongly the title
signals novelty — the quality New Scientist actually buys. Only the top of that
ranking is worth spending a SerpAPI lookup and an abstract fetch on.

Carried over from the pipeline this repo previously ran; the signal lists are
unchanged.
"""

from pubmed import SKIP_PUBTYPES, summary_fields

GROUNDBREAKING_SIGNALS = [
    "first", "novel", "unexpected", "contrary", "paradox", "no evidence",
    "challenges", "reverses", "debunks", "replication failure", "previously unknown",
    "newly identified", "overturns", "failed to replicate", "against prior",
    "first randomized", "first longitudinal", "first human", "first study",
    "surpris", "counterintuitive", "revised understanding", "new mechanism",
    "no significant", "opposite", "protective effect",
]

ANIMAL_ONLY_SIGNALS = {
    "in mice", "in rats", "in mouse", "in rat", "mouse model", "rat model",
    "murine", "rodent model", "in zebrafish", "in drosophila", "in c. elegans",
    "in macaques", "in primates", "in rabbits", "in pigs", "in sheep",
}

HUMAN_SIGNALS = {
    "human", "patients", "participants", "adults", "children", "adolescents",
    "men", "women", "cohort", "population",
}


def is_animal_only(title: str) -> bool:
    t = title.lower()
    return any(s in t for s in ANIMAL_ONLY_SIGNALS) and not any(s in t for s in HUMAN_SIGNALS)


def novelty_score(title: str) -> int:
    """How many novelty signals the title trips. Higher is more pitchable."""
    t = title.lower()
    return sum(1 for s in GROUNDBREAKING_SIGNALS if s in t)


def screen(
    summaries: dict,
    already_covered: set[str],
    max_candidates: int = 60,
) -> list[dict]:
    """Rank eligible summaries by novelty signal and return the top `max_candidates`.

    Studies already written up in a previous digest are dropped outright — this
    repo exists to surface pitchable ideas, and a study that has already been
    pitched is not a new idea. Editorials, errata and animal-only work are
    dropped too; none of them can become the kind of story this is looking for.

    Everything else is ranked, not gated. The keyword score is a crude proxy for
    novelty and it goes quiet on a topic-focused run — searching one subject over
    30 days, only a handful of titles trip a signal at all, and hard-gating on it
    would starve the digest and hand Claude an arbitrary remainder. Ranking
    instead means the strongest signals still float to the top of the shortlist
    while the rest are ordered newest-first behind them, and the real editorial
    judgment happens where it belongs: in the digest prompt, reading abstracts.
    """
    ranked: list[dict] = []
    with_signal = 0
    dropped = {"seen": 0, "pubtype": 0, "animal": 0, "no_title": 0}

    for pmid, summary in summaries.items():
        if pmid in already_covered:
            dropped["seen"] += 1
            continue
        fields = {"pmid": pmid, **summary_fields(summary)}
        if not fields["title"]:
            dropped["no_title"] += 1
            continue
        if SKIP_PUBTYPES & set(fields["pubtype"]):
            dropped["pubtype"] += 1
            continue
        if is_animal_only(fields["title"]):
            dropped["animal"] += 1
            continue
        fields["novelty"] = novelty_score(fields["title"])
        if fields["novelty"]:
            with_signal += 1
        ranked.append(fields)

    # Stable sort, so studies on equal footing keep PubMed's newest-first order.
    ranked.sort(key=lambda f: -f["novelty"])

    print(
        f"  Screened {len(ranked)} eligible ({with_signal} tripped a novelty signal). "
        f"Dropped {dropped['seen']} already covered, {dropped['pubtype']} by article type, "
        f"{dropped['animal']} animal-only, {dropped['no_title']} with no title."
    )
    return ranked[:max_candidates]
