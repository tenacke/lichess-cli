from __future__ import annotations

from lichess import BaseClient

class Simuls(BaseClient):
    _instance: Simuls | None = None

    def init(self) -> None:
        pass