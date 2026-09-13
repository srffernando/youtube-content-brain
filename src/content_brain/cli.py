from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from content_brain.config import Settings
from content_brain.domain.models import ContentPackage, VideoFormat
from content_brain.domain.validation import validate_package
from content_brain.pipeline import ContentPipeline
from content_brain.providers.mock import MockProvider
from content_brain.repositories.sqlite import SQLiteContentRepository

app = typer.Typer(help="Generate structured YouTube psychology content packages.", no_args_is_help=True)


def _repo(database: Path | None = None) -> SQLiteContentRepository:
    return SQLiteContentRepository(database or Settings.from_environment().database_path)


def _format(value: str) -> VideoFormat:
    normalized = "long_form" if value == "long" else value
    try:
        return VideoFormat(normalized)
    except ValueError as error:
        raise typer.BadParameter("Use 'short' or 'long'.") from error


@app.command()
def generate(
    topic: Annotated[str, typer.Option(help="The video topic or question.")],
    format: Annotated[str, typer.Option(help="short or long")] = "short",
    database: Annotated[Path | None, typer.Option(help="SQLite database path.")] = None,
) -> None:
    package = ContentPipeline(MockProvider()).generate(topic, _format(format))
    _repo(database).save(package)
    typer.echo(package.model_dump_json(indent=2))


@app.command(name="list")
def list_packages(database: Annotated[Path | None, typer.Option(help="SQLite database path.")] = None) -> None:
    packages = _repo(database).list()
    typer.echo(json.dumps([{ "package_id": item.package_id, "topic": item.topic, "format": item.format.value, "quality_score": item.quality_score.overall } for item in packages], indent=2))


def _load_or_exit(package_id: str, database: Path | None) -> tuple[SQLiteContentRepository, ContentPackage]:
    repository = _repo(database)
    package = repository.get(package_id)
    if package is None:
        raise typer.BadParameter(f"No package found with ID {package_id}.")
    return repository, package


@app.command()
def show(package_id: str, database: Annotated[Path | None, typer.Option(help="SQLite database path.")] = None) -> None:
    _, package = _load_or_exit(package_id, database)
    typer.echo(package.model_dump_json(indent=2))


@app.command()
def validate(package_id: str, database: Annotated[Path | None, typer.Option(help="SQLite database path.")] = None) -> None:
    _, package = _load_or_exit(package_id, database)
    result = validate_package(package)
    typer.echo(result.model_dump_json(indent=2))


@app.command()
def export(
    package_id: str,
    output: Annotated[Path | None, typer.Option(help="Output JSON path; stdout when omitted.")] = None,
    database: Annotated[Path | None, typer.Option(help="SQLite database path.")] = None,
) -> None:
    _, package = _load_or_exit(package_id, database)
    payload = package.model_dump_json(indent=2)
    if output:
        output.write_text(payload, encoding="utf-8")
        typer.echo(str(output))
    else:
        typer.echo(payload)


if __name__ == "__main__":
    app()
