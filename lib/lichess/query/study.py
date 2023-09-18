from __future__ import annotations

from lichess.base import BaseClient
from lichess.utils import Singleton

class Study(Singleton):
    _instance: Study | None = None

    def init(self) -> None:
        pass

class StudyClient(BaseClient):
    _instance: StudyClient | None = None

    def init(self) -> None:
        self.broadcast = Study()