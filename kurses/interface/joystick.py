import abc
import dataclasses
import typing

J = typing.TypeVar("J", bound="JoystickInterface")


@dataclasses.dataclass(frozen=True)
class AxisValue:
    name: str

    stick: bool
    x: float
    y: float

    def __hash__(self) -> int:
        return hash(self.name)


@dataclasses.dataclass(frozen=True)
class TriggerValue:
    name: str

    shoulder: bool
    trigger: float

    def __hash__(self) -> int:
        return hash(self.name)


@dataclasses.dataclass(frozen=True)
class JoystickInput:
    name: str
    connected: bool
    buttons: typing.Set[str]
    axis: typing.Tuple[AxisValue, AxisValue]
    triggers: typing.Tuple[TriggerValue, TriggerValue]

    def __hash__(self) -> int:
        return hash(self.name)

    @property
    def left_axis(self):
        return self.axis[0]

    @property
    def right_axis(self):
        return self.axis[1]


class JoystickInterface(abc.ABC, typing.Generic[J]):
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
    def inputs(self) -> typing.Tuple[JoystickInput, ...]:
        pass
