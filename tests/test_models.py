from __future__ import annotations

import pytest
from pydantic import ValidationError

from content_brain.domain.models import (
    AnalyticsMetrics,
    Confidence,
    HookCandidate,
    SourceMetadata,
    VideoFormat,
)


def test_models_accept_valid_values() -> None:
    assert VideoFormat.SHORT.word_range == (75, 150)
    assert VideoFormat.LONG_FORM.word_range == (1200, 2250)
    assert HookCandidate(text="A clear enough hook for testing.", rationale="A sufficiently clear rationale.").score == 0
    assert AnalyticsMetrics(views=10, ctr=4.5).views == 10
    assert SourceMetadata(title="A source", publication_year=2024).publication_year == 2024
    assert Confidence.MEDIUM.value == "medium"


@pytest.mark.parametrize("factory", [
    lambda: VideoFormat("vertical"),
    lambda: HookCandidate(text="short", rationale="A rationale that is long enough."),
    lambda: AnalyticsMetrics(ctr=110),
    lambda: SourceMetadata(title="Source", publication_year=1700),
])
def test_models_reject_invalid_values(factory: object) -> None:
    with pytest.raises((ValidationError, ValueError)):
        factory()  # type: ignore[operator]
