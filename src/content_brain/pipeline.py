"""Compatibility facade for the Phase 2 orchestrator and quality engine."""
from __future__ import annotations

from content_brain.domain.models import ContentPackage, QualityScore, QualityStatus


def calculate_quality(package: ContentPackage) -> QualityScore:
    hook = package.selected_hook.score
    sourced = sum(claim.source is not None for claim in package.claims)
    evidence = 55.0 + 45.0 * sourced / len(package.claims)
    confidence = sum({"low": 55.0, "medium": 75.0, "high": 95.0}[claim.confidence.value] for claim in package.claims) / len(package.claims)
    structure = 100.0 if len(package.script.sections) >= 6 else 40.0
    duration = 100.0 if not package.validation.errors else 0.0
    originality = 100.0 if len({item.text.lower() for item in package.hooks}) == len(package.hooks) else 40.0
    cta = 100.0 if len(package.cta.split()) >= 5 else 50.0
    penalty = min(25.0, len(package.validation.warnings) * 4.0)
    breakdown = {"hook": hook, "topic_relevance": 90.0, "emotional_impact": 85.0, "psychology": confidence, "evidence": evidence, "script_structure": structure, "originality": originality, "cta": cta, "validation_penalty": -penalty, "duration_fit": duration}
    overall = hook * .20 + 90 * .15 + 85 * .15 + confidence * .20 + evidence * .10 + structure * .10 + originality * .05 + cta * .05 - penalty
    overall = round(max(0.0, min(100.0, overall)), 2)
    status = QualityStatus.READY if overall >= 90 else QualityStatus.REVIEW if overall >= 75 else QualityStatus.NEEDS_WORK if overall >= 60 else QualityStatus.REJECT
    return QualityScore(overall=overall, status=status, breakdown=breakdown)


from content_brain.orchestrator import ContentOrchestrator

ContentPipeline = ContentOrchestrator

__all__ = ["ContentPipeline", "calculate_quality"]
