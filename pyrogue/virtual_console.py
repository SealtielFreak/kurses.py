import abc

import pyrogue.buffer_matrix


class VirtualConsole(abc.ABC):
    @property
    @abc.abstractmethod
    def buffer(self) -> pyrogue.buffer_matrix.BufferMatrix: ...

    @abc.abstractmethod
    def set_target(self, target): ...

    @abc.abstractmethod
    def main_loop(self): ...

    @abc.abstractmethod
    def set_title(self, _str: str): ...
