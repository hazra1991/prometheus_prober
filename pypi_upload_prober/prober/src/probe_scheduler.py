import logging
import threading

from .utils import Timer
from abc import ABC, abstractmethod
from .errors import DuplicateProberError
from .logger import get_logger


class BaseProber(ABC):

    def __init__(self, name, metric, interval: float = 0.0, log_dir=None):

        self._name = name
        self._interval = interval
        self._metric = metric.get_defined_metrices
        self._logger = get_logger(name, "info", log_dir=log_dir)
        self._thread = threading.Thread(target=self.run)
        self._thread.daemon = True
        self._scheduler = None
        self._event = threading.Event()

    @property
    def logger(self):
        return self._logger

    @property
    def get_defined_metric(self):
        return self._metric

    @property
    def name(self):
        return self._name

    def register(self, scheduler):
        """Registers this prober with a scheduler."""
        self._scheduler = scheduler

    def start(self):
        """Start the prober."""
        self._logger.info(f'starting {self._name}')
        self._thread.start()
        return self._thread, self._name

    @abstractmethod
    def probe(self):
        """The main probe logic should be defined here"""
        raise NotImplementedError('virtual method')

    def run(self):
        """Execute probes and space them out at regular intervals."""

        while True:
            try:
                with Timer() as timer:
                    self.probe()
            except Exception as e:
                msg = f"Critical Error ******* at {self.name} Exception: {str(e)}"
                self._logger.exception(msg)
            if self._interval > 0.0:
                delay = max(0.0, self._interval - timer.duration)
                self._logger.info(f'{self._name} sleeping for {delay:.0f} second(s)')
                self._event.wait(timeout=delay)


class ProberScheduler:
    """A scheduler that runs probers."""
    def __init__(self, probers, logger=None, log_dir=None, sanity_interval: float = 6.0):
        if logger:
            self._logger = logger
        else:
            self._logger = get_logger(self.__class__.__name__, 'INFO', log_dir=log_dir, backup_count=5)
        self._probers = probers
        self._shutdown = threading.Event()
        self._thread_pool = {}
        self._wait = sanity_interval

    def shutdown(self):
        """Quits the scheduler loop."""
        self._logger.info('shutting down')
        self._shutdown.set()

    def start(self):
        """Schedules probes to run and handle retry logic."""
        self._logger.info('starting probers')
        for prober in self._probers:
            if prober.name in self._thread_pool:
                raise DuplicateProberError()
            prober.register(self)
            thread, name = prober.start()
            self._thread_pool.setdefault(name, thread)

        while not self._shutdown.is_set():
            # TODO set a signal interrupt
            th_name = list(self._thread_pool.keys())
            try:
                self._logger.info('waiting for shutdown requests')
                self._logger.debug(f"Total thread pool {self._thread_pool}")
                if th_name:
                    for th in th_name:
                        if not self._thread_pool[th].is_alive():
                            self._logger.error(f"Thread {th} died ,removing from pool")
                            self._thread_pool.pop(th)
                    self._shutdown.wait(timeout=self._wait)
                else:
                    self.shutdown()
            except KeyboardInterrupt:
                self.shutdown()
        self._logger.info('All probe down exiting')
