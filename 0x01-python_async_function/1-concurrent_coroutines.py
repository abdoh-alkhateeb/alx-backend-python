#!/usr/bin/env python3

"""
Defines `wait_n`.
"""

import asyncio
from typing import List

wait_random = __import__("0-basic_async_syntax").wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Returns a list of delays from spawning `wait_random` n times.
    """

    tasks = [asyncio.create_task(wait_random(max_delay)) for _ in range(n)]
    delays = await asyncio.gather(*tasks)

    return sorted(delays)
