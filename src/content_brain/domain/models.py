from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class VideoFormat(StrEnum):
    SHORT = "short"
    LONG_FORM = "long_form"

    @property
    def word_range(self) -> tuple[int, int]:
        return (75, 150) if self is VideoFormat.SHORT else (1200, 2250)


class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SourceMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1)
    author: str | None = None
    url: str | None = None
    publication_year: int | None = Field(default=None, ge=1800, le=2100)


class PsychologyInsight(BaseModel):
    model_config = ConfigDict(extra="forbid")
    claim: str = Field(min_length=5)
    evidence_or_reasoning: str = Field(min_length=10)
    confidence: Confidence
    source: SourceMetadata | None = None
    recommended_wording: str = Field(min_length=5)


class HookCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=10)
    rationale: str = Field(min_length=10)
    score: float = Field(default=0, ge=0, le=100)
    score_breakdown: dict[str, float] = Field(default_factory=dict)


class TitleCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=10, max_length=100)
    rationale: str = Field(min_length=10)
    score: float = Field(default=0, ge=0, le=100)
    score_breakdown: dict[str, float] = Field(default_factory=dict)


class Story(BaseModel):
    model_config = ConfigDict(extra="forbid")
    summary: str = Field(min_length=20)
    beats: list[str] = Field(min_length=2)
    examples: list[str] = Field(default_factory=list)
    pattern_interrupts: list[str] = Field(default_factory=list)


class ThumbnailConcept(BaseModel):
    model_config = ConfigDict(extra="forbid")
    visual: str = Field(min_length=10)
    text_overlay: str = Field(min_length=2, max_length=50)
    rationale: str = Field(min_length=10)


class AnalyticsMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")
    views: int | None = Field(default=None, ge=0)
    impressions: int | None = Field(default=None, ge=0)
    ctr: float | None = Field(default=None, ge=0, le=100)
    average_view_duration_seconds: float | None = Field(default=None, ge=0)
    average_percentage_viewed: float | None = Field(default=None, ge=0, le=100)
    likes: int | None = Field(default=None, ge=0)
    comments: int | None = Field(default=None, ge=0)
    shares: int | None = Field(default=None, ge=0)
    subscribers_gained: int | None = Field(default=None, ge=0)


class ValidationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    valid: bool
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    word_count: int = Field(ge=0)


class QualityScore(BaseModel):
    model_config = ConfigDict(extra="forbid")
    overall: float = Field(ge=0, le=100)
    breakdown: dict[str, float] = Field(default_factory=dict)


class ContentDraft(BaseModel):
    """Provider output before ranking, validation, and persistence."""
    model_config = ConfigDict(extra="forbid")
    audience_pain: str = Field(min_length=10)
    emotional_angle: str = Field(min_length=10)
    hooks: list[HookCandidate] = Field(min_length=5, max_length=5)
    story: Story
    psychology_insights: list[PsychologyInsight] = Field(min_length=1)
    lesson: str = Field(min_length=10)
    cta: str = Field(min_length=5)
    titles: list[TitleCandidate] = Field(min_length=5, max_length=5)
    thumbnail: ThumbnailConcept
    final_script: str = Field(min_length=20)


class ContentPackage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    package_id: str = Field(default_factory=lambda: str(uuid4()))
    topic: str = Field(min_length=5)
    format: VideoFormat
    audience_pain: str
    emotional_angle: str
    hooks: list[HookCandidate]
    selected_hook: HookCandidate
    story: Story
    psychology_insights: list[PsychologyInsight]
    lesson: str
    cta: str
    titles: list[TitleCandidate]
    selected_title: TitleCandidate
    thumbnail: ThumbnailConcept
    final_script: str
    quality_score: QualityScore
    validation: ValidationResult
    prompt_version: str = "v1"
    provider: str
    model: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    analytics: AnalyticsMetrics = Field(default_factory=AnalyticsMetrics)

    @field_validator("hooks", "titles")
    @classmethod
    def exactly_five_candidates(cls, value: list[HookCandidate] | list[TitleCandidate]) -> list[HookCandidate] | list[TitleCandidate]:
        if len(value) != 5:
            raise ValueError("exactly five candidates are required")
        return value
