from __future__ import annotations

from typing import Iterator, Callable, Generic, TypeVar
from requests import Response

from lichess.utils import noop

T = TypeVar("T")


class BaseResponseFormatHandler(Generic[T]):
    def __init__(self, mime_type: str):
        self.mime_type = mime_type
        self.headers = {"Accept": mime_type}

    def handle(
        self,
        response: Response,
        is_stream: bool,
        converter: Callable[[T], T] = noop,
    ) -> T | Iterator[T]:
        if is_stream:
            return map(converter, iter(self.parse_stream(response)))
        else:
            return converter(self.parse(response))

    def parse(self, response: Response) -> T:
        raise NotImplementedError

    def parse_stream(self, response: Response) -> Iterator[T]:
        raise NotImplementedError

