from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class User(Singleton):
    _instance: User | None = None

    def init(self) -> None:
        pass

class UserClient(BaseClient):
    _instance: UserClient | None = None

    def init(self) -> None:
        self.broadcast = User()