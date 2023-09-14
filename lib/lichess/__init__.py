import os

DEFAULT_HOME = os.path.expanduser('~/.lichess')

HOME = os.getenv('LICHESS_HOME')
if HOME is None:
    HOME = DEFAULT_HOME