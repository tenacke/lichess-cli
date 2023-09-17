from __future__ import annotations

from lichess import BaseClient

class Message(BaseClient):
    _instance: Message | None = None

    def init(self) -> None:
        pass