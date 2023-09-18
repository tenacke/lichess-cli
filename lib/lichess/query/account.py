from __future__ import annotations

from typing import Any, Dict, Iterator

from lichess.utils import convert_to_boolean, Singleton, IOHandler
from lichess.base import BaseClient
from .client import QueryClient

API_URL = "https://lichess.org"

class Account(Singleton):
    _instance: Account | None = None

    def init(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        self.query = QueryClient(base_url=API_URL, token_key=kwargs.get('token_key', None))

    def get_info(self, ) -> Dict[str, Any] | Iterator[Any]:
        path = '/api/account'
        return self.query.get(path)

    def get_email(self, ) -> str:
        path = '/api/account/email'
        return self.query.get(path)['email']

    def get_preferences(self, ):
        path = '/api/account/preferences'
        return self.query.get(path)

    def get_kid_status(self):
        path = '/api/account/kid'
        return self.query.get(path)['kid']

    def set_kid_status(self, value: bool):
        path = '/api/account/kid'
        params = {'v': convert_to_boolean(value)}
        return self.query.post(path, params=params)

    def upgrade_bot(self, ):
        path = '/api/bot/account/upgrade'
        return self.query.post(path)
    

class AccountClient(BaseClient):
    _instance: AccountClient | None = None

    def init(self, *args: Any, token_key: str | None, **kwargs: Dict[str, Any]) -> None:
        self.account = Account(token_key=token_key)
        self.io = IOHandler(verbose=True)

    def info(self, ) -> None:
        self.io.print(self.account.get_info())

    def email(self, ) -> None:
        self.io.print(self.account.get_email())

    def preferences(self, ) -> None:
        self.io.print(self.account.get_preferences())

    def kid(self, mode: bool | None) -> None:
        if mode is not None:
            self.io.print(self.account.set_kid_status(mode))
        else:
            self.io.print(self.account.get_kid_status())

    def bot(self, ) -> None:
        self.io.print(self.account.upgrade_bot())
