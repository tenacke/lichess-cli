from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Challenge(Singleton):
    _instance: Challenge | None = None

    def init(self) -> None:
        pass

class ChallengeClient(BaseClient):
    _instance: ChallengeClient | None = None

    def init(self) -> None:
        self.broadcast = Challenge()