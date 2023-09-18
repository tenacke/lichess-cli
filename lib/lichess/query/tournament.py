from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Tournament(Singleton):
    _instance: Tournament | None = None

    def init(self) -> None:
        pass

class TournamentClient(BaseClient):
    _instance: TournamentClient | None = None

    def init(self) -> None:
        self.broadcast = Tournament()