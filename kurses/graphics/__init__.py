import collections
import math
import typing

import kurses.colors
from kurses.graphics.primitive import PolygonFigure, CircleFigure, RectangleFigure, LineFigure


class GraphicsBuffer:
    def __init__(self, **kwargs):
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.sx: int = kwargs.get("sx", 1)
        self.sy: int = kwargs.get("sy", 1)

        self.angle = 0
        self.__background_color: kurses.colors.Color = kwargs.get("background_color", (0, 0, 0))
        self.__primitives_figures = collections.deque()

    def __iter__(self):
        while bool(self.__primitives_figures):
            yield self.__primitives_figures.popleft()

    def clear(self):
        self.__primitives_figures.clear()

    @property
    def background(self) -> kurses.colors.Color:
        return self.__background_color

    def fill(self, color: kurses.colors.Color):
        self.__background_color = color

    def rotate(self, angle):
        self.angle += math.radians(angle)

    def line(self, start: typing.Tuple[int, int], end: typing.Tuple[int, int], color: kurses.colors.Color, thickness: int = 1):
        points = [*start, *end]

        line = LineFigure(
            points=tuple(points),
            color=color,
            thickness=thickness,
            filled=False,
        )

        self.__primitives_figures.append(line)

    def rect(self, x: int, y: int, size: typing.Tuple[int, int], color: kurses.colors.Color, filled: bool = False):
        rect = RectangleFigure(
            color=color,
            position=(x, y),
            size=size,
            filled=filled,
        )

        self.__primitives_figures.append(rect)

    def circle(self, x: int, y: int, r: int, color: kurses.colors.Color, filled: bool = False):
        circle = CircleFigure(
            color=color,
            position=(x, y),
            radius=r,
            filled=filled,
        )

        self.__primitives_figures.append(circle)

    def polygon(self, vertex: typing.List[typing.Union[int, float]], color: kurses.colors.Color, filled: bool = False):
        poly = PolygonFigure(
            color=color,
            vertex=vertex,
            filled=filled,
        )

        self.__primitives_figures.append(poly)
