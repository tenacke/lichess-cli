from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Message(Singleton):
    _instance: Message | None = None

    def init(self) -> None:
        pass

class MessageClient(BaseClient):
    _instance: MessageClient | None = None

    def init(self) -> None:
        self.broadcast = Message()