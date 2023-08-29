
from typing import List

import argparse


def split_text(s: str, max_len: int) -> List[str]:
    """
    Splits text to several parts with len<=max
    Args:
        s:
        max_len:

    Returns:

    >>> _ = split_text
    >>> _('t', max_len=10)
    ['t']
    >>> _('text', max_len=1)
    ['t', 'e', 'x', 't']
    >>> _('text with spaces', max_len=5)
    ['text', 'with', 'space', 's']
    >>> _('some usual text with many words', max_len=14)
    ['some usual', 'text with many', 'words']
    >>> _s = 'simple not so short test string'
    >>> for i in range(1, len(_s) + 3):
    ...     result = _(_s, max_len=i)
    ...     assert all(len(r) <= i for r in result), (i, result)
    """

    assert max_len > 0

    words = s.split()
    lines: List[List[str]] = [[]]

    cur_len = 0

    def process_word(w: str):
        nonlocal cur_len

        wlen = len(w)
        slen = 1 if cur_len else 0
        next_len = cur_len + slen + wlen

        if next_len <= max_len:
            lines[-1].append(w)
            cur_len = next_len
        elif wlen <= max_len:
            lines.append([w])
            cur_len = wlen
        else:
            symbols_left = max_len - cur_len - slen
            if symbols_left <= 0:
                lines.append([])
                cur_len = 0
                process_word(w)
                return

            lines[-1].append(w[:symbols_left])

            lines.append([])
            cur_len = 0
            process_word(w[symbols_left:])

    for _w in words:
        process_word(_w)

    return [' '.join(row) for row in lines]



