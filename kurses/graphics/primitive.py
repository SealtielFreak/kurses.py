import dataclasses
import typing

import kurses.colors


@dataclasses.dataclass
class PrimitiveFigure:
    color: kurses.colors.Color
    filled: bool


@dataclasses.dataclass
class LineFigure(PrimitiveFigure):
    points: typing.List[typing.Tuple[float, float]]


@dataclasses.dataclass
class CircleFigure(PrimitiveFigure):
    position: typing.Tuple[int, int]
    radius: typing.Union[int, float]


@dataclasses.dataclass
class PolygonFigure(PrimitiveFigure):
    vertex: typing.List
