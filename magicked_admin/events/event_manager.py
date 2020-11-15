import logging
from events.event import Event

logger = logging.getLogger(__name__)


class EventManager:
    def __init__(self):
        self._events = {}

    def register_event(self, event, listener):
        if event not in self._events.keys():
            self._events[event] = Event(event)

        self._events[event].add_listener(listener)

    def unregister_event(self, event, listener):
        if event in self._events.keys() and listener in self._events[event]:
            self._events[event].remove_listener(listener)

    def emit_event(self, event, sender, **kwargs):

        # Find the signal for this event
        # trigger it

        logger.debug("emission:" + str(event) + str(sender) + str(kwargs))
        if event in self._events.keys():
            self._events[event].emit(sender, **kwargs)
