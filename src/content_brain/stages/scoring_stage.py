from __future__ import annotations

from content_brain.domain.models import ContentPackage, QualityScore


def score(package: ContentPackage) -> QualityScore:
    from content_brain.pipeline import calculate_quality
    return calculate_quality(package)
