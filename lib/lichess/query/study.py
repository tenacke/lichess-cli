from __future__ import annotations

from lichess import BaseClient

class Study(BaseClient):
    _instance: Study | None = None

    def init(self) -> None:
        pass