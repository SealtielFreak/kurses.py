import abc
import typing


class EventTargetRuntime(abc.ABC):
    def load(self):
        ...

    @abc.abstractmethod
    def update(self, dt: typing.Union[int, float]):
        ...

    def resize(self, resizable: bool):
        ...

    def minimized(self):
        ...

    def hidden(self):
        ...

    def showed(self):
        ...

    def exposed(self):
        ...

    def restored(self):
        ...

    def close(self):
        ...

    def exit(self):
        ...

    def key_down(self, key: str):
        ...

    def key_up(self, key: str):
        ...

    def mouse(self, position: typing.Tuple[int, int], click: typing.List[str]):
        ...

    def scroll(self, move: int):
        ...


class EmptyTargetRuntime(EventTargetRuntime):
    def update(self, dt: typing.Union[int, float]):
        ...


def empty_target() -> None:
    ...
