class ShutdownDelay:
    def __init__(self, delay, color=None):
        self._delay = delay
        self._color = color

    @property
    def delay(self):
        return self._delay

    @property
    def color(self):
        return self._color
