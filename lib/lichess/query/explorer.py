from __future__ import annotations

from lichess import BaseClient

class Explorer(BaseClient):
    _instance: Explorer | None = None

    def init(self) -> None:
        pass