from __future__ import annotations

from content_brain.domain.models import ContentStrategy, TopicAnalysis


def build_concept(analysis: TopicAnalysis) -> ContentStrategy:
    return ContentStrategy(audience=analysis.target_audience, pain_point=analysis.pain_point, emotional_angles=analysis.emotional_angles, core_question=analysis.core_question, concept=analysis.content_opportunity)
