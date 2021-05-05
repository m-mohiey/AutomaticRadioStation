from abc import ABC, abstractmethod

class AbstractPlayer(ABC):

    @abstractmethod
    def open(self, media):
        pass

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def wait(self):
        pass