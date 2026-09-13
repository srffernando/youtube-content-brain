from __future__ import annotations

from content_brain.domain.models import ContentPackage, PsychologyInsight, ValidationResult

AUTHORITY_PHRASES = ("psychologists say", "studies prove", "science proves", "research shows", "researchers discovered", "your brain does")
HARD_UNSUPPORTED_PHRASES = ("studies prove", "science proves", "research proves")
ABSOLUTE_PHRASES = ("always", "never", "everyone", "guaranteed", "proven", "100%")


def validate_claim(insight: PsychologyInsight) -> list[str]:
    text = f"{insight.claim} {insight.recommended_wording}".lower()
    if insight.source is None and any(phrase in text for phrase in AUTHORITY_PHRASES):
        return ["Unsupported authority phrase without source metadata; use cautious wording or supply evidence."]
    return []


def validate_package(package: ContentPackage) -> ValidationResult:
    warnings: list[str] = []
    errors: list[str] = []
    word_count = len(package.script.text.split())
    minimum, maximum = package.format.word_range
    if not minimum <= word_count <= maximum:
        errors.append(f"Script has {word_count} words; {package.format.value} requires {minimum}-{maximum}.")
    for insight in package.psychology_insights:
        claim_text = f"{insight.claim} {insight.recommended_wording}".lower()
        if insight.source is None and any(phrase in claim_text for phrase in HARD_UNSUPPORTED_PHRASES):
            errors.append("Unsupported evidence claim requires source metadata.")
        warnings.extend(validate_claim(insight))
        if any(phrase in claim_text for phrase in ABSOLUTE_PHRASES):
            warnings.append("Absolute language detected in a claim.")
    if package.format.value == "short" and len(package.claims) > 3:
        warnings.append("Short-form content contains more than three psychology claims.")
    normalized_hooks = [hook.text.lower().split()[:4] for hook in package.hooks]
    if len({" ".join(words) for words in normalized_hooks}) < len(normalized_hooks):
        warnings.append("Hook originality warning: candidates share the same opening structure.")
    if not package.cta.strip():
        errors.append("CTA is required.")
    return ValidationResult(valid=not errors, warnings=warnings, errors=errors, word_count=word_count)
