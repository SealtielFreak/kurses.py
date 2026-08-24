import abc
import typing

from kurses.resources.mixer.sound import Sound


class Music(Sound, abc.ABC):
    @abc.abstractmethod
    def resume(self):
        ...

    @abc.abstractmethod
    def fadeout(self, seconds: typing.Optional[typing.Union[int, float]]):
        ...

    @abc.abstractmethod
    def loop(self, repeat: typing.Optional[bool]):
        ...

    @abc.abstractmethod
    def pause(self):
        ...
