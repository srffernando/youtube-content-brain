from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    database_path: Path
    openai_api_key: str | None

    @classmethod
    def from_environment(cls) -> Settings:
        return cls(
            database_path=Path(os.getenv("CONTENT_BRAIN_DB_PATH", "content_brain.db")),
            openai_api_key=os.getenv("CONTENT_BRAIN_OPENAI_API_KEY"),
        )
