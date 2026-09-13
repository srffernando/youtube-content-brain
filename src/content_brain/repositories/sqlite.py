from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from content_brain.domain.models import ContentPackage
from content_brain.repositories.base import ContentRepository


class SQLiteContentRepository(ContentRepository):
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute("""CREATE TABLE IF NOT EXISTS content_packages (
                package_id TEXT PRIMARY KEY, topic TEXT NOT NULL, format TEXT NOT NULL,
                selected_hook TEXT NOT NULL, selected_title TEXT NOT NULL,
                quality_score REAL NOT NULL, provider TEXT NOT NULL, model TEXT NOT NULL,
                prompt_version TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
                package_json TEXT NOT NULL
            )""")
            connection.execute("""CREATE TABLE IF NOT EXISTS content_versions (
                package_id TEXT NOT NULL, pipeline_version TEXT NOT NULL, prompt_version TEXT NOT NULL,
                created_at TEXT NOT NULL, PRIMARY KEY (package_id, pipeline_version)
            )""")
            connection.execute("""CREATE TABLE IF NOT EXISTS hooks (
                package_id TEXT NOT NULL, text TEXT NOT NULL, score REAL NOT NULL, selected INTEGER NOT NULL
            )""")
            connection.execute("""CREATE TABLE IF NOT EXISTS titles (
                package_id TEXT NOT NULL, text TEXT NOT NULL, score REAL NOT NULL, selected INTEGER NOT NULL
            )""")
            connection.execute("""CREATE TABLE IF NOT EXISTS claims (
                package_id TEXT NOT NULL, claim TEXT NOT NULL, claim_type TEXT NOT NULL, confidence TEXT NOT NULL, source_json TEXT
            )""")
            connection.execute("""CREATE TABLE IF NOT EXISTS quality_scores (
                package_id TEXT PRIMARY KEY, score REAL NOT NULL, status TEXT NOT NULL, warnings_json TEXT NOT NULL
            )""")
            connection.execute("""CREATE TABLE IF NOT EXISTS generation_runs (
                package_id TEXT PRIMARY KEY, provider TEXT NOT NULL, model TEXT NOT NULL, prompt_version TEXT NOT NULL,
                pipeline_version TEXT NOT NULL, created_at TEXT NOT NULL
            )""")

    def save(self, package: ContentPackage) -> ContentPackage:
        payload = package.model_dump_json()
        with self._connect() as connection:
            connection.execute("""INSERT INTO content_packages
                (package_id, topic, format, selected_hook, selected_title, quality_score, provider, model, prompt_version, created_at, updated_at, package_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(package_id) DO UPDATE SET updated_at=excluded.updated_at, package_json=excluded.package_json,
                selected_hook=excluded.selected_hook, selected_title=excluded.selected_title, quality_score=excluded.quality_score""",
                (package.package_id, package.topic, package.format.value, package.selected_hook.text, package.selected_title.text, package.quality_score.overall, package.provider, package.model, package.prompt_version, package.created_at.isoformat(), package.updated_at.isoformat(), payload))
            connection.execute("DELETE FROM hooks WHERE package_id = ?", (package.package_id,))
            connection.execute("DELETE FROM titles WHERE package_id = ?", (package.package_id,))
            connection.execute("DELETE FROM claims WHERE package_id = ?", (package.package_id,))
            connection.executemany("INSERT INTO hooks VALUES (?, ?, ?, ?)", [(package.package_id, item.text, item.score, int(item.text == package.selected_hook.text)) for item in package.hooks])
            connection.executemany("INSERT INTO titles VALUES (?, ?, ?, ?)", [(package.package_id, item.text, item.score, int(item.text == package.selected_title.text)) for item in package.titles])
            connection.executemany("INSERT INTO claims VALUES (?, ?, ?, ?, ?)", [(package.package_id, item.claim, item.claim_type.value, item.confidence.value, item.source.model_dump_json() if item.source else None) for item in package.claims])
            connection.execute("INSERT OR REPLACE INTO content_versions VALUES (?, ?, ?, ?)", (package.package_id, package.pipeline_version, package.prompt_version, package.created_at.isoformat()))
            connection.execute("INSERT OR REPLACE INTO quality_scores VALUES (?, ?, ?, ?)", (package.package_id, package.quality_score.overall, package.quality_score.status.value, json.dumps(package.validation.warnings)))
            connection.execute("INSERT OR REPLACE INTO generation_runs VALUES (?, ?, ?, ?, ?, ?)", (package.package_id, package.provider, package.model, package.prompt_version, package.pipeline_version, package.created_at.isoformat()))
        return package

    def get(self, package_id: str) -> ContentPackage | None:
        with self._connect() as connection:
            row = connection.execute("SELECT package_json FROM content_packages WHERE package_id = ?", (package_id,)).fetchone()
        return ContentPackage.model_validate_json(row["package_json"]) if row else None

    def list(self) -> list[ContentPackage]:
        with self._connect() as connection:
            rows = connection.execute("SELECT package_json FROM content_packages ORDER BY created_at DESC").fetchall()
        return [ContentPackage.model_validate_json(row["package_json"]) for row in rows]
