#!/usr/bin/env python3

"""
Defines `measure_time`.
"""

import asyncio
import time

wait_n = __import__("1-concurrent_coroutines").wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Returns the total execution time for `wait_n`.
    """

    epoch = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    total_time = time.perf_counter() - epoch

    return total_time / n
