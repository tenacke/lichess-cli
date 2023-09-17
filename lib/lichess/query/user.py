from __future__ import annotations

from lichess import BaseClient

class User(BaseClient):
    _instance: User | None = None

    def init(self) -> None:
        pass