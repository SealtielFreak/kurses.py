import pyrlkit.backend.virtual_console
import pyrlkit.buffer_matrix


class PygameVirtualConsole(pyrlkit.backend.virtual_console.VirtualConsole):
    @property
    def buffer(self) -> pyrlkit.buffer_matrix.BufferMatrix:
        pass

    def set_target(self, target):
        pass

    def main_loop(self):
        pass

    def set_title(self, _str: str):
        pass
