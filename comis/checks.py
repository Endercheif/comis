from collections.abc import Awaitable
from typing import Any, Callable

from comis.utils import content_type


def check(predicate: Callable[[content_type, Any], Awaitable[bool]]):
    def decorator(func):
        func.before.append(predicate)
        return func

    return decorator
