from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Relation(Singleton):
    _instance: Relation | None = None

    def init(self) -> None:
        pass

class RelationClient(BaseClient):
    _instance: RelationClient | None = None

    def init(self) -> None:
        self.broadcast = Relation()