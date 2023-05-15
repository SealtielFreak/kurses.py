import pyrogue.virtual_console
from pyrogue.virtual_console import T


class PygameVirtualConsole(pyrogue.virtual_console.VirtualConsole):
    def keyspressed(self) -> list[chr]:
        pass

    @property
    def window(self) -> T:
        pass

    @property
    def surface(self) -> T:
        pass

    @property
    def font(self) -> T:
        pass

    def clear_cache(self):
        pass

    def present(self):
        pass

    def events(self):
        pass

    def quit(self):
        pass

    @property
    def buffer(self) -> pyrogue.buffer_matrix.BufferTerm:
        pass

    def set_target(self, target):
        pass

    def main_loop(self):
        pass

    def set_title(self, _str: str):
        pass
