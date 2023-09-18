from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class TV(Singleton):
    _instance: TV | None = None

    def init(self) -> None:
        pass

class TVClient(BaseClient):
    _instance: TVClient | None = None

    def init(self) -> None:
        self.broadcast = TV()