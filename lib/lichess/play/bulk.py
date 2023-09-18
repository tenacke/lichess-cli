from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Bulk(Singleton):
    _instance: Bulk | None = None

    def init(self) -> None:
        pass

class BulkClient(BaseClient):
    _instance: BulkClient | None = None

    def init(self) -> None:
        self.broadcast = Bulk()