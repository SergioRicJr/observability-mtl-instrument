from abc import ABCMeta, abstractmethod


class LogRequestInterface(metaclass=ABCMeta):
    @abstractmethod
    def make_request(self):
        raise NotImplementedError('Run function was not implemented')
