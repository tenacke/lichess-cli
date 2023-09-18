from __future__ import annotations
import json
from typing import Any, Callable, Dict, Iterator, Mapping, List, Type, TypeVar, Union, cast

import ndjson  # type: ignore
from requests import Response

from .base import BaseResponseFormatHandler

T = TypeVar("T")

Params = Mapping[str, Union[int, bool, str, None]]
Data = Union[str, Params]
Converter = Callable[[T], T]

"""
    This module is a copy of the berserk module from the berserk library, with some modifications.
    It is used to parse the Lichess API responses.
    The original code is available here:
        https://github.com/lichess-org/berserk/blob/master/berserk/formats.py
"""

class JsonHandler(BaseResponseFormatHandler[Dict[str, Any]]):
    def __init__(
        self, mime_type: str, decoder: Type[json.JSONDecoder] = json.JSONDecoder
    ):
        super().__init__(mime_type=mime_type)
        self.decoder = decoder

    def parse(self, response: Response) -> Dict[str, Any]:
        return response.json(cls=self.decoder)

    def parse_stream(self, response: Response) -> Iterator[Dict[str, Any]]:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                yield json.loads(decoded_line)


class PgnHandler(BaseResponseFormatHandler[str]):
    def __init__(self):
        super().__init__(mime_type="application/x-chess-pgn")

    def parse(self, response: Response) -> str:
        return response.text

    def parse_stream(self, response: Response) -> Iterator[str]:
        lines: List[str] = []
        last_line = True
        for line in response.iter_lines():
            decoded_line = line.decode("utf-8")
            if last_line or decoded_line:
                lines.append(decoded_line)
            else:
                yield "\n".join(lines).strip()
                lines = []
            last_line = decoded_line

        if lines:
            yield "\n".join(lines).strip()


class TextHandler(BaseResponseFormatHandler[str]):
    def __init__(self):
        super().__init__(mime_type="text/plain")

    def parse(self, response: Response) -> str:
        return response.text

    def parse_stream(self, response: Response) -> Iterator[str]:
        yield from response.iter_lines()


#: Basic text
TEXT = TextHandler()

#: Handles vanilla JSON
JSON = JsonHandler(mime_type="application/json")

#: Handle vanilla JSON where the response is a top-level list (this is only needed bc of type checking)
JSON_LIST = cast(BaseResponseFormatHandler[List[Dict[str, Any]]], JSON)

#: Handles oddball LiChess JSON (normal JSON, crazy MIME type)
LIJSON = JsonHandler(mime_type="application/vnd.lichess.v3+json")

#: Handles newline-delimited JSON
NDJSON = JsonHandler(mime_type="application/x-ndjson", decoder=ndjson.Decoder)  # type: ignore

#: Handles newline-delimited JSON where the response is a top-level list (this is only needed bc of type checking, if not streaming NJDSON, the result is always a list)
NDJSON_LIST = cast(BaseResponseFormatHandler[List[Dict[str, Any]]], NDJSON)

#: Handles PGN
PGN = PgnHandler()
