import time

from functools import wraps
from threading import Event, Thread
from .errors import RetryTimedOut


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


class Timeout(Thread):
    def __init__(self, timeout, evnt):
        super().__init__()
        self.daemon = True
        self.timeout = timeout
        self.event = evnt

    def run(self):
        self.event.wait(timeout=self.timeout)
        if not self.event.is_set():
            self.event.set()
        return None

    def stop(self):
        self.event.set()


def retryOnException(*exp_to_check, retry=2, delay=2, logger=None):
    def decorator(fun):
        @wraps(fun)
        def inner(*a, **kw):
            mretry, mdelay = retry, delay
            while mretry >= 1:
                try:
                    return fun(*a, **kw)
                except exp_to_check as e:
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


def retryUntilTrue(timeout=60.0, delay=5):
    """raises exception RetryTimedOut .Retries till success/True """
    def decorator(f):
        @wraps(f)
        def inner(*a, **kw):
            event = Event()
            alarm = Timeout(timeout, event)
            alarm.start()
            try:
                while not event.is_set():
                    event.wait(timeout=delay)
                    val: bool = f(*a, **kw)
                    if val:
                        event.set()
                        return val
            except Exception as e:
                alarm.stop()
                raise e
            raise RetryTimedOut(f'The function {f.__qualname__} Timed out')
        return inner
    return decorator


def logException(logger_p):
    def decorator(fun):
        @wraps(fun)
        def inner(*a, **kw):
            try:
                logger_p.info(f"starting to run {fun.__name__}")
                return fun(*a, **kw)
            except Exception as e:
                msg = f"Critical Error ******* at {fun.__qualname__} Exception: {str(e)}"
                logger_p.exception(msg)
                return

        return inner
    return decorator
