from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Puzzle(Singleton):
    _instance: Puzzle | None = None

    def init(self) -> None:
        pass

class PuzzleClient(BaseClient):
    _instance: PuzzleClient | None = None

    def init(self) -> None:
        self.broadcast = Puzzle()