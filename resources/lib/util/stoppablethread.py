from abc import ABCMeta, abstractmethod
from threading import Event, Thread


class StoppableThread(Thread):
    __metaclass__ = ABCMeta

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self._stop = Event()
        self.start()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass
