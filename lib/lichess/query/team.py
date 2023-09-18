from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Team(Singleton):
    _instance: Team | None = None

    def init(self) -> None:
        pass

class TeamClient(BaseClient):
    _instance: TeamClient | None = None

    def init(self) -> None:
        self.broadcast = Team()