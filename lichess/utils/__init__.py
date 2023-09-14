from __future__ import annotations

from typing import TypeVar
import datetime


T = TypeVar("T")

def noop(arg: T) -> T:
    return arg