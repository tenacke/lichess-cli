from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Simuls(Singleton):
    _instance: Simuls | None = None

    def init(self) -> None:
        pass

class SimulsClient(BaseClient):
    _instance: SimulsClient | None = None

    def init(self) -> None:
        self.broadcast = Simuls()