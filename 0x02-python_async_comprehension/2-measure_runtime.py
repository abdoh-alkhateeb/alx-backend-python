#!/usr/bin/env python3

"""
Defines `measure_runtime`.
"""

import asyncio
import time

async_comprehension = __import__("1-async_comprehension").async_comprehension


async def measure_runtime() -> float:
    """
    Returns the total execution time of running `async_comprehension` 4 times.
    """

    epoch = time.perf_counter()

    await asyncio.gather(*[asyncio.create_task(async_comprehension())
                           for _ in range(4)])

    total_time = time.perf_counter() - epoch

    return total_time
