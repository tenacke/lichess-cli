#!/usr/bin/env python3

from __future__ import annotations

import sys

from lichess.args import Args
from lichess.config import Config
from lichess.commands import LichessClient
from lichess.exceptions import LichessError

def main():
    """try:
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
        sys.exit(1)"""

if __name__ == '__main__':
    try:
        args = Args()
        config = Config()
    except LichessError:
        info = sys.exc_info()
        type = info[0].__name__
        message = info[1]
        print(__file__, type, message, sep=': ', file=sys.stderr)
        sys.exit(1)


