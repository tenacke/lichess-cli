from __future__ import annotations

from lichess import BaseClient

class Broadcast(BaseClient):
    _instance: Broadcast | None = None

    def init(self) -> None:
        pass