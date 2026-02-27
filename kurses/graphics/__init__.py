import collections
import math

import kurses.colors
from kurses.graphics.primitive import PolygonFigure, CircleFigure


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

    @property
    def background(self) -> kurses.colors.Color:
        return self.__background_color

    def fill(self, color: kurses.colors.Color):
        self.__background_color = color

    def rotate(self, angle):
        self.angle += math.radians(angle)

    def rect(self, x: int, y: int, size, color: kurses.colors.Color):
        w, h = size

        rect = PolygonFigure(
            color=color,
            vertex=[
                [x, y],
                [x, y + h],
                [x + w, y],
                [x + w, y + h],
            ]
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

    def polygon(self, color: kurses.colors.Color):
        pass
