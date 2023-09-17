from __future__ import annotations

from lichess import BaseClient

class TV(BaseClient):
    _instance: TV | None = None

    def init(self) -> None:
        pass