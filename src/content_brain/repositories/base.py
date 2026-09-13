from __future__ import annotations

from abc import ABC, abstractmethod

from content_brain.domain.models import ContentPackage


class ContentRepository(ABC):
    @abstractmethod
    def save(self, package: ContentPackage) -> ContentPackage: ...

    @abstractmethod
    def get(self, package_id: str) -> ContentPackage | None: ...

    @abstractmethod
    def list(self) -> list[ContentPackage]: ...
