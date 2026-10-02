import asyncio
import time
from typing import Callable, Awaitable, TypeVar

T = TypeVar("T")


async def async_retry(
    operation: Callable[[], Awaitable[T]],
    attempts: int = 3,
    timeout: int = 20,
    delay: int = 1
) -> T:
    """Run async external call with timeout and bounded retry."""

    last_error = None

    for attempt in range(attempts):
        try:
            return await asyncio.wait_for(
                operation(),
                timeout=timeout
            )

        except Exception as e:
            last_error = e

            if attempt < attempts - 1:
                await asyncio.sleep(delay)

    raise last_error


def sync_retry(
    operation: Callable[[], T],
    attempts: int = 3,
    delay: int = 1
) -> T:
    """Run sync external call with bounded retry."""

    last_error = None

    for attempt in range(attempts):
        try:
            return operation()

        except Exception as e:
            last_error = e

            if attempt < attempts - 1:
                time.sleep(delay)

    raise last_error