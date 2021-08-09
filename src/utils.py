import time
from functools import wraps

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


def retryOnException(ExceptionToCheck, retry=2, delay=2, logger=None):
    def decorator(fun):
        @wraps(fun)
        def inner(*a ,**kw):
            mretry, mdelay = retry, delay
            while mretry > 1:
                try:
                    return fun(*a, **kw)
                except ExceptionToCheck as e:
                    msg = f"{str(e)}, Retrying in {mdelay} seconds..."
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mretry -= 1
            return None
        return inner
    return decorator