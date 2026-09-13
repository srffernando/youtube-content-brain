from __future__ import annotations

from content_brain.domain.models import ContentPackage, ValidationResult
from content_brain.domain.validation import validate_package


def validate(package: ContentPackage) -> ValidationResult:
    return validate_package(package)
