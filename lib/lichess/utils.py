from __future__ import annotations


import os
from argparse import HelpFormatter, Action, _MutuallyExclusiveGroup
from typing import Any, Dict, Iterable, TypeVar
from gettext import gettext as _

from .exceptions import LichessError

T = TypeVar('T')

BOOLEAN_STATES = {'1': True, 'yes': True, 'true': True, 'on': True,
                    '0': False, 'no': False, 'false': False, 'off': False}

DEFAULT_HOME = os.path.expanduser('~/.lichess')

HOME = os.getenv('LICHESS_HOME')
if HOME is None:
    HOME = DEFAULT_HOME
ETC = os.path.join(HOME, 'etc')
MAN = os.path.join(HOME, 'share', 'mann')


def noop(arg: T) -> T:
    return arg

def convert_to_boolean( value):
        """Return a boolean value translating from other types if necessary.
        """
        if value.lower() not in BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % value)
        return BOOLEAN_STATES[value.lower()]


class Singleton:
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Dict[str, Any]) -> Singleton:
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.init(*args, **kwargs)
        cls._instance.new(*args, **kwargs)
        return cls._instance
    
    def init(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        raise NotImplementedError('This method must be implemented in the subclass')
    
    def new(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        # This method is used to set properties for all new singleton calls
        # It is similar to constructor, but it is executed for all new calls
        # It is not necessary to implement it in the subclass so it does nothing by default
        # It is called after init method if it is a new instance
        pass


class IOHandler:
    def __init__(self, verbose: bool = True) -> None:
        self.verbose = verbose 
    
    def print(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        if self.verbose:
            print(*args, **kwargs)

    def input(self, *args: Any, **kwargs: Dict[str, Any]) -> str:
        if self.verbose:
            return input(*args, **kwargs)
        else:
            return LichessError(PermissionError(_('Input is not allowed in non-interactive mode')))
        
    def confirm(self, *args: Any, **kwargs: Dict[str, Any]) -> bool:
        if self.verbose:
            return input(*args, **kwargs).lower() == 'y'
        else:
            return LichessError(PermissionError(_('Input is not allowed in non-interactive mode')))


class BaseCommandFormatter(HelpFormatter):
    def _format_usage(self, usage: str | None, actions: Iterable[Action], groups: Iterable[_MutuallyExclusiveGroup], prefix: str | None) -> str:
        if prefix is None:
            prefix = _('Usage: ')
        return super()._format_usage(usage, actions, groups, prefix)
    

    def _fill_text(self, text: str, width: int, indent: str) -> str:
        return ''.join(indent + line for line in text.splitlines(keepends=True))

    def _split_lines(self, text: str, width: int) -> list[str]:
        if '\n' in text:
            return text.splitlines()
        return super()._split_lines(text, width)
    