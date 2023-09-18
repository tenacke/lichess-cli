from __future__ import annotations
from typing import Any, Dict

from lichess.api.requests import RequestClient


class QueryClient(RequestClient):
    def init(self, *args: Any, **kwargs: Dict[str, Any]):
        pass

