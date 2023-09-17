from __future__ import annotations

from lichess import BaseClient

class Relations(BaseClient):
    _instance: Relations | None = None

    def init(self) -> None:
        pass