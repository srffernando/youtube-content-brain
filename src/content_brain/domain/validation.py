from __future__ import annotations

from content_brain.domain.models import ContentPackage, PsychologyInsight, ValidationResult

AUTHORITY_PHRASES = ("psychologists say", "studies prove", "science proves", "research shows")


def validate_claim(insight: PsychologyInsight) -> list[str]:
    text = f"{insight.claim} {insight.recommended_wording}".lower()
    if insight.source is None and any(phrase in text for phrase in AUTHORITY_PHRASES):
        return ["Unsupported authority phrase without source metadata; use cautious wording or supply evidence."]
    return []


def validate_package(package: ContentPackage) -> ValidationResult:
    warnings: list[str] = []
    errors: list[str] = []
    word_count = len(package.final_script.split())
    minimum, maximum = package.format.word_range
    if not minimum <= word_count <= maximum:
        errors.append(f"Script has {word_count} words; {package.format.value} requires {minimum}-{maximum}.")
    for insight in package.psychology_insights:
        warnings.extend(validate_claim(insight))
    if not package.cta.strip():
        errors.append("CTA is required.")
    return ValidationResult(valid=not errors, warnings=warnings, errors=errors, word_count=word_count)
