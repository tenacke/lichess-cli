from __future__ import annotations

import os
import json
from typing import TypeVar, Any, Dict, Iterable
from argparse import HelpFormatter, Action, _MutuallyExclusiveGroup, ArgumentParser, Namespace
from configparser import RawConfigParser, ConfigParser, ParsingError
from gettext import gettext as _

from utils.exceptions import CorruptedSourceError, LichessError
from lichess import ETC

T = TypeVar('T')
U = TypeVar('U')

BOOLEAN_STATES = {'1': True, 'yes': True, 'true': True, 'on': True,
                    '0': False, 'no': False, 'false': False, 'off': False}

def noop(arg: T) -> T:
    return arg

def convert_to_boolean( value):
        """Return a boolean value translating from other types if necessary.
        """
        if value.lower() not in BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % value)
        return BOOLEAN_STATES[value.lower()]


def parse_config() -> RawConfigParser:
    config = ConfigParser(inline_comment_prefixes=('#', ';'))
    
    if not os.path.exists(ETC):
        raise CorruptedSourceError(NotADirectoryError(f'Configuration directory {ETC} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
    
    try:
        if os.path.isfile(os.path.join(ETC, 'defaults.conf')):
            config.read(os.path.join(ETC, 'defaults.conf'))
        else:
            raise CorruptedSourceError(FileNotFoundError(f'Default configuration file {os.path.join(ETC, "defaults.conf")} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
        
        if os.path.isfile(os.path.join(ETC, 'lichess.conf')):
            config.read(os.path.join(ETC, 'lichess.conf'))
    except ParsingError as e:
        e.message = f'Error parsing configuration file {e.source}:\n{e.message}'
        raise CorruptedSourceError(e)

    return config

def parse_args() -> Namespace:
    def set_subparser(parser: Any, parser_dict: Dict[str, Any]) -> None:
        subparsers = parser.add_subparsers(**parser_dict['kwargs'])
        for subparser_dict in parser_dict['subparsers']:
            subparser = subparsers.add_parser(**subparser_dict['kwargs'], formatter_class=SubcommandFormatter)
            if subparser_dict['parser_type'] == 'subparser':
                set_subparser(subparser, subparser_dict['subparser'])
            elif subparser_dict['parser_type'] == 'argument':
                set_argument(subparser, subparser_dict['args'])
    
    def set_argument(parser: Any, arguments: Dict[str, Any]) -> None:
        for argument_dict in arguments:
            parser.add_argument(*argument_dict['name'], **argument_dict['kwargs'])

    if not os.path.exists(ETC):
        raise CorruptedSourceError(NotADirectoryError(f'Configuration directory {ETC} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
    
    parser_file = os.path.join(ETC, 'parser.json')
    if not os.path.isfile(parser_file):
        raise CorruptedSourceError(FileNotFoundError(f'Default configuration file {parser_file} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
    
    try:
        parser_dict = json.load(open(parser_file, 'r'))
    except json.JSONDecodeError as e:
        raise CorruptedSourceError(e)

    parser = ArgumentParser(**parser_dict['kwargs'], formatter_class=MainFormatter)
    if parser_dict['parser_type'] == 'subparser':
        set_subparser(parser, parser_dict['subparser'])
    elif parser_dict['parser_type'] == 'argument':
        set_argument(parser, parser_dict)

    return parser.parse_args()

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


class BaseFormatter(HelpFormatter):
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
    

class MainFormatter(BaseFormatter):
    pass


class SubcommandFormatter(BaseFormatter):
    pass


class IOHandler(Singleton):
    def init(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        self.verbose = True # default value

    def new(self, verbose: bool | None = None) -> None:
        if verbose is not None:
            self.verbose = verbose
    
    def print(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        if self.verbose:
            print(*args, **kwargs)

    def input(self, *args: Any, **kwargs: Dict[str, Any]) -> str:
        if self.verbose:
            return input(*args, **kwargs)
        else:
            return LichessError(PermissionError(_('Input is not allowed in non-interactive mode')))



