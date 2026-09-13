from __future__ import annotations

from content_brain.domain.models import ContentDraft, VideoFormat
from content_brain.providers.base import LLMProvider


class OpenAIProvider(LLMProvider):
    """Reserved adapter boundary; intentionally does not couple business logic to an SDK yet."""

    name = "openai"

    def __init__(self, api_key: str, model: str = "gpt-4.1-mini") -> None:
        if not api_key:
            raise ValueError("OpenAI API key is required")
        self.api_key = api_key
        self.model = model

    def generate(self, topic: str, format_: VideoFormat) -> ContentDraft:
        raise NotImplementedError("OpenAI generation is not configured in this phase; use MockProvider.")
