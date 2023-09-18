from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Game(Singleton):
    _instance: Game | None = None

    def init(self) -> None:
        pass

class GameClient(BaseClient):
    _instance: GameClient | None = None

    def init(self) -> None:
        self.broadcast = Game()