"""A process-wide circuit breaker for SerpAPI, shared by every screen that calls it.

Two screens in this pipeline hit SerpAPI back to back — `media_filter` (Google
News) and `ns_check` (a site-scoped web search) — and on 2026-09-05 both of them
sat through the full read timeout on every candidate while SerpAPI answered
nothing. Between them that is enough to spend the whole 30-minute Actions
ceiling discovering the same outage a hundred times over. A screen that cannot
run should cost seconds, not the job.

Counting rules, both learned the hard way in the sibling `trending-content` repo
on 2026-09-06:

- **Count queries, not attempts.** One slow query is not an outage.
- **Count per engine, not globally.** The first screen to run must not decide
  whether the second one gets to try; they fail independently, and a screen
  skipped on someone else's evidence is signal thrown away for free.

The global time budget is the exception, and deliberately outranks both: once
the run has spent it, every engine stops, because at that point the risk being
managed is the job ceiling rather than the upstream.
"""

import os
import time

# Consecutive failed *queries* for one engine before that engine is given up on.
FAILURE_THRESHOLD = int(os.getenv("SERPAPI_FAILURE_THRESHOLD", "3"))

# Wall-clock ceiling per engine, then across the whole process. Backstop for the
# slow-but-succeeding case, which a failure count never sees.
ENGINE_TIME_BUDGET_SECONDS = float(os.getenv("SERPAPI_ENGINE_TIME_BUDGET_SECONDS", "240"))
TOTAL_TIME_BUDGET_SECONDS = float(os.getenv("SERPAPI_TIME_BUDGET_SECONDS", "600"))

_failures: dict[str, int] = {}
_engine_elapsed: dict[str, float] = {}
_tripped: set[str] = set()
_total_elapsed = 0.0
_all_tripped = False


def is_open(engine: str) -> bool:
    """True once this engine has earned a rest for the remainder of the process."""
    global _all_tripped

    if _all_tripped:
        return True

    if _total_elapsed >= TOTAL_TIME_BUDGET_SECONDS:
        _all_tripped = True
        print(
            f"  SerpAPI circuit breaker OPEN for all engines — "
            f"{_total_elapsed:.0f}s spent, over the "
            f"{TOTAL_TIME_BUDGET_SECONDS:.0f}s run budget"
        )
        return True

    if engine in _tripped:
        return True

    reason = None
    if _failures.get(engine, 0) >= FAILURE_THRESHOLD:
        reason = (
            f"{_failures[engine]} consecutive failed queries "
            f"(threshold {FAILURE_THRESHOLD})"
        )
    elif _engine_elapsed.get(engine, 0.0) >= ENGINE_TIME_BUDGET_SECONDS:
        reason = (
            f"{_engine_elapsed[engine]:.0f}s spent, over this engine's "
            f"{ENGINE_TIME_BUDGET_SECONDS:.0f}s budget"
        )

    if reason:
        _tripped.add(engine)
        print(f"  SerpAPI circuit breaker OPEN for {engine} — {reason}")
        return True
    return False


def record(engine: str, *, ok: bool, seconds: float) -> None:
    """Book one query's outcome and cost against the breaker."""
    global _total_elapsed
    _failures[engine] = 0 if ok else _failures.get(engine, 0) + 1
    _engine_elapsed[engine] = _engine_elapsed.get(engine, 0.0) + seconds
    _total_elapsed += seconds


class timed:
    """Context manager that records one query. Set `.ok = True` on success.

        with timed("google_news") as t:
            data = fetch()
            t.ok = True

    Defaults to failure, so an exception escaping the block is counted without
    the caller having to remember an except clause.
    """

    def __init__(self, engine: str):
        self.engine = engine
        self.ok = False

    def __enter__(self):
        self._started = time.monotonic()
        return self

    def __exit__(self, *exc):
        record(self.engine, ok=self.ok, seconds=time.monotonic() - self._started)
        return False


def reset() -> None:
    """Test hook: forget everything recorded so far."""
    global _total_elapsed, _all_tripped
    _failures.clear()
    _engine_elapsed.clear()
    _tripped.clear()
    _total_elapsed = 0.0
    _all_tripped = False
