from __future__ import annotations

from content_brain.domain.models import ContentPackage, QualityScore, ValidationResult, VideoFormat
from content_brain.providers.base import LLMProvider
from content_brain.stages.claim_stage import extract_claims
from content_brain.stages.concept_stage import build_concept
from content_brain.stages.hook_stage import score_candidates
from content_brain.stages.script_stage import build_script
from content_brain.stages.topic_stage import analyze_topic
from content_brain.stages.validation_stage import validate


class ContentOrchestrator:
    """Coordinates stages only; content creation lives in provider/stage modules."""
    prompt_version = "psychology-v1"
    pipeline_version = "phase-2-v1"

    def __init__(self, provider: LLMProvider) -> None:
        self.provider = provider

    def generate(self, topic: str, format_: VideoFormat) -> ContentPackage:
        analysis = analyze_topic(topic)
        strategy = build_concept(analysis)
        draft = self.provider.generate(topic, format_)
        hooks, titles = score_candidates(draft, topic, strategy, format_)
        provisional = ContentPackage(topic=topic, format=format_, topic_analysis=analysis, strategy=strategy, hooks=hooks, selected_hook=max(hooks, key=lambda item: item.score), titles=titles, selected_title=max(titles, key=lambda item: item.score), script=build_script(draft), story=draft.story, claims=extract_claims(draft), lesson=draft.lesson, cta=draft.cta, thumbnail=draft.thumbnail, quality_score=QualityScore(overall=0), validation=ValidationResult(valid=False, word_count=0), prompt_version=self.prompt_version, pipeline_version=self.pipeline_version, provider=self.provider.name, model=self.provider.model)
        checked = provisional.model_copy(update={"validation": validate(provisional)})
        from content_brain.stages.scoring_stage import score
        return checked.model_copy(update={"quality_score": score(checked)})
