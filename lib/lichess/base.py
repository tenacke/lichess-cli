from __future__ import annotations
from typing import Any, Dict

from .utils import Singleton

class BaseClient(Singleton):
    def init(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        pass

