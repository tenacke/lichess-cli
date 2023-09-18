#!/usr/bin/env python3

from __future__ import annotations

import sys
import inspect

from lichess.args import Args
from lichess.config import Config
from lichess.client import LichessClient
from lichess.exceptions import UserError


if __name__ == '__main__':
    try:
        args = Args()
        config = Config()
        lichess = LichessClient(verbose=True)

        command = args.get_command()
        subcommand = args.get_subcommand()
        arguments = args.get_arguments()

        module = getattr(lichess, command)
        module_parameters = inspect.signature(module).parameters
        client = module(**{k: arguments[k] for k in module_parameters})

        method = getattr(client, subcommand)
        method_parameters = inspect.signature(method).parameters
        method(**{k: arguments[k] for k in method_parameters})

    except UserError:
        info = sys.exc_info()
        message = info[1]
        print(__file__, 'error', message, sep=': ', file=sys.stderr)
        sys.exit(1)


