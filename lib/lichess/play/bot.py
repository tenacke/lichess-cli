from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Bot(Singleton):
    _instance: Bot | None = None

    def init(self) -> None:
        pass

class BotClient(BaseClient):
    _instance: BotClient | None = None

    def init(self) -> None:
        self.broadcast = Bot()