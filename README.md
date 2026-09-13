# YouTube Content Brain

A provider-independent, typed content-generation pipeline for a Psychology + Human Behavior YouTube channel. It produces a complete, persistent content package from a topic without requiring an API key in its initial deterministic mock mode.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Install

```powershell
uv sync --all-groups
Copy-Item .env.example .env
```

`CONTENT_BRAIN_DB_PATH` optionally changes the SQLite file location. API credentials are reserved for future real-provider use and are never hardcoded.

## Usage

```powershell
uv run content-brain generate --topic "Why do people procrastinate?" --format short
uv run content-brain generate --topic "Why do people procrastinate?" --format long
uv run content-brain list
uv run content-brain show <package-id>
uv run content-brain validate <package-id>
uv run content-brain export <package-id> --output package.json
```

The CLI accepts `short` and `long`; internally `long` maps to `long_form`.

## Design

`LLMProvider` is the only provider boundary. `MockProvider` creates deterministic structured output; `OpenAIProvider` reserves an adapter contract but is intentionally not wired to an SDK in this phase. The Phase 2 `ContentOrchestrator` coordinates isolated topic, concept, hook, script, claim, validation, and scoring stages. It does not embed generation logic.

Each psychology insight includes a claim, reasoning, confidence, optional source metadata, and recommended wording. Unsupported authority phrases without a source produce validation warnings. This project performs no web research.

Scripts are structured into timed sections rather than emitted as an opaque blob. SQLite retains the complete JSON package and searchable metadata, plus version, hook, title, claim, quality-score, and generation-run records. The package includes empty analytics fields for views, impressions, CTR, average view duration, average percentage viewed, likes, comments, shares, and subscribers gained.

## Development

```powershell
uv run pytest
uv run ruff check .
uv run mypy
```
