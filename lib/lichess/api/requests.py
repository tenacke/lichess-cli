from __future__ import annotations

from typing import Any, Dict, Iterator

from .session import Requestor
from .formats import JSON, Params, Data, BaseResponseFormatHandler, Converter
from lichess.base import BaseClient
from lichess.utils import noop

# Requests Client API for lichess package

class RequestClient(BaseClient):
    _instance: RequestClient | None = None

    def init(self, *args: Any, **kwargs: Dict[str, Any]):
        pass

    def new(self, base_url: str, token_key: str | None) -> None:
        self._r = Requestor(base_url=base_url, default_fmt=JSON, token_key=token_key)

    def get(self,
            path: str,
            *,
            stream: bool = False,
            params: Params | None = None,
            data: Data | None = None,
            json: Dict[str, Any] | None = None,
            fmt: BaseResponseFormatHandler[Any] | None = None,
            converter: Converter[Any] = noop,
            **kwargs: Any) -> Any | Iterator[Any]:
        return self._r.request("GET",
                                path,
                                params=params,
                                stream=stream,
                                fmt=fmt,
                                converter=converter,
                                data=data,
                                json=json,
                                **kwargs, 
        )
    
    def post(self,
            path: str,
            *,
            stream: bool = False,
            params: Params | None = None,
            data: Data | None = None,
            json: Dict[str, Any] | None = None,
            fmt: BaseResponseFormatHandler[Any] | None = None,
            converter: Converter[Any] = noop,
            **kwargs: Any) -> Any | Iterator[Any]:
        return self._r.request("POST",
                                path,
                                params=params,
                                stream=stream,
                                fmt=fmt,
                                converter=converter,
                                data=data,
                                json=json,
                                **kwargs, 
        )