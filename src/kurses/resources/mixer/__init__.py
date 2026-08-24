import abc


class AudioSystem(abc.ABC):
    def __init__(self, frequency: int, format: int, channels: int = 2):
        self.__frequency = frequency
        self.__format = format
        self.__channels = channels

    @property
    def frequency(self):
        return self.__frequency

    @property
    def format(self):
        return self.__format

    @property
    def channels(self):
        return self.__channels

    @abc.abstractmethod
    def init(self):
        ...

    @abc.abstractmethod
    def enabled(self):
        ...
