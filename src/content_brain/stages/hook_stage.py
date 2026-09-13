from __future__ import annotations

from content_brain.domain.models import (
    ContentDraft,
    ContentStrategy,
    HookCandidate,
    TitleCandidate,
    VideoFormat,
)
from content_brain.domain.scoring import score_hook, score_title


def score_candidates(draft: ContentDraft, topic: str, strategy: ContentStrategy, format_: VideoFormat) -> tuple[list[HookCandidate], list[TitleCandidate]]:
    return ([score_hook(item, topic, strategy.pain_point, format_) for item in draft.hooks], [score_title(item, topic) for item in draft.titles])
