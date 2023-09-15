#!/usr/bin/env python3

from __future__ import annotations

import os
import sys
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
print(sys.path)

from typing import Any, Dict

from .exceptions import LichessError, CorruptedSourceError
from lichess import BaseClient
from utils.tokens import Token


class LichessClient(BaseClient):
    def init(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        client = BaseClient(*args, **kwargs)
        self.set_credentials(*client.get_credentials())

    def get_command(self) -> str:
        return self.get_argument('command')
    
    def get_subcommand(self) -> list[str] | None:
        return self.get_argument('subcommand')


def main():
    client = LichessClient()
    token = Token()
    print(token.list())
    try:
        command = client.get_command()
        if command == 'help':
            subcommand = client.get_subcommand()
            if subcommand is None:
                subprocess.call(['lichess', '--help'])
            else:
                subprocess.call(['lichess'] + subcommand + ['--help'])
        else:
            def find_package(command, directory=os.path.dirname(os.path.realpath(__file__))):
                for elem in os.listdir(directory):
                    if os.path.isdir(os.path.join(directory, elem)):
                        pkg = find_package(command, os.path.join(directory, elem))
                        if pkg is not None:
                            return pkg
                    elif elem.startswith(command) and elem.endswith('.py'):
                        return os.path.basename(directory)
                return None
            
            package = find_package(command)
            if package is None:
                raise CorruptedSourceError(FileNotFoundError(f'Module {command}.py not found!\nTry checking LICHESS_HOME environment variable or reinstalling the program'))

    except LichessError:
        info = sys.exc_info()
        type = info[0].__name__
        message = info[1]
        print(__file__, type, message, sep=': ', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()