import weakref


class Event:
    def __init__(self, name):
        self._listeners = []
        self.name = name

    def add_listener(self, listener):
        if hasattr(listener, '__self__') and hasattr(listener, '__func__'):
            listener_obj = listener.__self__
            listener = weakref.WeakMethod(listener)
        else:
            listener_obj = listener
            listener = weakref.ref(listener)

        # FIXME: I think a lock is needed for thread safety
        weakref.finalize(listener_obj, self.remove_listener, listener)
        self._listeners.append(listener)

    def remove_listener(self, listener):
        print("released: ", listener, self.name)
        self._listeners.remove(listener)

    def emit(self, sender, **kwargs):
        for listener in self._listeners:
            listener()(event=self, sender=sender, **kwargs)

