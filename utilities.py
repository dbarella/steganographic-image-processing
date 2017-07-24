"""Utilities."""

import sys
from typing import Dict, Optional

RGB_RANGE = 0b11111111


def bit_mask(size: int) -> int:
    """Return a bit mask with `size` number of 1-s."""
    if size < 0:
        raise ValueError('{0:d} B TOO SMALL BB'.format(size))
    elif size == 0:
        return 0
    else:
        return int('1' * size, base=2)


def query_user(question: str, default: Optional[bool]=None) -> bool:
    """Ask the user a yes/no question and return the response.

    Copied from
    https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    if default is None:
        prompt = ' [y/n] '
    elif default == 'yes':
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    response_to_bool: Dict[str, bool] = {
        'yes': True,
        'y': True,
        'no': False,
        'n': False
    }
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return response_to_bool_map[default]
        elif choice in response_to_bool_map:
            return response_to_bool_map[choice]
        else:
            print(
                'Please respond with one of "{0:s}"'.format(
                    '", "'.join(response_to_bool_map.keys())))

