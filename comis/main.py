from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable
from inspect import signature
from typing import Any, Callable, Literal

from asyncpraw import Reddit
from asyncpraw.models.reddit.comment import Comment, CommentModeration
from asyncpraw.models.reddit.submission import Submission, SubmissionModeration

from .utils import content_type, mod_type

_logger = logging.getLogger(__name__)

_valid_events = ("post", "comment")


class Event:
    events: dict[Literal["submission", "comment"], list[Event]] = {
        "submission": [],
        "comment": [],
    }

    def __init__(
        self,
        evt: str,
        evt_type: Literal["submission", "comment"],
        handler: Callable[[content_type, mod_type], Awaitable[None]],
        criteria: dict[str, Any],
    ):
        self.event: str = evt
        self.handler: Callable[[content_type, mod_type], Awaitable[None]] = handler
        self.criteria = criteria

        self.events[evt_type].append(self)

        self.before: list[Callable[[content_type, mod_type], Awaitable[bool]]] = []

    async def __call__(self, *args, **kwargs):
        print(args, kwargs)
        for predicate in self.before:
            if not await predicate(*args, **kwargs):
                break
        else:
            await self.handler(self, *args, **kwargs)


def submission(**kwargs):
    def wrapper(handler: Callable[[Submission, SubmissionModeration], Awaitable[None]]):
        e = Event(handler.__name__, "submission", handler, kwargs)

        for condition in kwargs:
            pass

        return e

    return wrapper


def comment(**kwargs):
    def wrapper(handler: Callable[[Comment, CommentModeration], Awaitable[None]]):
        return Event(handler.__name__, "comment", handler, kwargs)

    return wrapper


class Client:
    def __init__(
        self,
        client_id,
        client_secret,
        user_agent: str,
        username: str,
        password: str,
        subreddits: list[str],
    ):
        self._create_reddit = lambda: Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )

        self.reddit: Reddit = None  # type: ignore

        self.subreddits = subreddits
        self._subreddits = "+".join(subreddits)

    async def process(self, payload: content_type) -> None:
        evt_type = "submission" if isinstance(payload, Submission) else "comment"
        for evt in Event.events[evt_type]:  # type: ignore
            sig = signature(evt.handler)
            if sig.parameters.get("self", None) is not None:
                await evt.handler(self, payload, payload.mod)  # type: ignore
            else:
                await evt.handler(payload, payload.mod)

    async def _run(self):
        print(self)
        if self.reddit is None:
            self.reddit = self._create_reddit()

        async for post in (
            await self.reddit.subreddit(self._subreddits)
        ).stream.submissions():
            await self.process(post)

    def run(self) -> None:
        asyncio.new_event_loop().run_until_complete(self._run())
