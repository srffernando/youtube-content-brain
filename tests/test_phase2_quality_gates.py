from __future__ import annotations

import pytest
from pydantic import ValidationError

from content_brain.domain.models import Confidence, ContentDraft, PsychologyInsight, VideoFormat
from content_brain.domain.scoring import score_hook
from content_brain.domain.validation import validate_package
from content_brain.pipeline import ContentPipeline
from content_brain.providers.mock import MockProvider


def test_malformed_provider_shape_is_rejected() -> None:
    with pytest.raises(ValidationError):
        ContentDraft.model_validate({"audience_pain": "only one field"})


def test_unsupported_proof_claim_fails_validation() -> None:
    package = ContentPipeline(MockProvider()).generate("Why people procrastinate", VideoFormat.SHORT)
    bad_claim = PsychologyInsight(claim="Studies prove procrastination is always harmful.", evidence_or_reasoning="A deliberately sufficient reasoning field for schema validation.", confidence=Confidence.LOW, recommended_wording="Studies prove this is true.")
    result = validate_package(package.model_copy(update={"claims": [bad_claim]}))
    assert not result.valid
    assert any("requires source" in error for error in result.errors)


def test_clickbait_hook_is_not_high_quality() -> None:
    hook = MockProvider().generate("Why people procrastinate", VideoFormat.SHORT).hooks[0].model_copy(update={"text": "You won't believe what happens next!"})
    scored = score_hook(hook, "Why people procrastinate", "People avoid difficult tasks", VideoFormat.SHORT)
    assert "clickbait_phrase" in scored.risk_flags
    assert scored.score < 70


def test_short_with_many_claims_warns() -> None:
    package = ContentPipeline(MockProvider()).generate("Why people procrastinate", VideoFormat.SHORT)
    result = validate_package(package.model_copy(update={"claims": package.claims * 4}))
    assert any("more than three" in warning for warning in result.warnings)
