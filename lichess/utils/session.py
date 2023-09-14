from __future__ import annotations

import requests
from urllib.parse import urljoin
from typing import Any, Dict, Iterator

from utils.formats import FormatHandler, Params, Data, Converter
from utils import noop, T
from utils.exceptions import ApiError, ResponseError

"""
    This module is a copy of the utils package from the berserk library, with some modifications.
    It is used to make requests to the Lichess API.
    The original code is available here:
        https://github.com/lichess-org/berserk/blob/master/berserk/session.py
"""

class Requestor:
    def __init__(
        self, session: requests.Session, base_url: str, default_fmt: FormatHandler[T]
    ):
        self.session = session
        self.base_url = base_url
        self.default_fmt = default_fmt

    def request(
        self,
        method: str,
        path: str,
        *,
        stream: bool = False,
        params: Params | None = None,
        data: Data | None = None,
        json: Dict[str, Any] | None = None,
        fmt: FormatHandler[Any] | None = None,
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