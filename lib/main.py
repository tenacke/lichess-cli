#!/usr/bin/env python3

from __future__ import annotations

import sys

from lichess.args import Args
from lichess.config import Config
from lichess.client import LichessClient
from lichess.exceptions import UserError


if __name__ == '__main__':
    try:
        args = Args()
        config = Config()
        client = LichessClient(verbose=True)
        module = getattr(client, args.get_command())()
        getattr(module, args.get_subcommand())(**args.get_arguments())
    except UserError:
        info = sys.exc_info()
        message = info[1]
        print(__file__, 'error', message, sep=': ', file=sys.stderr)
        sys.exit(1)


