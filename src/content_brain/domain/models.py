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


class EmotionalAngle(StrEnum):
    CURIOSITY = "curiosity"
    FEAR = "fear"
    SURPRISE = "surprise"
    VALIDATION = "validation"
    HOPE = "hope"
    ANGER = "anger"
    IDENTITY = "identity"
    STATUS = "status"
    SELF_IMPROVEMENT = "self_improvement"
    RELATIONSHIP = "relationship"


class ClaimType(StrEnum):
    PSYCHOLOGY = "psychology"
    BEHAVIORAL = "behavioral"
    NEUROSCIENCE = "neuroscience"
    RESEARCH = "research"
    STATISTICAL = "statistical"
    HISTORICAL = "historical"
    GENERAL_ADVICE = "general_advice"
    OPINION = "opinion"


class HookType(StrEnum):
    CONTRARIAN = "contrarian"
    QUESTION = "question"
    CURIOSITY = "curiosity"
    OBSERVATION = "observation"
    REFRAME = "reframe"


class QualityStatus(StrEnum):
    READY = "ready"
    REVIEW = "review"
    NEEDS_WORK = "needs_work"
    REJECT = "reject"


class SourceMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1)
    author: str | None = None
    url: str | None = None
    publication_year: int | None = Field(default=None, ge=1800, le=2100)


class TopicAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic: str = Field(min_length=5)
    target_audience: str = Field(min_length=10)
    pain_point: str = Field(min_length=10)
    psychological_tension: str = Field(min_length=10)
    emotional_angles: list[EmotionalAngle] = Field(min_length=1, max_length=2)
    core_question: str = Field(min_length=10)
    content_opportunity: str = Field(min_length=10)


class ContentStrategy(BaseModel):
    model_config = ConfigDict(extra="forbid")
    audience: str = Field(min_length=10)
    pain_point: str = Field(min_length=10)
    emotional_angles: list[EmotionalAngle] = Field(min_length=1, max_length=2)
    core_question: str = Field(min_length=10)
    concept: str = Field(min_length=10)


class PsychologyInsight(BaseModel):
    model_config = ConfigDict(extra="forbid")
    claim: str = Field(min_length=5)
    claim_type: ClaimType = ClaimType.PSYCHOLOGY
    evidence_or_reasoning: str = Field(min_length=10)
    confidence: Confidence
    source: SourceMetadata | None = None
    recommended_wording: str = Field(min_length=5)


class HookCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=10)
    type: HookType = HookType.CURIOSITY
    rationale: str = Field(min_length=10)
    score: float = Field(default=0, ge=0, le=100)
    score_breakdown: dict[str, float] = Field(default_factory=dict)
    risk_flags: list[str] = Field(default_factory=list)


class TitleCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=10, max_length=100)
    style: str = "psychology"
    rationale: str = Field(min_length=10)
    score: float = Field(default=0, ge=0, le=100)
    score_breakdown: dict[str, float] = Field(default_factory=dict)
    risk_flags: list[str] = Field(default_factory=list)


class Story(BaseModel):
    model_config = ConfigDict(extra="forbid")
    summary: str = Field(min_length=20)
    beats: list[str] = Field(min_length=2)
    examples: list[str] = Field(default_factory=list)
    pattern_interrupts: list[str] = Field(default_factory=list)


class ScriptSection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=2)
    start_seconds: int = Field(ge=0)
    end_seconds: int = Field(gt=0)
    text: str = Field(min_length=5)

    @field_validator("end_seconds")
    @classmethod
    def valid_duration(cls, value: int, info: object) -> int:
        start = getattr(info, "data", {}).get("start_seconds", 0)
        if value <= start:
            raise ValueError("end_seconds must be after start_seconds")
        return value


class StructuredScript(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sections: list[ScriptSection] = Field(min_length=6)

    @property
    def text(self) -> str:
        return "\n\n".join(section.text for section in self.sections)


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
    status: QualityStatus = QualityStatus.REVIEW
    breakdown: dict[str, float] = Field(default_factory=dict)


class ContentDraft(BaseModel):
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
    script: StructuredScript


class ContentPackage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    package_id: str = Field(default_factory=lambda: f"CB-{datetime.now(UTC):%Y}-{uuid4().hex[:8].upper()}")
    topic: str = Field(min_length=5)
    format: VideoFormat
    topic_analysis: TopicAnalysis
    strategy: ContentStrategy
    hooks: list[HookCandidate]
    selected_hook: HookCandidate
    titles: list[TitleCandidate]
    selected_title: TitleCandidate
    script: StructuredScript
    story: Story
    claims: list[PsychologyInsight]
    lesson: str
    cta: str
    thumbnail: ThumbnailConcept
    quality_score: QualityScore
    validation: ValidationResult
    prompt_version: str = "psychology-v1"
    pipeline_version: str = "phase-2-v1"
    provider: str
    model: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    analytics: AnalyticsMetrics = Field(default_factory=AnalyticsMetrics)

    @property
    def final_script(self) -> str:
        return self.script.text

    @property
    def psychology_insights(self) -> list[PsychologyInsight]:
        return self.claims

    @field_validator("hooks", "titles")
    @classmethod
    def exactly_five_candidates(cls, value: list[HookCandidate] | list[TitleCandidate]) -> list[HookCandidate] | list[TitleCandidate]:
        if len(value) != 5:
            raise ValueError("exactly five candidates are required")
        return value
