#!/usr/bin/env python3

"""
Defines `to_kv`.
"""

from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Returns the tuple (k, v squared).
    """

    return (k, float(v * v))
