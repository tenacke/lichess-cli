from __future__ import annotations

from typing import TypeVar

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
