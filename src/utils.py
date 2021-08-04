import time

class Timer:
    """A context manager that measure the duration of it's with block."""
    def __init__(self, timer=time.perf_counter):
        self._timer = timer
        self._duration = 0.0
        self._started = False
        self._start = 0.0

    @property
    def duration(self):
        """Returns the duration of the timer."""
        if self._started:
            self.stop()
        return self._duration

    def start(self):
        """Starts the timer."""
        self._start = self._timer()
        self._started = True

    def stop(self):
        """Stops the timer."""
        self._duration = max(self._timer() - self._start, 0)
        self._started = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, typ, value, traceback):
        self.stop()