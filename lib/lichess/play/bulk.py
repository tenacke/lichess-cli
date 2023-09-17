from __future__ import annotations

from lichess import BaseClient

class Bulk(BaseClient):
    _instance: Bulk | None = None

    def init(self) -> None:
        pass