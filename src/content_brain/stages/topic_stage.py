from __future__ import annotations

from content_brain.domain.models import EmotionalAngle, TopicAnalysis


def analyze_topic(topic: str) -> TopicAnalysis:
    """Extract viewer tension rather than paraphrasing the input topic."""
    lower = topic.lower()
    relationship = any(word in lower for word in ("ignore", "available", "relationship", "granted", "pull away", "respect"))
    if relationship:
        return TopicAnalysis(topic=topic, target_audience="People who feel overlooked or taken for granted in close relationships.", pain_point="I keep showing up for people, so why do they seem to value me less?", psychological_tension="The need for closeness conflicts with the fear that availability lowers perceived value.", emotional_angles=[EmotionalAngle.CURIOSITY, EmotionalAngle.RELATIONSHIP], core_question="Why can constant availability change how some people respond to us?", content_opportunity="Reframe availability as a boundary and reciprocity question, not a game of withholding care.")
    return TopicAnalysis(topic=topic, target_audience="People who know what matters but repeatedly delay uncomfortable work.", pain_point="I know the task matters, yet I choose small distractions and then blame myself.", psychological_tension="The desire for progress conflicts with immediate relief from discomfort.", emotional_angles=[EmotionalAngle.CURIOSITY, EmotionalAngle.VALIDATION], core_question="Why can avoiding a meaningful task feel easier than beginning it?", content_opportunity="Replace the laziness label with a practical explanation of short-term emotion management.")
