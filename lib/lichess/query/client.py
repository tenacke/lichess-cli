from __future__ import annotations

from lichess.api.requests import RequestClient


class QueryClient(RequestClient):
    def init(self, base_url: str, token_key: str | None) -> None:
        super().init(session=self.session, base_url=base_url, token_key=token_key)

