class Event:
    def __init__(self):
        self._handlers = []

    def add(self, handler):
        self._handlers.append(handler)

        return self

    def remove(self, handler):
        self._handlers.remove(handler)

        return self

    def fire(self, sender, args = []):
        for handler in self._handlers:
            handler(sender, *args)

    __iadd__ = add
    __isub__ = remove
    __call__ = fire


