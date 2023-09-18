from __future__ import annotations

import requests
from urllib.parse import urljoin
from typing import Any, Dict, Iterator, TypeVar

from .formats import BaseResponseFormatHandler, Params, Data, Converter
from lichess.utils import noop
from lichess.exceptions import ApiError, ResponseError, CLIError
from lichess.base import BaseClient
from lichess.tokens import Token
from lichess.config import Config

"""
    This module is a copy of the utils package from the berserk library, with some modifications.
    It is used to make requests to the Lichess API.
    The original code is available here:
        https://github.com/lichess-org/berserk/blob/master/berserk/session.py
"""

T = TypeVar("T")


class Requestor(BaseClient):
    _instance: Requestor | None = None

    def init(
        self, *args: Any, **kwargs: Dict[str, Any]
    ):
        self.token_key = None
        self.session = None

    def new(self, base_url: str, default_fmt: BaseResponseFormatHandler[T], token_key: str | None = None) -> None:
        self.base_url = base_url
        self.default_fmt = default_fmt
        if token_key is not None and self.token_key != token_key:
            self.create_session(token_key=token_key)
        elif self.session is None:
            self.create_session(token_key=Config().get_option('token', 'key'))

    def create_session(self, token_key: str) -> None:
        self.token_key = token_key
        if self.token_key == '':
            raise CLIError(ValueError("No token key provided. See 'lichess token --help' for more information."))
        
        token_handler = Token()
        self.token = token_handler.get_token(self.token_key)
        session = Session(self.token)
    
        self.session = session

    def request(
        self,
        method: str,
        path: str,
        *,
        stream: bool = False,
        params: Params | None = None,
        data: Data | None = None,
        json: Dict[str, Any] | None = None,
        fmt: BaseResponseFormatHandler[Any] | None = None,
        converter: Converter[Any] = noop,
        **kwargs: Any,
    ) -> Any | Iterator[Any]:
        fmt = fmt or self.default_fmt
        url = urljoin(self.base_url, path)
        try:
            response = self.session.request(
                method,
                url,
                stream=stream,
                params=params,
                headers=fmt.headers,
                data=data,
                json=json,
                **kwargs,
            )
        except requests.RequestException as e:
            raise ApiError(e)
        if not response.ok:
            raise ResponseError(response)

        return fmt.handle(response, is_stream=stream, converter=converter)


class Session(requests.Session):
    def __init__(self, token: str) -> None:
        super().__init__()
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}