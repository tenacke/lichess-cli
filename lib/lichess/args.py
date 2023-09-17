from __future__ import annotations

import os
import json
from argparse import Namespace, ArgumentParser
from typing import Any, Dict, List

from .base import BaseClient
from .utils import ETC, BaseCommandFormatter
from .exceptions import CorruptedSourceError


PARSER_FILE = os.path.join(ETC, 'parser.json')

class MainCommandFormatter(BaseCommandFormatter):
    pass


class SubCommandFormatter(BaseCommandFormatter):
    pass


def parse_args() -> Namespace:
    def set_subparser(parser: Any, parser_dict: Dict[str, Any]) -> None:
        subparsers = parser.add_subparsers(**parser_dict['kwargs'])
        for subparser_dict in parser_dict['subparsers']:
            subparser = subparsers.add_parser(**subparser_dict['kwargs'], formatter_class=SubCommandFormatter)
            if subparser_dict['parser_type'] == 'subparser':
                set_subparser(subparser, subparser_dict['subparser'])
            elif subparser_dict['parser_type'] == 'argument':
                set_argument(subparser, subparser_dict['args'])
    
    def set_argument(parser: Any, arguments: Dict[str, Any]) -> None:
        for argument_dict in arguments:
            parser.add_argument(*argument_dict['name'], **argument_dict['kwargs'])

    if not os.path.exists(ETC):
        raise CorruptedSourceError(NotADirectoryError(f'Configuration directory {ETC} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
    
    if not os.path.isfile(PARSER_FILE):
        raise CorruptedSourceError(FileNotFoundError(f'Default configuration file {PARSER_FILE} does not exist!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))
    
    try:
        parser_dict = json.load(open(PARSER_FILE, 'r'))
    except json.JSONDecodeError as e:
        raise CorruptedSourceError(e)

    parser = ArgumentParser(**parser_dict['kwargs'], formatter_class=MainCommandFormatter)
    if parser_dict['parser_type'] == 'subparser':
        set_subparser(parser, parser_dict['subparser'])
    elif parser_dict['parser_type'] == 'argument':
        set_argument(parser, parser_dict)

    return parser.parse_args()


class Args(BaseClient):
    _instance: Args | None = None

    def init(self):
        self.args = parse_args()

    def has_argument(self, argument: str) -> bool:
        return hasattr(self.args, argument)

    def get_argument(self, argument: str) -> Any | List[Any]:
        if hasattr(self.args, argument):
            return getattr(self.args, argument)
        raise KeyError(f'Argument {argument} not found')
    
    def get_arguments(self) -> Dict[str, Any]:
        arguments_dict = self.args.__dict__.copy()
        arguments_dict.pop('command')
        arguments_dict.pop('subcommand')
        return arguments_dict
    
    def get_command(self) -> str:
        if hasattr(self.args, 'command'):
            return self.args.command
        raise AttributeError('No command found in args')
        
    def get_subcommand(self) -> str:
        if hasattr(self.args, 'subcommand'):
            return self.args.subcommand
        raise AttributeError('No subcommand found in args')