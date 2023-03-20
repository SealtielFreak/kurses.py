import pyrlkit.buffer_matrix
import pyrlkit.virtual_console


class PygameVirtualConsole(pyrlkit.virtual_console.VirtualConsole):
    @property
    def buffer(self) -> pyrlkit.buffer_matrix.BufferMatrix:
        pass

    def set_target(self, target):
        pass

    def main_loop(self):
        pass

    def set_title(self, _str: str):
        pass
