from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Explorer(Singleton):
    _instance: Explorer | None = None

    def init(self) -> None:
        pass

class ExplorerClient(BaseClient):
    _instance: ExplorerClient | None = None

    def init(self) -> None:
        self.broadcast = Explorer()