from __future__ import annotations

from typing import Any, Dict, Iterator
from utils import noop

from .session import Session, Requestor
from .formats import JSON, Params, Data, FormatHandler, Converter


# Client API for lichess package

class BaseClient:
    def __init__(self, session: Session, base_url: str):
        self._r = Requestor(session, base_url, default_fmt=JSON)

    
    def get(self,
            path: str,
            *,
            stream: bool = False,
            params: Params | None = None,
            data: Data | None = None,
            json: Dict[str, Any] | None = None,
            fmt: FormatHandler[Any] | None = None,
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
            fmt: FormatHandler[Any] | None = None,
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