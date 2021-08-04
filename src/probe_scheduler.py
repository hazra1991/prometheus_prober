import logging
import threading

from .utils import Timer


class BaseProber:

    def __init__(self, name, interval: float = 0.0):

        self._name = name
        self._interval = interval
        self._logger = logging.getLogger(name)
        self._thread = threading.Thread(target=self.run)
        self._thread.daemon = True
        self._scheduler = None
        self._event = threading.Event()

    def register(self, scheduler):
        """Registers this prober with a scheduler."""
        self._scheduler = scheduler

    def start(self):
        """Start the prober."""
        self._logger.info(f'starting {self._name}')
        self._thread.start()

    def probe(self):
        """The main probe logic should be deined here"""
        raise NotImplementedError('virtual method')

    def run(self):
        """Execute probes and space them out at regular intervals."""
        while True:
            with Timer() as timer:
                self.probe()
            if self._interval > 0.0:
                delay = max(0.0, self._interval - timer.duration)
                self._logger.info(f'sleeping for {delay:.0f} second(s)')
                self._event.wait(timeout=delay)


class ProberScheduler:
    """A scheduler that runs probers."""
    def __init__(self, *probers: BaseProber):
        # self._logger = logging.getLogger(self.__class__.__name__)
        self._probers = probers
        self._shutdown = threading.Event()

    def shutdown(self):
        """Quits the scheduler loop."""
        # self._logger.info('shutting down')
        self._shutdown.set()

    def start(self):
        """Schedules probes to run and handle retry logic."""
        # self._logger.info('starting probers')
        for prober in self._probers:
            prober.register(self)
            prober.start()

        while not self._shutdown.is_set():
            # TODO set a signal interrupt
            try:
                # self._logger.info('waiting for shutdown requests')
                self._shutdown.wait(timeout=60.0)
            except KeyboardInterrupt:
                self.shutdown()
        # self._logger.info('exiting')
