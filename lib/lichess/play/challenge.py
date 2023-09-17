from __future__ import annotations

from lichess import BaseClient

class Challenge(BaseClient):
    _instance: Challenge | None = None

    def init(self) -> None:
        pass