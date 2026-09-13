from __future__ import annotations

from content_brain.domain.models import (
    Confidence,
    HookCandidate,
    PsychologyInsight,
    TitleCandidate,
    VideoFormat,
)
from content_brain.domain.scoring import score_hook, score_title
from content_brain.domain.validation import validate_claim


def test_hook_scoring_is_deterministic_and_bounded() -> None:
    candidate = HookCandidate(text="Why does guilt make you avoid the task tonight?", rationale="Testing score behavior.")
    scored = score_hook(candidate, "Why people procrastinate", "People avoid difficult tasks because of guilt", VideoFormat.SHORT)
    assert scored.score == score_hook(candidate, "Why people procrastinate", "People avoid difficult tasks because of guilt", VideoFormat.SHORT).score
    assert 0 <= scored.score <= 100
    assert "novelty" in scored.score_breakdown


def test_title_scoring_penalizes_clickbait() -> None:
    safe = score_title(TitleCandidate(text="Why Starting Feels Hard", rationale="Clear title rationale."), "Why people procrastinate")
    clickbait = score_title(TitleCandidate(text="The SHOCKING Secret Cure for Procrastination", rationale="Clear title rationale."), "Why people procrastinate")
    assert safe.score_breakdown["clickbait_risk"] == 0
    assert clickbait.score_breakdown["clickbait_risk"] < 0


def test_claim_validator_detects_unsupported_authority() -> None:
    insight = PsychologyInsight(claim="Research shows procrastination is bad.", evidence_or_reasoning="This is a deliberately adequate reasoning field.", confidence=Confidence.LOW, recommended_wording="Psychologists say this is always true.")
    assert validate_claim(insight)


def test_claim_validator_allows_cautious_claim() -> None:
    insight = PsychologyInsight(claim="Avoidance can lower discomfort in the moment.", evidence_or_reasoning="Immediate relief can make the behavior appealing when discomfort returns.", confidence=Confidence.MEDIUM, recommended_wording="One useful way to view this is as short-term emotion management.")
    assert validate_claim(insight) == []
