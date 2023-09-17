from __future__ import annotations

from typing import cast
from requests import Response


"""
    This module is a copy of the exceptions module from the berserk library, with some modifications.
    It is used to represent the Lichess CLI errors.
    The original code is available here:
        https://github.com/lichess-org/berserk/blob/master/berserk/exceptions.py
"""

def get_message(e: Exception) -> str:
    return e.args[0] if e.args else ""


def set_message(e: Exception, value: str) -> None:
    args = list(e.args)
    if args:
        args[0] = value
    else:
        args.append(value)
    e.args = tuple(args)


class LichessError(Exception):
    message = property(get_message, set_message)


class CLIError(LichessError):
    def __init__(self, error: Exception):
        super().__init__(get_message(error))
        self.__cause__ = self.error = error


class CorruptedSourceError(LichessError):
    def __init__(self, error: Exception):
        super().__init__(get_message(error))
        self.__cause__ = self.error = error


class ApiError(LichessError):
    def __init__(self, error: Exception):
        super().__init__(get_message(error))
        self.__cause__ = self.error = error

class UserError(LichessError):
    def __init__(self, error: Exception):
        super().__init__(get_message(error))
        self.__cause__ = self.error = error


class ResponseError(ApiError):
    """Response that indicates an error."""

    # sentinal object for when None is a valid result
    __UNDEFINED = object()

    def __init__(self, response: Response):
        error = ResponseError._catch_exception(response)
        super().__init__(cast(Exception, error))
        self._cause = ResponseError.__UNDEFINED
        self.response = response
        base_message = f"HTTP {self.status_code}: {self.reason}"
        if self.cause:
            self.message = f"{base_message}: {self.cause}"

    @property
    def status_code(self):
        """HTTP status code of the response."""
        return self.response.status_code

    @property
    def reason(self):
        """HTTP status text of the response."""
        return self.response.reason

    @property
    def cause(self):
        if self._cause is ResponseError.__UNDEFINED:
            try:
                self._cause = self.response.json()
            except Exception:
                self._cause = None
        return self._cause

    @staticmethod
    def _catch_exception(response: Response):
        try:
            response.raise_for_status()
        except Exception as e:
            return e
