from __future__ import annotations

import json

from typer.testing import CliRunner

from content_brain.cli import app
from content_brain.domain.models import VideoFormat
from content_brain.pipeline import ContentPipeline
from content_brain.providers.mock import MockProvider
from content_brain.repositories.sqlite import SQLiteContentRepository

TOPIC = "Why do people procrastinate even when they know what they need to do?"


def test_sqlite_save_and_load(tmp_path: object) -> None:
    path = tmp_path / "brain.db"  # type: ignore[operator]
    repository = SQLiteContentRepository(path)
    package = ContentPipeline(MockProvider()).generate(TOPIC, VideoFormat.SHORT)
    repository.save(package)
    loaded = repository.get(package.package_id)
    assert loaded is not None
    assert loaded.model_dump() == package.model_dump()
    assert len(repository.list()) == 1


def test_cli_generate_list_show_validate_and_export(tmp_path: object) -> None:
    database = tmp_path / "brain.db"  # type: ignore[operator]
    export_path = tmp_path / "package.json"  # type: ignore[operator]
    runner = CliRunner()
    generated = runner.invoke(app, ["generate", "--topic", TOPIC, "--format", "short", "--database", str(database), "--json"])
    assert generated.exit_code == 0, generated.output
    package_id = json.loads(generated.output)["package_id"]
    assert runner.invoke(app, ["list", "--database", str(database)]).exit_code == 0
    assert runner.invoke(app, ["show", package_id, "--database", str(database)]).exit_code == 0
    validation = runner.invoke(app, ["validate", package_id, "--database", str(database)])
    assert validation.exit_code == 0
    assert json.loads(validation.output)["valid"]
    exported = runner.invoke(app, ["export", package_id, "--database", str(database), "--output", str(export_path)])
    assert exported.exit_code == 0
    assert json.loads(export_path.read_text(encoding="utf-8"))["package_id"] == package_id
