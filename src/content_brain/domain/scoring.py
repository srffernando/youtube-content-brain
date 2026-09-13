from __future__ import annotations

from content_brain.domain.models import HookCandidate, TitleCandidate, VideoFormat


def _contains_any(text: str, phrases: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(phrase in lower for phrase in phrases)


def _bounded(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 2)


def score_hook(candidate: HookCandidate, topic: str, audience_pain: str, format_: VideoFormat) -> HookCandidate:
    text = candidate.text.lower()
    topic_words = {word.strip("?!,. ").lower() for word in topic.split() if len(word) > 3}
    pain_words = {word.strip("?!,. ").lower() for word in audience_pain.split() if len(word) > 4}
    curiosity = 15.0 if "?" in candidate.text or _contains_any(text, ("why", "secret", "real reason")) else 8.0
    emotional = 15.0 if _contains_any(text, ("guilt", "stuck", "fear", "shame", "avoid", "relief")) else 8.0
    specificity = 15.0 if any(char.isdigit() for char in text) or _contains_any(text, ("tonight", "when", "before")) else 9.0
    clarity = 15.0 if len(candidate.text.split()) <= (18 if format_ is VideoFormat.SHORT else 28) else 8.0
    alignment = 15.0 if topic_words.intersection(text.split()) or pain_words.intersection(text.split()) else 7.0
    suitability = 15.0 if (format_ is VideoFormat.SHORT and len(candidate.text.split()) <= 18) or format_ is VideoFormat.LONG_FORM else 8.0
    novelty = 10.0 if _contains_any(text, ("isn't", "not laziness", "instead")) else 5.0
    impact = 15.0 if len(candidate.text.split()) <= 14 and ("?" in candidate.text or emotional >= 15) else 7.0
    risk = -25.0 if _contains_any(text, ("you won't believe", "guaranteed", "100%")) else 0.0
    flags = ["clickbait_phrase"] if risk else []
    breakdown = {"curiosity": curiosity, "clarity": clarity, "emotional_tension": emotional, "specificity": specificity, "novelty": novelty, "first_3_second_impact": impact, "clickbait_risk": risk, "audience_pain_alignment": alignment, "format_suitability": suitability}
    return candidate.model_copy(update={"score": _bounded(sum(breakdown.values())), "score_breakdown": breakdown, "risk_flags": flags})


def score_title(candidate: TitleCandidate, topic: str) -> TitleCandidate:
    text = candidate.text.lower()
    topic_words = {word.strip("?!,. ").lower() for word in topic.split() if len(word) > 3}
    curiosity = 16.0 if _contains_any(text, ("why", "real reason", "what", "truth")) else 9.0
    clarity = 15.0 if 4 <= len(candidate.text.split()) <= 14 else 7.0
    specificity = 14.0 if _contains_any(text, ("when", "even", "before", "every")) else 8.0
    emotional = 14.0 if _contains_any(text, ("guilt", "stuck", "avoid", "fear", "lazy")) else 8.0
    alignment = 15.0 if topic_words.intersection(text.split()) else 7.0
    click_potential = 16.0 if _contains_any(text, ("why", "real reason", "not", "even")) else 9.0
    risk = 0.0 if not _contains_any(text, ("shocking", "guaranteed", "always", "never", "secret cure", "100%")) else -12.0
    flags = ["clickbait_or_absolute_language"] if risk else []
    breakdown = {"curiosity": curiosity, "clarity": clarity, "specificity": specificity, "emotional_relevance": emotional, "topic_alignment": alignment, "click_potential": click_potential, "clickbait_risk": risk}
    return candidate.model_copy(update={"score": _bounded(sum(breakdown.values())), "score_breakdown": breakdown, "risk_flags": flags})
