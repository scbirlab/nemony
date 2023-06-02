"""Encoding Python objects as mnemonic adjective-noun pairs.

Currently supports strings, iterables, floats and ints.

"""

from __future__ import annotations

from typing import Union
from collections.abc import Sequence, Iterable

from functools import singledispatch
import hashlib
import os
import sys

import yaml

def _get_data_path():

    return os.path.join(os.path.dirname(__file__), 'words.yml')


def _load_corpus():

    _data_path = _get_data_path()

    with open(_data_path, 'r') as f:
        _words = yaml.safe_load(f)

    return _words


def _get_wordlist(full: bool = False) -> Sequence[Sequence[str]]:

    _words = _load_corpus()

    versions = _words['versions']
    word_lists = _words['word lists']
    latest_version = versions[0]

    adjectives = list(set(word_lists[latest_version]['adjectives']))
    adjectives.sort()
    nouns = list(set(word_lists[latest_version]['nouns']))
    nouns.sort()

    if full:
        return adjectives, nouns, latest_version, _words
    else:
        return adjectives, nouns
    

@singledispatch
def hash(x, *args, **kwargs) -> str:

    """Hash an object using SHA-256 and take the first `n` hexadecimal digits.

    Parameters
    ----------
    x : str | int | float | Iterable
        Object to hash.
    n : int, optional
        Truncate to first n digits. Default: use all 64 digits.
    listsep : str, optional
        Character to use to separate entries of iterable. Default: newline.

    Returns 
    -------
    str
        Hexadecimal representation of hashed string.

    Raises
    ------
    TypeError
        If the object is not supported.
    
    Examples
    --------
    >>> hash('world')
    '486ea46224d1bb4fb680f34f7c9ad96a8f24ec88be73ea8e5a6c65260e9cb8a7'
    >>> hash('world', n=8)
    '486ea462'
    >>> hash(5., n=8)
    'a19a1584'
    >>> hash(['hello', 'world']) == hash(('hello', 'world'))
    True

    """
    
    raise TypeError(f'Cannot hash object of type {type(x)}')


@hash.register
def _(x: str, 
      n: int = None) -> str:
    
    """Hash a string using SHA-256 and take the first `n` hexadecimal digits."""
    
    n = n or 64

    return hashlib.sha256(x.encode('utf-8')).hexdigest()[:n]


@hash.register
def _(x: int, 
      n: int = None) -> str:
    
    """Hash an integer."""

    return hash(str(x), n=n or 64)

@hash.register
def _(x: float, 
      n: int = None) -> str:
    
    """Hash a float."""

    return hash(str(x), n=n or 64)


@hash.register
def _(x: Iterable, 
      n: int = None,
      listsep: str = '\n') -> str:
    
    """Hash an iterable object."""

    return hash(listsep.join(map(str, x)), n=n or 64)


def encode(x: Union[str, int, float, Iterable], 
           sep: str = '_',
           n: int = 8,
           wordlist: Sequence[Sequence[str], Sequence[str]] = None) -> str:
    
    """Encode an object as an adjective-noun pair.

    Works for strings, integers, floats, and iterables containing those
    types. 

    Parameters
    ----------
    x : str | int | float | Iterable
        Python object to encode.
    sep : str
        Separator between adjective and noun.
    n : int, optional
        Number of digits to take from hexadecimal of SHA-256 hash. Default: 8.
    wordlist: tuple, optional
        2-tuple containing adjective list and noun list. Default: use builtin word list.

    Returns
    -------
    str
        Adjective and noun separated by sep.

    Examples
    --------
    >>> encode('hello')
    'decorous_block'
    >>> encode('world')
    'late_kevin'
    >>> encode('world', sep='-')
    'late-kevin'
    >>> encode('world', sep='-', n=5)
    'peppy-gabriel'
    >>> encode(5.)
    'live_drum'
    >>> encode(['hello', 'world']) == encode(('hello', 'world'))
    True

    """

    adjectives, nouns = wordlist or _DEFAULT_WORDLIST

    # Take the first n characters of the hash and convert to an integer
    integer = int(hash(x, n=n), base=16)

    # Generate the two-word mnemonic from the hashed integer
    adjective = adjectives[integer % len(adjectives)]
    noun = nouns[(integer // len(adjectives)) % len(nouns)]
    mnemonic = sep.join((adjective, noun))

    return mnemonic


def _check_version() -> None:

    adjectives, nouns, latest_version, _words = _get_wordlist(full=True)

    versions = _words['versions']
    latest_version = versions[0]

    version_name = encode(adjectives + nouns,
                          wordlist=(adjectives, nouns))
    
    if version_name != latest_version:

        print(f'INFO: Word list has changed compared to {latest_version}. '
              f'Saving new list as {version_name}.',
              file=sys.stderr)
        _words['versions'] = [version_name] + _words['versions'][1:]
        del  _words['word lists'][latest_version]
        _words['word lists'][version_name] = dict(adjectives=adjectives, 
                                                  nouns=nouns)

        with open(_get_data_path(), 'w') as f:
            yaml.safe_dump(_words, f, 
                    default_flow_style=False, 
                    width=80, indent=1)
            
    return version_name

_check_version()
_DEFAULT_WORDLIST = _get_wordlist()
