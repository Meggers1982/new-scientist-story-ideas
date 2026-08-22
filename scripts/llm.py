"""Shared Claude call helpers for the three generation passes.

Two things every pass needs and neither the senior-research-digest original nor
a naive port gets right on current models:

1. **Read every text block, not `content[0]`.** Claude Opus 5 runs adaptive
   thinking by default, so on any non-trivial prompt the first content block is
   a `thinking` block whose `.text` is empty. `response.content[0].text` returns
   "" and the pass silently produces an empty digest — no exception, no warning.
   `response_text` joins the blocks that actually carry text.

2. **Stream.** Thinking tokens come out of the same `max_tokens` budget as the
   visible answer, so these calls need a large ceiling, and the SDK wants
   streaming at that size rather than risking an HTTP timeout on a long
   non-streaming request.
"""

import anthropic

MODEL = "claude-opus-5"


def response_text(response) -> str:
    """Concatenate the text blocks of a response, skipping thinking blocks."""
    return "".join(
        block.text for block in response.content
        if getattr(block, "type", None) == "text"
    )


def call(client: anthropic.Anthropic, **kwargs):
    """Streamed `messages.create`, returning the completed Message.

    Streaming is an implementation detail here — nothing consumes the events —
    but it is what keeps a long, high-`max_tokens` request from tripping the
    SDK's request timeout.
    """
    kwargs.setdefault("model", MODEL)
    with client.messages.stream(**kwargs) as stream:
        return stream.get_final_message()
