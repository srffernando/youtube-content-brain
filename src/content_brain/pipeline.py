from __future__ import annotations

from content_brain.domain.models import ContentPackage, QualityScore, ValidationResult, VideoFormat
from content_brain.domain.scoring import score_hook, score_title
from content_brain.domain.validation import validate_package
from content_brain.providers.base import LLMProvider


def calculate_quality(package: ContentPackage) -> QualityScore:
    hook_quality = package.selected_hook.score
    title_quality = package.selected_title.score
    sourced = sum(insight.source is not None for insight in package.psychology_insights)
    evidence = 65.0 + (35.0 * sourced / len(package.psychology_insights))
    confidence_values = {"low": 55.0, "medium": 75.0, "high": 95.0}
    confidence = sum(confidence_values[item.confidence.value] for item in package.psychology_insights) / len(package.psychology_insights)
    structure = 100.0 if len(package.story.beats) >= 2 else 50.0
    duration = 100.0 if not package.validation.errors else 0.0
    clarity = 90.0
    cta = 90.0 if len(package.cta.split()) >= 5 else 55.0
    completeness = 100.0
    warning_penalty = min(20.0, len(package.validation.warnings) * 5.0)
    breakdown = {"completeness": completeness, "hook_quality": hook_quality, "title_quality": title_quality, "evidence_coverage": evidence, "claim_confidence": confidence, "structure": structure, "duration_fit": duration, "clarity": clarity, "cta_quality": cta, "validation_warning_penalty": -warning_penalty}
    overall = (completeness * .10 + hook_quality * .14 + title_quality * .14 + evidence * .12 + confidence * .10 + structure * .10 + duration * .10 + clarity * .05 + cta * .05 - warning_penalty)
    return QualityScore(overall=round(max(0.0, min(100.0, overall)), 2), breakdown=breakdown)


class ContentPipeline:
    prompt_version = "v1"

    def __init__(self, provider: LLMProvider) -> None:
        self.provider = provider

    def generate(self, topic: str, format_: VideoFormat) -> ContentPackage:
        draft = self.provider.generate(topic, format_)
        hooks = [score_hook(item, topic, draft.audience_pain, format_) for item in draft.hooks]
        titles = [score_title(item, topic) for item in draft.titles]
        provisional = ContentPackage(topic=topic, format=format_, audience_pain=draft.audience_pain, emotional_angle=draft.emotional_angle, hooks=hooks, selected_hook=max(hooks, key=lambda item: item.score), story=draft.story, psychology_insights=draft.psychology_insights, lesson=draft.lesson, cta=draft.cta, titles=titles, selected_title=max(titles, key=lambda item: item.score), thumbnail=draft.thumbnail, final_script=draft.final_script, quality_score=QualityScore(overall=0), validation=ValidationResult(valid=False, word_count=0), prompt_version=self.prompt_version, provider=self.provider.name, model=self.provider.model)
        validation = validate_package(provisional)
        package = provisional.model_copy(update={"validation": validation})
        return package.model_copy(update={"quality_score": calculate_quality(package)})
