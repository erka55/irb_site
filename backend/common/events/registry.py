from collections import defaultdict
from collections.abc import Callable

from .base import BaseEvent
from common.events.types import EventTypes

class EventHandlerRegistry:
    """
    In-memory registry mapping event types to handlers.
    """

    def __init__(self):
        self._handlers: dict[
            str,
            list[Callable[[BaseEvent], None]]
        ] = defaultdict(list)

    def register(
        self,
        event_type: str,
        handler: Callable[[BaseEvent], None],
    ) -> None:

        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)

    def get_handlers(
        self,
        event_type: str,
    ) -> list[Callable[[BaseEvent], None]]:

        return list(
            self._handlers.get(event_type, [])
        )


registry = EventHandlerRegistry()
