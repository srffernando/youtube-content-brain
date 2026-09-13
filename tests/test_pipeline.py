from __future__ import annotations

from content_brain.domain.models import StructuredScript, VideoFormat
from content_brain.domain.validation import validate_package
from content_brain.pipeline import ContentPipeline, calculate_quality
from content_brain.providers.mock import MockProvider

TOPIC = "Why do people procrastinate even when they know what they need to do?"


def test_mock_provider_is_deterministic() -> None:
    provider = MockProvider()
    assert provider.generate(TOPIC, VideoFormat.SHORT).model_dump() == provider.generate(TOPIC, VideoFormat.SHORT).model_dump()


def test_full_short_pipeline() -> None:
    package = ContentPipeline(MockProvider()).generate(TOPIC, VideoFormat.SHORT)
    assert package.validation.valid
    assert len(package.hooks) == len(package.titles) == 5
    assert package.selected_hook.score == max(item.score for item in package.hooks)
    assert package.quality_score.overall > 0
    assert 75 <= package.validation.word_count <= 150


def test_full_long_pipeline() -> None:
    package = ContentPipeline(MockProvider()).generate(TOPIC, VideoFormat.LONG_FORM)
    assert package.validation.valid
    assert 1200 <= package.validation.word_count <= 2250
    assert len(package.psychology_insights) == 3


def test_duration_validation_and_quality_penalty() -> None:
    package = ContentPipeline(MockProvider()).generate(TOPIC, VideoFormat.SHORT)
    bad = package.model_copy(update={"script": StructuredScript(sections=[section.model_copy(update={"text": "too short"}) for section in package.script.sections])})
    validation = validate_package(bad)
    scored = bad.model_copy(update={"validation": validation})
    assert not validation.valid
    assert calculate_quality(scored).breakdown["duration_fit"] == 0
