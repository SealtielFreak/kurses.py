import pyrogue.virtual_console


class PygameVirtualConsole(pyrogue.virtual_console.VirtualConsole):
    @property
    def buffer(self) -> pyrogue.buffer_matrix.BufferTerm:
        pass

    def set_target(self, target):
        pass

    def main_loop(self):
        pass

    def set_title(self, _str: str):
        pass
