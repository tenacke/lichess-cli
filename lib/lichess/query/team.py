from __future__ import annotations

from lichess import BaseClient

class Team(BaseClient):
    _instance: Team | None = None

    def init(self) -> None:
        pass