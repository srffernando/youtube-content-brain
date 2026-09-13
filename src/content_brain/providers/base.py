from __future__ import annotations

from abc import ABC, abstractmethod

from content_brain.domain.models import ContentDraft, VideoFormat


class LLMProvider(ABC):
    """Boundary for any structured-content generation provider."""

    name: str
    model: str

    @abstractmethod
    def generate(self, topic: str, format_: VideoFormat) -> ContentDraft:
        """Return structured draft content. Ranking and validation stay outside providers."""
