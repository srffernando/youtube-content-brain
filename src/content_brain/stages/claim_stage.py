from __future__ import annotations

from content_brain.domain.models import ContentDraft, PsychologyInsight


def extract_claims(draft: ContentDraft) -> list[PsychologyInsight]:
    return draft.psychology_insights
