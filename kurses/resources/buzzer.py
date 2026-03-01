import abc
import typing


class Buzzer(abc.ABC):
    @abc.abstractmethod
    def record(self, track_id: int, notes: typing.List[typing.Tuple[int, int]]):
        ...

    @abc.abstractmethod
    def play(self, track_id: int, volume: int, loop: typing.Optional[bool] = None):
        ...

    @abc.abstractmethod
    def beep(self, frequency: float, duration_ms: int, volume: typing.Optional[int]):
        ...

    @abc.abstractmethod
    def stop(self):
        ...

    @abc.abstractmethod
    def playing(self) -> bool:
        ...

    @abc.abstractmethod
    def update(self):
        ...
