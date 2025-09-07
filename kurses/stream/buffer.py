import typing

from kurses.stream import CharacterAttribute, RectangleAttribute


class BufferMatrix:
    def __init__(self, shape):
        rows, columns = shape

        self.__rows, self.__cols = rows, columns
        self.__buffer_matrix = [[None] * columns for _ in range(rows)]

    @property
    def cols(self) -> int:
        return self.__cols

    @property
    def rows(self) -> int:
        return self.__rows

    def __setitem__(self, index: typing.Tuple[int, int], value: typing.Union[CharacterAttribute, RectangleAttribute]):
        x, y = 0, 0

        if isinstance(index, tuple):
            x, y = index

        while x >= self.cols:
            x = x - (self.cols + 1)
            y += 1

        while x < 0:
            x = x + (self.cols + 1)
            y -= 1

        value.x = x
        value.y = y

        if 0 <= x < self.cols and 0 <= y < self.rows:
            self.__buffer_matrix[y][x] = value

    def __getitem__(self, index: typing.Tuple[int, int]) -> typing.Union[CharacterAttribute, RectangleAttribute, None]:
        x, y = index

        return self.__buffer_matrix[y][x]

    def clear(self):
        self.__buffer_matrix = [[None] * self.__cols for _ in range(self.__rows)]

    def reshape(self, shape: typing.Tuple[int, int]):
        self.__rows, self.__cols = shape
        self.clear()

    @property
    def shape(self) -> typing.Tuple[int, int]:
        return self.__rows, self.__cols

    @shape.setter
    def shape(self, shape: typing.Tuple[int, int]):
        self.__rows, self.__cols = shape

    def __iter__(self):
        for i in range(self.__rows):
            for j in range(self.__cols):
                attr = self.__buffer_matrix[i][j]

                if attr is not None:
                    yield attr
