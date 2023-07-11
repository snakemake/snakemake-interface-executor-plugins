from abc import ABC, abstractmethod


class LoggerExecutorInterface(ABC):
    @abstractmethod
    def info(self, msg: str):
        ...

    @abstractmethod
    def error(self, msg: str):
        ...

    @abstractmethod
    def debug(self, msg: str):
        ...
