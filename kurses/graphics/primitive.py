import dataclasses
import typing

import kurses.colors


@dataclasses.dataclass
class PrimitiveFigure:
    color: kurses.colors.Color
    filled: bool


@dataclasses.dataclass
class LineFigure(PrimitiveFigure):
    points: typing.Tuple[int, int, int, int]
    thickness: int

    @property
    def start(self):
        return self.points[0], self.points[1]

    @property
    def end(self):
        return self.points[2], self.points[3]


@dataclasses.dataclass
class RectangleFigure(PrimitiveFigure):
    position: typing.Tuple[int, int]
    size: typing.Tuple[int, int]


@dataclasses.dataclass
class CircleFigure(PrimitiveFigure):
    position: typing.Tuple[int, int]
    radius: typing.Union[int, float]


@dataclasses.dataclass
class PolygonFigure(PrimitiveFigure):
    vertex: typing.List[typing.Union[int, float]]

    @property
    def points(self):
        return (
            [self.vertex[n] for n in range(0, self.length, 2)],
            [self.vertex[n] for n in range(1, self.length, 2)],
        )

    @property
    def length(self):
        return len(self.vertex) // 2
