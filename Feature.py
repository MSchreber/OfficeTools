from abc import ABC, abstractmethod

class Feature(ABC):
    @abstractmethod
    def run(self, frame, return_callback):
        pass