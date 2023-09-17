from __future__ import annotations

from lichess import BaseClient

class Tablebase(BaseClient):
    _instance: Tablebase | None = None

    def init(self) -> None:
        pass