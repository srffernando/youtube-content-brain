from __future__ import annotations

from content_brain.domain.models import ContentDraft, StructuredScript


def build_script(draft: ContentDraft) -> StructuredScript:
    return draft.script
