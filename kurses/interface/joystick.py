import abc
import typing

AxisType = typing.Tuple[str, bool, float, float]
TriggerType = typing.Tuple[str, bool, float]
JoystickType = typing.Tuple[
    str,
    typing.Set[str],
    typing.Tuple[AxisType, AxisType],
    typing.Tuple[TriggerType, TriggerType]
]


class JoystickInterface(abc.ABC):
    @abc.abstractmethod
    def open(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    @property
    @abc.abstractmethod
    def inputs(self) -> typing.Tuple[JoystickType, ...]:
        pass
