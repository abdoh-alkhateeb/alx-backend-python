#!/usr/bin/env python3

"""
Defines `element_length`.
"""

from typing import Iterable, List, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Returns a list of tuples of the form (sequence, sequence length).
    """

    return [(i, len(i)) for i in lst]
